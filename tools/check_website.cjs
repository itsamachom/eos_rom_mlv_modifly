/* Functional smoke checks for the static, bilingual project-site draft. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.jpg':'image/jpeg'};
(async () => {
  const currentVersion=(await fs.readFile(path.join(root,"scripts/photo-ui-version.txt"),"utf8")).trim();
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
      for (const width of [1920,1440,1024,768,390,320]) {
        await page.setViewportSize({width,height:1000});
        assert.equal((await page.goto(target)).status(),200);
        await page.evaluate(()=>document.fonts.ready);
        assert.equal(await page.locator('html').getAttribute('lang'),lang);
        assert.equal(await page.locator('h1').count(),1);
          for(const url of ['https://www.youtube.com/@Online2easy','https://www.facebook.com/online2easy','https://online2hobby.blogspot.com/']){const a=page.locator(`footer a[href="${url}"]`);assert.equal(await a.count(),1);assert.equal(await a.getAttribute('target'),'_blank');assert((await a.getAttribute('rel')).includes('noopener'));}
        assert.equal(await page.locator('form,iframe,script').count(),0);
        assert.deepEqual(await page.locator('#creator .creator-channel').evaluateAll(as=>as.map(a=>a.href)),[
          'https://www.youtube.com/@Online2easy',
          'https://www.facebook.com/online2easy',
          'https://online2hobby.blogspot.com/'
        ]);
        assert.equal(await page.locator('.hero-photo img').getAttribute('src'),`${lang==='th'?'assets/':'../assets/'}menu-photos/shoot-${lang}.jpg`);
        assert.equal(await page.locator('.device').count(),0,'Concept illustration still present');
        assert.equal(await page.locator('#gallery .photo-grid').count(),3);
        assert.equal(await page.locator('#gallery img').count(),6);
        assert.equal(new Set(await page.locator('#gallery img').evaluateAll(is=>is.map(i=>i.src))).size,6);
        for(const img of await page.locator('.hero-photo img, #gallery img').all()) {
          assert(await img.getAttribute('alt'));
          await img.scrollIntoViewIfNeeded();
          await img.evaluate(i=>i.decode());
          assert.deepEqual(await img.evaluate(i=>[i.naturalWidth,i.naturalHeight]),[2000,1268]);
          assert.equal(await img.evaluate(i=>i.closest('a')===null),true,'Photo still opens a larger image');
          const size=await img.boundingBox();
          assert(size.width<=520.5,`${lang}: photo exceeds its 520px frame at ${width}px`);
          assert(Math.abs(size.height/size.width-1268/2000)<0.01,'Photo proportions changed');
        }
        assert.equal(await page.locator('a[href$=".jpg"]').count(),0,'A full-size photo link remains');
        if(width>=1024)assert((await page.locator('.hero-copy').boundingBox()).width>=350,'Hero image squeezed the text column');
        assert((await page.locator('link[rel="stylesheet"]').getAttribute('href')).includes('?v='),'CSS version missing');
        assert(await page.locator('#status').innerText().then(t=>t.includes(currentVersion) && t.includes('39') && t.includes('dietlibc')));
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
          await page.locator('#story').screenshot({path:path.join(out,'website-th-story.png')});
        }
        if(width===1440) {
          await page.locator('#creator').screenshot({path:path.join(out,`website-${lang}-creator.png`)});
          await page.locator('#gallery').screenshot({path:path.join(out,`website-${lang}-gallery.png`)});
        }
        if(width===390 && lang==='th')await page.locator('.hero').screenshot({path:path.join(out,'website-th-hero-mobile.png')});
        if(width===1440 || (width===390 && lang==='th'))await page.screenshot({path:path.join(out,`website-${lang}-${width===1440?'desktop':'mobile'}.png`),fullPage:true});
      }
      await page.goto(target);
      for(const url of ['https://www.youtube.com/@Online2easy','https://www.facebook.com/online2easy','https://online2hobby.blogspot.com/']) {
        await context.route(url,route=>route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>External profile fixture</title><p>Profile</p>'}));
        const before=page.url();
        const [popup]=await Promise.all([context.waitForEvent('page'),page.locator(`#creator a[href="${url}"]`).click()]);
        await popup.waitForLoadState('domcontentloaded');
        assert.equal(page.url(),before,'Creator link replaced the project page');
        assert.equal(await popup.evaluate(()=>window.opener===null),true);
        await popup.close();
      }
      await page.goto(target);
      await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'skip');
      await page.keyboard.press('Enter');assert(new URL(page.url()).hash==='#main');
      await page.locator('details summary').first().click();assert(await page.locator('details').first().getAttribute('open')!==null);
      await page.locator('a.language').click();assert.equal(await page.locator('html').getAttribute('lang'),lang==='th'?'en':'th');
      // Follow the journal as a reader would, then check each article's
      // responsive layout, navigation and corresponding translation.
      await page.goto(target);
      const articlePaths=await page.locator('#journal .journal-card > a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));
      assert.equal(articlePaths.length,2);
      for(const articlePath of articlePaths) {
        const articleURL=new URL(articlePath,target).href;
        for(const width of [1440,768,390,320]) {
          await page.setViewportSize({width,height:1000});
          assert.equal((await page.goto(articleURL)).status(),200);
          await page.evaluate(()=>document.fonts.ready);
          assert.equal(await page.locator('html').getAttribute('lang'),lang);
          assert.equal(await page.locator('h1').count(),1);
          for(const url of ['https://www.youtube.com/@Online2easy','https://www.facebook.com/online2easy','https://online2hobby.blogspot.com/']){const a=page.locator(`footer a[href="${url}"]`);assert.equal(await a.count(),1);assert.equal(await a.getAttribute('target'),'_blank');assert((await a.getAttribute('rel')).includes('noopener'));}
          assert.equal(await page.locator('article .article-body h2').count()>=4,true);
          assert.equal(await page.locator('form,iframe,script').count(),0);
          assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),`${articlePath}: overflow at ${width}px`);
          assert.equal(await page.locator('time').getAttribute('datetime'),'2026-11-05');
          const articleLinks=await page.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));
          for(const href of articleLinks) {
            assert(href && href!=='#');
            assert(!/paypal|buymeacoffee|stripe|promptpay/i.test(href));
            if(href.startsWith('#'))assert.equal(await page.locator(href).count(),1,href);
            else if(!href.startsWith('https://'))assert.equal((await context.request.get(new URL(href,articleURL).href)).status(),200,href);
          }
          const slug=path.basename(articlePath,'.html');
          if(width===1440 || (width===390 && lang==='th')) {
            const file=`article-${slug}-${lang}-${width===1440?'desktop':'mobile'}.png`;
            await page.screenshot({path:path.join(out,file),fullPage:true});
          }
          if(slug==='inspiration' && ((lang==='th' && width===390)||(lang==='en' && width===1440)))await page.screenshot({path:path.join(out,`article-${lang}-first-screen.png`)});
        }
        await page.goto(articleURL);
        await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'skip');
        await page.keyboard.press('Enter');assert(new URL(page.url()).hash==='#main');
        await page.locator('a.language').click();
        assert.equal(await page.locator('html').getAttribute('lang'),lang==='th'?'en':'th');
        assert.equal(path.basename(new URL(page.url()).pathname),path.basename(articlePath),'Language switch lost the article');
      }
      assert.deepEqual(failures,[]);
      await context.close();
      console.log(`PASS ${lang}: homepage + two articles, 4 viewport widths, local links, matching translation, keyboard navigation, FAQ, no payment/form/tracker`);
    }
  } finally {
    if(browser)await browser.close();
    await new Promise(r=>server.close(r));
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
