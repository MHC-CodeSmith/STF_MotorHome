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
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
host.append(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(-.5, 0, 1.2);
controls.enableDamping = true;
controls.listenToKeyEvents(window);
scene.add(new THREE.HemisphereLight(0xffffff, 0x62676c, 2.3));
const sun = new THREE.DirectionalLight(0xffffff, 2.7);
sun.position.set(3, -4, 8); scene.add(sun);
const back = new THREE.DirectionalLight(0xc9e4ff, 1.8);
back.position.set(-5, 4, 4); scene.add(back);
const grid = new THREE.GridHelper(12, 24, '#7c8a96', '#c4ccd2');
grid.rotation.x = Math.PI/2; grid.position.z = -.02; scene.add(grid);

let shell;
const originalOpacity = new Map();
const volumes = new THREE.Group();
volumes.visible = false;
scene.add(volumes);
const colors = [0x83bb6b, 0xe5a35e, 0x74aeb8, 0xae8dce];
const alignment = data.layout_alignment_assumed;
data.layout.floor_zones.forEach((z, i) => {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(z.length_m, z.width_m, z.height_m),
    new THREE.MeshStandardMaterial({ color: colors[i], transparent: true, opacity: .8 }));
  mesh.position.set(alignment.rear_x_m+z.x_m+z.length_m/2,
    -data.layout.cargo_m[1]/2+z.y_m+z.width_m/2, alignment.floor_z_m+z.height_m/2);
  mesh.name = z.label; volumes.add(mesh);
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry),
    new THREE.LineBasicMaterial({color: 0x334455}));
  edges.position.copy(mesh.position); volumes.add(edges);
});
const panels = new THREE.Group(); scene.add(panels);
const roof = data.layout.roof;
for(let i=0; i<roof.modules; i++) {
  const module = new THREE.Mesh(new THREE.BoxGeometry(roof.module_length_x_m,
    roof.module_width_y_m, roof.module_thickness_m),
    new THREE.MeshStandardMaterial({color: 0x143d63, roughness: .35, metalness: .3}));
  module.position.set(alignment.rear_x_m+roof.start_x_m+i*(roof.module_length_x_m+roof.gap_m)+roof.module_length_x_m/2,
    0, 2.612+roof.support_height_m+roof.module_thickness_m/2);
  panels.add(module);
  const border = new THREE.LineSegments(new THREE.EdgesGeometry(module.geometry), new THREE.LineBasicMaterial({color: 0xc2cbd2}));
  border.position.copy(module.position); panels.add(border);
  for(let j=1; j<6; j++) {
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(module.position.x-roof.module_length_x_m/2, -roof.module_width_y_m/2+j*roof.module_width_y_m/6, module.position.z+.016),
      new THREE.Vector3(module.position.x+roof.module_length_x_m/2, -roof.module_width_y_m/2+j*roof.module_width_y_m/6, module.position.z+.016)]),
      new THREE.LineBasicMaterial({color: 0x92afc3}));
    panels.add(line);
  }
}
const bytes = Uint8Array.from(atob(data.glb_base64), c => c.charCodeAt(0));
new GLTFLoader().parse(bytes.buffer, '', gltf => {
  shell = gltf.scene;
  shell.traverse(obj => {
    if(!obj.isMesh) return;
    const mats = (Array.isArray(obj.material) ? obj.material : [obj.material]).map(mat => {
      const copy = mat.clone(); originalOpacity.set(copy, copy.opacity); return copy;
    });
    obj.material = Array.isArray(obj.material) ? mats : mats[0];
  });
  scene.add(shell);
  note.textContent = 'Carroceria detalhada carregada · arraste para girar · roda para aproximar';
  document.body.dataset.ready = 'true';
}, err => { note.textContent = 'Falha ao carregar a geometria: '+err.message; });

function materials(callback) {
  shell?.traverse(obj => {
    if(obj.isMesh) (Array.isArray(obj.material) ? obj.material : [obj.material]).forEach(callback);
  });
}
document.querySelector('#inside').addEventListener('change', event => {
  volumes.visible = event.target.checked;
  if(event.target.checked) { panels.visible = false; document.querySelector('#panels').checked = false; }
  materials(mat => { mat.opacity = event.target.checked ? .16 : originalOpacity.get(mat); mat.transparent = mat.opacity < 1; mat.depthWrite = !event.target.checked; });
});
document.querySelector('#wire').addEventListener('change', event => materials(mat => mat.wireframe = event.target.checked));
document.querySelector('#panels').addEventListener('change', event => panels.visible = event.target.checked);
const views = {iso: [6,-7,4.5], side: [-.5,-10,1.3], top: [-.5,-.001,10], front: [10,0,1.3]};
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {
  camera.position.set(...views[button.dataset.view]); controls.target.set(-.5,0,1.2); controls.update();
}));
function resize() {
  camera.aspect = host.clientWidth/host.clientHeight; camera.updateProjectionMatrix();
  renderer.setSize(host.clientWidth, host.clientHeight);
}
addEventListener('resize', resize); resize();
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
