// Uso: CHROMIUM_BIN=/caminho/chromium node verificar.cjs ARQUIVO.html DESTINO
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');

(async () => {
  if(process.argv.length !== 4) throw new Error('Forneça HTML e diretório novo de QA');
  const dest = path.resolve(process.argv[3]);
  fs.mkdirSync(dest, {recursive: false});
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_BIN || undefined,
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle',
      '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
  });
  try {
    const page = await browser.newPage({viewport: {width:1440,height:1000}});
    const errors = [], requests = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('request', r => { if(/^https?:/.test(r.url())) requests.push(r.url()); });
    await page.goto(pathToFileURL(path.resolve(process.argv[2])).href);
    await page.waitForFunction(() => document.body.dataset.ready === 'true', {timeout:30000});
    await page.waitForTimeout(300);
    await page.screenshot({path:path.join(dest, 'exterior.png')});
    await page.getByRole('button', {name:'Superior',exact:true}).click();
    await page.waitForTimeout(400);
    await page.screenshot({path:path.join(dest, 'solar_recolhido.png')});
    await page.check('#extensionInstalled');
    await page.waitForTimeout(300);
    await page.screenshot({path:path.join(dest, 'solar_empilhado.png')});
    await page.check('#deploy');
    await page.waitForTimeout(400);
    await page.screenshot({path:path.join(dest, 'solar_aberto.png')});
    await page.check('#inside');
    await page.check('#hideShell');
    await page.getByRole('button', {name:'Superior',exact:true}).click();
    await page.waitForTimeout(400);
    await page.screenshot({path:path.join(dest, 'interior.png')});
    await page.locator('[data-component="geladeira"]').click();
    await page.locator('[data-component="lava_seca"]').click();
    await page.waitForTimeout(400);
    await page.screenshot({path:path.join(dest, 'lava_seca.png')});
    await page.check('#wire'); await page.uncheck('#panels');
    const result = {ready:true,errors,external_requests:requests,canvas_count:await page.locator('canvas').count(),
      components:await page.locator('[data-component]').count(), interior_meshes:await page.evaluate(() => +document.body.dataset.interiorMeshes),
      focused_item:await page.locator('#itemInfo strong').innerText()};
    fs.writeFileSync(path.join(dest,'qa.json'),JSON.stringify(result,null,2));
    console.log(JSON.stringify(result));
    if(errors.length || requests.length || result.canvas_count !== 1 || result.components !== 7 || result.interior_meshes < 80 || !result.focused_item.includes('LG')) process.exitCode = 1;
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode=1;});
