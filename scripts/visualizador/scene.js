import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const host = document.querySelector('#scene');
const note = document.querySelector('#loading');
const data = window.AURORA_DATA;
const scene = new THREE.Scene();
scene.background = new THREE.Color('#ecf0f3');
const camera = new THREE.PerspectiveCamera(42, 1, .05, 100);
camera.up.set(0, 0, 1);
camera.position.set(6, -7, 4.5);
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
renderer.localClippingEnabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = .9;
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
host.append(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(-.5, 0, 1.2); controls.enableDamping = true;
controls.listenToKeyEvents(window);
scene.add(new THREE.HemisphereLight(0xffffff, 0x62676c, 2.3));
const sun = new THREE.DirectionalLight(0xffffff, 2.7);
sun.position.set(3,-4,8); scene.add(sun);
const back = new THREE.DirectionalLight(0xc9e4ff, 1.8);
back.position.set(-5,4,4); scene.add(back);
const grid = new THREE.GridHelper(12, 24, '#7c8a96', '#c4ccd2');
grid.rotation.x = Math.PI/2; grid.position.z = -.02; scene.add(grid);
const originalOpacity = new Map();
const roofClip = new THREE.Plane(new THREE.Vector3(0,0,-1), 2.05);
let shell, insideModel, stowed, deployed, fixed, electrical, portableGround, portableStorage;
let activeItem;
function load(encoded) {
  if(!encoded) return Promise.resolve(new THREE.Group());
  return new Promise((resolve,reject) => {
    const bytes = Uint8Array.from(atob(encoded), c => c.charCodeAt(0));
    new GLTFLoader().parse(bytes.buffer, '', gltf => resolve(gltf.scene), reject);
  });
}
function eachMaterial(root, callback) {
  root?.traverse(obj => {
    if(obj.isMesh) (Array.isArray(obj.material) ? obj.material : [obj.material]).forEach(callback);
  });
}
function update() {
  const inside = document.querySelector('#inside').checked;
  const technical = document.querySelector('#technical').checked;
  if(insideModel) insideModel.visible = inside && !technical;
  if(electrical) electrical.visible = document.querySelector('#electrical').checked;
  electrical?.traverse(obj => {if(obj.isMesh && obj.name.startsWith('mppt_extensao__')) obj.visible = document.querySelector('#extensionInstalled').checked;});
  const isolated = document.querySelector('#isolate').checked && activeItem;
  insideModel?.traverse(obj => {
    if(obj.isMesh) obj.visible = (!obj.name.startsWith('cama__') || !document.querySelector('#hideBed').checked) && (!isolated || obj.name.startsWith(activeItem+'__'));
  });
  electrical?.traverse(obj => {
    if(obj.isMesh) obj.visible = (!obj.name.startsWith('mppt_extensao__') || document.querySelector('#extensionInstalled').checked) && (!isolated || obj.name.startsWith(activeItem+'__') || (activeItem === 'hvac' && obj.name.startsWith('dutos_hvac__')));
  });
  if(shell) shell.visible = !document.querySelector('#hideShell').checked && !technical;
  const solar = document.querySelector('#panels').checked && !technical;
  const open = document.querySelector('#deploy').checked;
  const extension = document.querySelector('#extensionInstalled').checked;
  if(fixed) fixed.visible = solar && !extension;
  if(stowed) stowed.visible = solar && extension && !open;
  if(deployed) deployed.visible = solar && extension && open;
  const portable = document.querySelector('#portableInstalled').checked;
  const portableOpen = document.querySelector('#portableDeployed').checked;
  if(portableGround) portableGround.visible = portable && portableOpen && !technical;
  if(portableStorage) portableStorage.visible = portable && !portableOpen && !technical;
  eachMaterial(shell, mat => {
    mat.opacity = inside ? .22 : originalOpacity.get(mat);
    mat.transparent = mat.opacity < 1; mat.depthWrite = !inside;
    mat.clippingPlanes = inside ? [roofClip] : [];
    mat.wireframe = document.querySelector('#wire').checked;
    mat.needsUpdate = true;
  });
  document.querySelector('#solarState').textContent = technical
    ? 'Vista técnica: carroceria, interior e cobertura retirados para inspeção das instalações.' : !extension
    ? 'Cobertura fixa: 3 JA + 1 Victron, 1.540 W STC. Proposta principal mais leve.' : open
    ? 'Estacionado / aberto: 7 módulos expostos, 2.890 W STC; largura 3,564 m.'
    : 'Recolhido: 3 JA + 1 Victron expostos, 1.540 W STC. Camada JA inferior sombreada.';
  if(portable && !technical) document.querySelector('#solarState').textContent += portableOpen
    ? ' Alternativa: +1.600 W no solo, somente parado. Arranjo e fixação em revisão.'
    : ' Quatro bolsas verticais reservadas sob cama; acesso e ancoragem pendentes.';
}
Promise.all([load(data.glb_base64), load(data.interior_glb_base64),
  load(data.roof_stowed_glb_base64), load(data.roof_open_glb_base64), load(data.roof_fixed_glb_base64), load(data.electrical_glb_base64),
  load(data.portable_ground_glb_base64), load(data.portable_storage_glb_base64)]).then(models => {
    [shell, insideModel, stowed, deployed, fixed, electrical, portableGround, portableStorage] = models;
    for(const id of ['portableInstalled','portableDeployed']) document.querySelector('#'+id).disabled = !data.portable_ground_glb_base64;
    eachMaterial(shell, mat => originalOpacity.set(mat, mat.opacity));
    models.forEach(model => scene.add(model)); update();
    note.textContent = 'Carroceria, equipamentos e suportes carregados. Arraste para girar; selecione um equipamento para localizar.';
    document.body.dataset.ready = 'true';
    let count = 0; insideModel.traverse(o => { if(o.isMesh) count++; });
    document.body.dataset.interiorMeshes = String(count);
    let electricalCount = 0; electrical.traverse(o => {if(o.isMesh) electricalCount++;});
    document.body.dataset.electricalMeshes = String(electricalCount);
    let portableCount = 0; portableGround.traverse(o => {if(o.isMesh) portableCount++;});
    portableStorage.traverse(o => {if(o.isMesh) portableCount++;});
    document.body.dataset.portableMeshes = String(portableCount);
  }).catch(err => { note.textContent = 'Falha ao carregar a geometria: '+err.message; });
for(const id of ['inside','hideShell','hideBed','wire','panels','deploy','extensionInstalled','electrical','technical','isolate','portableInstalled','portableDeployed']) {
  document.querySelector('#'+id).addEventListener('change', event => {
    if(id === 'inside' && event.target.checked) document.querySelector('#panels').checked = false;
    if(id === 'hideShell' && event.target.checked) document.querySelector('#inside').checked = true;
    if(id === 'deploy' && event.target.checked) document.querySelector('#extensionInstalled').checked = true;
    if(id === 'extensionInstalled' && !event.target.checked) document.querySelector('#deploy').checked = false;
    if(['extensionInstalled','deploy'].includes(id) && event.target.checked) {
      document.querySelector('#portableInstalled').checked = false;
      document.querySelector('#portableDeployed').checked = false;
    }
    if(['portableInstalled','portableDeployed'].includes(id) && event.target.checked) {
      document.querySelector('#portableInstalled').checked = true;
      document.querySelector('#extensionInstalled').checked = false;
      document.querySelector('#deploy').checked = false;
    }
    if(id === 'portableInstalled' && !event.target.checked) document.querySelector('#portableDeployed').checked = false;
    update();
  });
}
const views = {iso:[6,-7,4.5], side:[-.5,-10,1.3], top:[-.5,-.001,10], front:[10,0,1.3], portable:[6,-10,6]};
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {
  camera.position.set(...views[button.dataset.view]); controls.target.set(-.5,button.dataset.view === 'portable' ? -1.6 : 0,1.2); controls.update();
}));
let selection;
function focusItem(item, globalCoordinates = false) {
  activeItem = item.id;
  document.querySelector('#isolate').checked = item.id === 'hvac';
  document.querySelector('#technical').checked = globalCoordinates && item.mass_in_oem_curb;
  document.querySelector('#electrical').checked = true;
  if(item.optional_extension) document.querySelector('#extensionInstalled').checked = true;
  document.querySelector('#inside').checked = true;
  document.querySelector('#hideShell').checked = true;
  document.querySelector('#panels').checked = false; update();
  document.querySelector('#hideBed').checked = globalCoordinates || ['lava_seca','hvac','agua'].includes(item.id); update();
  const align = globalCoordinates ? data.electrical.alignment_assumed : data.equipment.alignment_assumed;
  const point = new THREE.Vector3(align.rear_x_m+item.position_xyz_m[0]+item.dimensions_xyz_m[0]/2,
    -align.cargo_width_m/2+item.position_xyz_m[1]+item.dimensions_xyz_m[1]/2,
    align.floor_z_m+item.position_xyz_m[2]+item.dimensions_xyz_m[2]/2);
  if(selection) { scene.remove(selection); selection.dispose(); }
  selection = new THREE.Box3Helper(new THREE.Box3().setFromCenterAndSize(point,
    new THREE.Vector3(...item.dimensions_xyz_m)), 0xd87520); scene.add(selection);
  controls.target.copy(point); camera.position.copy(point.clone().add(new THREE.Vector3(2,2.5,1.8)));
  const info = document.querySelector('#itemInfo'); info.replaceChildren();
  const title = document.createElement('strong'); title.textContent = item.label; info.append(title);
  const size = document.createElement('p');
  size.textContent = item.dimensions_xyz_m.map(v => (v*1000).toFixed(0)).join(' × ')+' mm (X/Y/Z) · massa '+(item.mass_kg ?? 'pendente')+' kg'; info.append(size);
  const desc = document.createElement('p'); desc.textContent = item.source_note; info.append(desc);
  if(/^https:\/\//.test(item.source)) {
    const link = document.createElement('a'); link.href = item.source; link.target = '_blank';
    link.rel = 'noopener'; link.textContent = 'Fonte de fabricante'; info.append(link);
  }
  info.scrollIntoView({block:'nearest'});
}
function addItem(item, globalCoordinates) {
  const button = document.createElement('button'); button.textContent = item.label;
  button.dataset.component = item.id; button.addEventListener('click', () => focusItem(item, globalCoordinates));
  document.querySelector('#components').append(button);
}
data.equipment.items.forEach(item => addItem(item, false));
data.electrical.items.forEach(item => addItem(item, true));
function resize() {
  camera.aspect = host.clientWidth/host.clientHeight; camera.updateProjectionMatrix();
  renderer.setSize(host.clientWidth, host.clientHeight);
}
addEventListener('resize', resize); resize();
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
