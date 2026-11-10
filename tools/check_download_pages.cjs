/* Browser checks for choosing and downloading the camera package, separately from source. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const root = path.resolve(__dirname,'..');
(async()=>{
  const version = (await fs.readFile(path.join(root,'scripts/photo-ui-version.txt'),'utf8')).trim();
  const meta = JSON.parse(await fs.readFile(path.join(root,`downloads/${version}/DOWNLOAD_INFO.json`),'utf8'));
  const packages={};
  for(const key of ['first_install','camera']) {
    const item=meta[key];const payload=await fs.readFile(path.join(root,item.path));
    assert.equal(payload.length,item.bytes);
    assert.equal(crypto.createHash('sha256').update(payload).digest('hex'),item.sha256);
    packages[key]={...item,payload,url:`https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/site/eos-600d-bilingual/${item.path}`};
  }
  const cameraURL=packages.camera.url;
  const server = http.createServer(async(req,res)=>{
    try {
      let name = decodeURIComponent(new URL(req.url,'http://local.test').pathname);
      if(name.endsWith('/'))name+='index.html';
      const file = path.resolve(root,'.'+name);
      if(!file.startsWith(path.join(root,'docs')+path.sep)){res.writeHead(404).end();return;}
      const data=await fs.readFile(file);
      res.writeHead(200,{'Content-Type':file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.css')?'text/css; charset=utf-8':'application/octet-stream'}).end(data);
    }catch{res.writeHead(404).end();}
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const origin=`http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
    for(const lang of ['th','en']) {
      const context=await browser.newContext({acceptDownloads:true});
      const page=await context.newPage();
      const failures=[];
      page.on('pageerror',e=>failures.push(e.message));
      page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()}: ${r.url()}`);});
      await page.route('**/*',route=>route.request().url().startsWith(origin+'/')?route.continue():route.abort());
      // Exercise the real link and browser download using the actual verified ZIP.
      // GitHub transport is separately checked against the published URL after upload.
      for(const item of Object.values(packages))await page.route(item.url,route=>route.fulfill({status:200,headers:{'Content-Type':'application/zip','Content-Disposition':`attachment; filename="${item.filename}"`},body:item.payload}));
      const home=origin+(lang==='th'?'/docs/':'/docs/en/');
      await page.goto(home);
      await page.locator('.hero .actions a.primary').click();
      const target=home+'download.html';
      assert.equal(page.url(),target);
      for(const width of [1440,768,390,320]) {
        await page.setViewportSize({width,height:1000});
        assert.equal((await page.goto(target)).status(),200);
        await page.evaluate(()=>document.fonts.ready);
        assert.equal(await page.locator('html').getAttribute('lang'),lang);
        assert.equal(await page.locator('h1').count(),1);
        assert((await page.locator('h1').innerText()).includes(version));
        assert.equal(await page.locator('.download-card').count(),3);
        assert.equal(await page.locator('[data-download="first_install"]').getAttribute('href'),packages.first_install.url);
        assert((await page.locator('#first-install-steps').innerText()).includes('32 GB'));
        assert((await page.locator('#first-install-steps').innerText()).includes('60'));
        for(const url of ['https://www.youtube.com/@Online2easy','https://www.facebook.com/online2easy','https://online2hobby.blogspot.com/'])assert.equal(await page.locator(`footer a[href="${url}"]`).count(),1);
        assert.equal(await page.locator('[data-download="camera"]').getAttribute('href'),cameraURL);
        assert.equal(await page.locator('[data-download="source"]').getAttribute('href'),meta.source.url);
        assert.notEqual(cameraURL,meta.source.url);
        assert((await page.locator('#camera-download').innerText()).includes(meta.camera.filename));
        assert((await page.locator('#source-download').innerText()).includes(meta.source.filename));
        assert((await page.locator('#camera-download .checksum').innerText()).includes(meta.camera.sha256));
        assert((await page.locator('#source-download .checksum').innerText()).includes(meta.source.sha256));
        assert((await page.locator('body').innerText()).includes('1.0.2'));
        assert((await page.locator('body').innerText()).includes('Experimental'));
        assert.equal(await page.locator('form,iframe,script').count(),0);
        assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),`${lang}: download overflow at ${width}`);
        for(const href of await page.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')))) {
          assert(href && href!=='#');
          if(href.startsWith('#'))assert.equal(await page.locator(href).count(),1);
          else if(!href.startsWith('https://'))assert.equal((await context.request.get(new URL(href,target).href)).status(),200);
        }
      }
      await page.goto(target);
      await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'skip');
      await page.keyboard.press('Enter');assert.equal(new URL(page.url()).hash,'#main');
      for(const key of ['first_install','camera']) {
        const item=packages[key];
        const [download]=await Promise.all([page.waitForEvent('download'),page.locator(`[data-download="${key}"]`).click()]);
        assert.equal(download.suggestedFilename(),item.filename);
        assert.equal(crypto.createHash('sha256').update(await fs.readFile(await download.path())).digest('hex'),item.sha256);
        await download.delete();
      }
      await page.locator('a.language').click();
      assert.equal(await page.locator('html').getAttribute('lang'),lang==='th'?'en':'th');
      assert.equal(path.basename(new URL(page.url()).pathname),'download.html');
      assert.deepEqual(failures,[]);
      await context.close();
      console.log(`PASS ${lang}: homepage to downloads, 4 widths, separate first-install/update/source links and hashes, keyboard/language navigation, both actual camera ZIP browser downloads and developer links`);
    }
  }finally{
    if(browser)await browser.close();
    await new Promise(r=>server.close(r));
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
