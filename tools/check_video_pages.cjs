/* Video-library flow: local cover, no third-party load, correct external tabs and language routes. */
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
  const data=JSON.parse(await fs.readFile(path.join(root,'website-content/videos.json'),'utf8'));
  const featured=data.videos.find(v=>v.id===data.featured);
  const video=`https://www.youtube.com/watch?v=${featured.youtube_id}`;
  const server=http.createServer(async(req,res)=>{
    try{
      let name=decodeURIComponent(new URL(req.url,'http://local.test').pathname);if(name.endsWith('/'))name+='index.html';
      const file=path.resolve(root,'.'+name);if(!file.startsWith(path.join(root,'docs')+path.sep)){res.writeHead(404).end();return;}
      const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.jpg':'image/jpeg'};
      res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'}).end(await fs.readFile(file));
    }catch{res.writeHead(404).end();}
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const origin=`http://127.0.0.1:${server.address().port}`;
  let browser;
  try{
    browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
    for(const lang of ['th','en']){
      const context=await browser.newContext();const page=await context.newPage();const failures=[];const external=[];
      page.on('pageerror',e=>failures.push(e.message));
      page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()}: ${r.url()}`);});
      page.on('request',r=>{if(!r.url().startsWith(origin+'/'))external.push(r.url());});
      await page.route('**/*',r=>r.request().url().startsWith(origin+'/')?r.continue():r.abort());
      const home=origin+(lang==='th'?'/docs/':'/docs/en/');const target=home+'videos.html';
      await page.goto(home);await page.locator('#video-guide a[href="videos.html"]').click();assert.equal(page.url(),target);
      for(const width of [1440,1024,768,390,320]){
        await page.setViewportSize({width,height:1000});assert.equal((await page.goto(target)).status(),200);
        await page.evaluate(()=>document.fonts.ready);
        assert.equal(await page.locator('html').getAttribute('lang'),lang);assert.equal(await page.locator('h1').count(),1);
        assert.equal(await page.locator('iframe,script,form').count(),0);
        assert.equal(await page.locator('[data-video="watch"]').getAttribute('href'),video);
        assert.equal(await page.locator('[data-video="playlist"]').getAttribute('href'),data.playlist_url);
        for(const selector of ['[data-video="watch"]','[data-video="playlist"]','[data-video="featured"]']){
          const a=page.locator(selector);assert.equal(await a.getAttribute('target'),'_blank');assert((await a.getAttribute('rel')).includes('noopener'));
        }
        await page.locator('.lesson-poster img').evaluate(i=>i.decode());
        assert.deepEqual(await page.locator('.lesson-poster img').evaluate(i=>[i.naturalWidth,i.naturalHeight]),[960,540]);
        for(const href of await page.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')))){
          assert(href && href!=='#');
          if(href.startsWith('#'))assert.equal(await page.locator(href).count(),1);
          else if(!href.startsWith('https://'))assert.equal((await context.request.get(new URL(href,target).href)).status(),200,href);
          assert(!/paypal|buymeacoffee|stripe|promptpay|github.com\/sponsors/.test(href),'Unrequested funding link');
        }
        for(const url of ['https://www.youtube.com/@Online2easy','https://www.facebook.com/online2easy','https://online2hobby.blogspot.com/'])assert.equal(await page.locator(`footer a[href="${url}"]`).count(),1);
        assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),`${lang}: video overflow ${width}`);
        if(process.env.VIDEO_PROOF_OUT && [1440,390].includes(width)){
          await fs.mkdir(process.env.VIDEO_PROOF_OUT,{recursive:true});
          await page.screenshot({path:path.join(process.env.VIDEO_PROOF_OUT,`videos-${lang}-${width}.png`),fullPage:true});
        }
      }
      assert.deepEqual(external,[],'Video page loaded an external resource before a click');
      await page.goto(target);await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'skip');
      await page.keyboard.press('Enter');assert.equal(new URL(page.url()).hash,'#main');
      for(const [selector,url] of [['[data-video="watch"]',video],['[data-video="playlist"]',data.playlist_url]]){
        await context.route(url,r=>r.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>YouTube navigation fixture</title><p>External destination</p>'}));
        const before=page.url();const [popup]=await Promise.all([context.waitForEvent('page'),page.locator(selector).click()]);
        await popup.waitForLoadState('domcontentloaded');assert.equal(popup.url(),url);assert.equal(page.url(),before);assert.equal(await popup.evaluate(()=>window.opener===null),true);await popup.close();
      }
      await page.locator('a.language').click();assert.equal(await page.locator('html').getAttribute('lang'),lang==='th'?'en':'th');
      assert.equal(path.basename(new URL(page.url()).pathname),'videos.html');
      await page.goto(home+'download.html');assert.equal(await page.locator('.video-callout a[href="videos.html#installation"]').count(),1);
      await page.locator('.video-callout a[href="videos.html#installation"]').click();assert.equal(new URL(page.url()).hash,'#installation');
      assert.deepEqual(failures,[]);await context.close();
      console.log(`PASS ${lang}: home/download to video guides, 5 widths, local poster/no embeds or initial third-party requests, exact YouTube and playlist tabs, keyboard/language navigation`);
    }
  }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
