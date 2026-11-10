"""Elasticidade3D de tira local: tetraedros lineares, carga uniforme na ponta.

Geometria representativa da hipótese de balanço; não FEM da carroceria ou chapa
perfurada inteira. Picos junto ao engaste não são tensões convergidas de projeto.
"""
import json
from pathlib import Path

import gmsh
import numpy as np
import pandas as pd
import yaml
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas'


def shape_gradients(barycentric,corner_gradients,order=1):
    if order==1:return corner_gradients
    # GmshTet10 order, read from installedAPI getElementProperties(11).
    edges=[(0,1),(1,2),(2,0),(0,3),(2,3),(1,3)]
    l=np.array(barycentric);grad=np.zeros((3,10))
    grad[:,:4]=corner_gradients*(4*l-1)
    for index,(a,b) in enumerate(edges,start=4):
        grad[:,index]=4*(l[a]*corner_gradients[:,b]+l[b]*corner_gradients[:,a])
    return grad


def strain_operator(grad):
    b=np.zeros((6,3*grad.shape[1]))
    for i,(dx,dy,dz) in enumerate(grad.T):
        b[:,3*i:3*i+3]=[[dx,0,0],[0,dy,0],[0,0,dz],[dy,dx,0],[0,dz,dy],[dz,0,dx]]
    return b


