/* Functional smoke checks for the static, bilingual project-site draft. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml'};
(async () => {
  const server = http.createServer(async (req,res) => {
    try {
      let pathname = decodeURIComponent(new URL(req.url,'http://local.test').pathname);
      if (pathname.endsWith('/')) pathname += 'index.html';
      const file = path.resolve(root, '.' + pathname);
      if (!file.startsWith(path.join(root,'docs')+path.sep)) {res.writeHead(404).end();return;}
      const data = await fs.readFile(file);
      res.writeHead(200,{'Content-Type':types[path.extname(file)] || 'application/octet-stream'}).end(data);
    } catch { res.writeHead(404).end(); }
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser = await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
    const out = path.join(root,'previews');await fs.mkdir(out,{recursive:true});
    for (const lang of ['th','en']) {
      const context = await browser.newContext();
      const page = await context.newPage();
      const failures = [];
      page.on('pageerror',e=>failures.push(e.message));
      page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()}: ${r.url()}`);});
      await page.route('**/*',route=>route.request().url().startsWith(origin+'/') ? route.continue() : route.abort());
      const target = origin + (lang==='th' ? '/docs/' : '/docs/en/');
      for (const width of [1440,768,390,320]) {
        await page.setViewportSize({width,height:1000});
        assert.equal((await page.goto(target)).status(),200);
        await page.evaluate(()=>document.fonts.ready);
        assert.equal(await page.locator('html').getAttribute('lang'),lang);
        assert.equal(await page.locator('h1').count(),1);
        assert.equal(await page.locator('form,iframe,script').count(),0);
        assert(await page.locator('#status').innerText().then(t=>t.includes('28') && t.includes('38') && t.includes('dietlibc')));
        const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
        assert(!overflow,`${lang}: horizontal overflow at ${width}px`);
        const links=await page.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));
        for(const href of links) {
          assert(href && href!=='#','Empty/placeholder link');
          if(href.startsWith('#'))assert.equal(await page.locator(href).count(),1,href);
          else if(!href.startsWith('https://')) {
            const r=await context.request.get(new URL(href,target).href);assert.equal(r.status(),200,href);
          }
          assert(!/paypal|buymeacoffee|stripe|promptpay/i.test(href),'Payment link added while support is closed');
        }
        if(width===1440 && lang==='th') {
          const box=await page.locator('#story').boundingBox();
          await page.screenshot({path:path.join(out,'website-th-story.png'),clip:{x:box.x-16,y:box.y,width:box.width+32,height:box.height}});
        }
        if(width===1440 || (width===390 && lang==='th'))await page.screenshot({path:path.join(out,`website-${lang}-${width===1440?'desktop':'mobile'}.png`),fullPage:true});
      }
      await page.goto(target);
      await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'skip');
      await page.keyboard.press('Enter');assert(new URL(page.url()).hash==='#main');
      await page.locator('details summary').first().click();assert(await page.locator('details').first().getAttribute('open')!==null);
      await page.locator('a.language').click();assert.equal(await page.locator('html').getAttribute('lang'),lang==='th'?'en':'th');
      assert.deepEqual(failures,[]);
      await context.close();
      console.log(`PASS ${lang}: mobile/tablet/desktop layout, local links, language switch, keyboard skip link, FAQ, no payment/form/tracker`);
    }
  } finally {
    if(browser)await browser.close();
    await new Promise(r=>server.close(r));
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