def solve(length,width,thickness,force,young,poisson,size,dest,order=1):
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal',0);gmsh.model.add('tira3d')
        gmsh.model.occ.addBox(0,0,0,length,width,thickness);gmsh.model.occ.synchronize()
        gmsh.option.setNumber('Mesh.MeshSizeMin',size);gmsh.option.setNumber('Mesh.MeshSizeMax',size)
        gmsh.model.mesh.generate(3)
        if order==2:gmsh.model.mesh.setOrder(2)
        tags,xyz,_=gmsh.model.mesh.getNodes();xyz=np.array(xyz).reshape(-1,3)
        lookup={int(tag):i for i,tag in enumerate(tags)}
        _,conn=gmsh.model.mesh.getElementsByType(4 if order==1 else 11);cells=np.array([lookup[int(t)] for t in conn]).reshape(-1,4 if order==1 else 10)
        _,tri=gmsh.model.mesh.getElementsByType(2 if order==1 else 9);tri=np.array([lookup[int(t)] for t in tri]).reshape(-1,3 if order==1 else 6)
    finally:gmsh.finalize()
    lam=young*poisson/((1+poisson)*(1-2*poisson));mu=young/(2*(1+poisson))
    d=np.zeros((6,6));d[:3,:3]=lam;d[:3,:3]+=2*mu*np.eye(3);d[3:,3:]=mu*np.eye(3)
    ndof=3*cells.shape[1]
    rows=np.empty((len(cells),ndof**2),dtype=np.int32);cols=np.empty_like(rows)
    values=np.empty_like(rows,dtype=float);element_data=[]
    gauss=[np.full(4,.25)] if order==1 else [np.roll([.5854101966249685,.1381966011250105,.1381966011250105,.1381966011250105],i) for i in range(4)]
    for index,cell in enumerate(cells):
        points=xyz[cell[:4]];a=np.column_stack((np.ones(4),points));volume=abs(np.linalg.det(a))/6
        grad=np.linalg.inv(a)[1:,:];ke=np.zeros((ndof,ndof))
        for point in gauss:
            b=strain_operator(shape_gradients(point,grad,order));ke+=volume/len(gauss)*b.T@d@b
        b=strain_operator(shape_gradients(np.full(4,.25),grad,order))
        dofs=(cell[:,None]*3+np.arange(3)).ravel()
        rows[index]=np.repeat(dofs,ndof);cols[index]=np.tile(dofs,ndof);values[index]=ke.ravel()
        element_data.append((dofs,b,volume))
    matrix=coo_matrix((values.ravel(),(rows.ravel(),cols.ravel())),shape=(len(xyz)*3,)*2).tocsr();load=np.zeros(len(xyz)*3)
    tip_area=0
    for face in tri:
        p=xyz[face]
        if not np.allclose(p[:,0],length,atol=1e-10,rtol=0):continue
        area=np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))/2;tip_area+=area
        load[3*(face if order==1 else face[3:])+2]+=area*force/(width*thickness)/3
    fixed_nodes=np.where(np.abs(xyz[:,0])<1e-10)[0];fixed=(fixed_nodes[:,None]*3+np.arange(3)).ravel()
    free=np.setdiff1d(np.arange(len(load)),fixed);u=np.zeros(len(load));u[free]=spsolve(matrix[free][:,free],load[free])
    residual=matrix@u-load;reaction=np.zeros_like(load);reaction[fixed]=residual[fixed]
    force_error=load.reshape(-1,3).sum(axis=0)+reaction.reshape(-1,3).sum(axis=0)
    moment_error=np.cross(xyz,load.reshape(-1,3)+reaction.reshape(-1,3)).sum(axis=0)
    stress=[];centers=[];volumes=[]
    for cell,(dofs,b,vol) in zip(cells,element_data,strict=True):
        stress.append(d@b@u[dofs]);centers.append(xyz[cell].mean(axis=0));volumes.append(vol)
    stress=np.array(stress);centers=np.array(centers)
    vm=np.sqrt(((stress[:,0]-stress[:,1])**2+(stress[:,1]-stress[:,2])**2+(stress[:,2]-stress[:,0])**2)/2+3*(stress[:,3:]**2).sum(axis=1))
    tip_disp=float(load@u/force)
    np.savez_compressed(dest,xyz_m=xyz,tetrahedra=cells,displacement_m=u.reshape(-1,3),centers_m=centers,stress_pa=stress,von_mises_pa=vm)
    inertia=width*thickness**3/12;area=width*thickness
    reference=force*length**3/(3*young*inertia)+force*length/((5/6)*mu*area)
    return {'element_order':order,'mesh_size_m':size,'nodes':len(xyz),'elements':len(cells),'tip_area_m2':tip_area,
        'force_n':force,'force_residual_n':float(max(abs(force_error))),'moment_residual_nm':float(max(abs(moment_error))),
        'free_residual_n':float(max(abs(residual[free]))),'volume_m3':sum(volumes),'tip_work_average_m':tip_disp,
        'timoshenko_comparator_m':reference,'strain_energy_j':float(u@matrix@u/2),'external_work_j':float(load@u),
        'max_von_mises_pa_not_converged':float(vm.max()),'peak_stress_validated':False}


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());g=c['development']['mounting_redesign'];f=g['solid_verification']
    selected=pd.read_csv(OUT/'selecoes.csv');rows=[]
    runs=[(ident,size) for ident in f['components'] for size in f['mesh_sizes_m']+f.get('extra_mesh_sizes_m',{}).get(ident,[])]
    for ident,size in runs:
        s=selected[selected.component==ident].iloc[0]
        demand=pd.read_csv(OUT/f'demandas_{ident}_{int(s.span_x_m*1000)}x{int(s.span_y_m*1000)}.csv')
        force=float(demand.max_tension_n.max())
        result=solve(g['local_flange_lever_m'],g['tributary_strip_width_m'],float(s.thickness_m),force,f['young_pa'],f['poisson'],size,OUT/f'campo_{ident}_{size:.4f}.npz')
        rows.append({'component':ident,'thickness_m':float(s.thickness_m),**result})
    df=pd.DataFrame(rows);df.to_csv(OUT/'elasticidade3d_convergencia.csv',index=False)
    convergence=[]
    for name,group in df.groupby('component'):
        group=group.sort_values('mesh_size_m',ascending=False);a,b=group.tip_work_average_m.iloc[-2:]
        convergence.append({'component':name,'last_relative_displacement_change':abs(b-a)/abs(b),'displacement_refinement_criterion_met':bool(abs(b-a)/abs(b)<=f['displacement_relative_change_criterion']),'peak_stress_validated':False})
    (OUT/'elasticidade3d_resumo.json').write_text(json.dumps({'cases':len(rows),'convergence':convergence,
        'max_force_residual_n':float(df.force_residual_n.max()),'max_moment_residual_nm':float(df.moment_residual_nm.max()),
        'physical_validation':False,'limits':'Tira3D elástica com engaste ideal;sem furo/contato/prying/carroceria. ComparadorTimoshenko não é soluçãoexata3D. Picos de engaste não promovidos a resistência.'},indent=2,ensure_ascii=False)+'\n')
    print(df.to_string(index=False))


if __name__=='__main__':main()
