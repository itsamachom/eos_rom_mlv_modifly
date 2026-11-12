/* Validate the Thai manual's browser layout and export a printable, tagged PDF. */
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const release=(await fs.readFile(path.join(root,'scripts/photo-ui-version.txt'),'utf8')).trim();
 const server=http.createServer(async(req,res)=>{
  try{
   let name=decodeURIComponent(new URL(req.url,'http://local.test').pathname);if(name.endsWith('/'))name+='index.html';
   const file=path.resolve(root,'docs','.'+name);
   if(!file.startsWith(path.join(root,'docs')+path.sep)){res.writeHead(404).end();return;}
   const types={'.html':'text/html; charset=utf-8','.css':'text/css','.ttf':'font/ttf','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.pdf':'application/pdf'};
   res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'}).end(await fs.readFile(file));
  }catch{res.writeHead(404).end();}
 });
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
 let browser;
 try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
  const page=await browser.newPage();const failures=[];const remote=[];
  page.on('pageerror',e=>failures.push(e.message));
  page.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()} ${r.url()}`);});
  page.on('request',r=>{if(!r.url().startsWith(origin+'/'))remote.push(r.url());});
  for(const width of [1440,1024,768,390,320]){
   await page.setViewportSize({width,height:900});await page.goto(origin+'/manual-th.html');await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('.menu-entry').count(),44);
   assert.equal(await page.locator('.menu-group').count(),7);
   assert.equal(await page.locator('article dt').count(),116);
   assert.equal(await page.locator('html').getAttribute('lang'),'th');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1), JSON.stringify(await page.evaluate(()=>({width:innerWidth,scrollX:scrollX,total:document.documentElement.scrollWidth,wide:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right+scrollX>innerWidth+1).slice(0,5).map(e=>[e.tagName,e.className,e.textContent.slice(0,80)])}))));
   assert(await page.evaluate(()=>document.fonts.check('18px ManualThai','คู่มือภาษาไทย')));
   assert.equal(await page.locator('script,iframe,form').count(),0);
   for(const id of await page.locator('.toc a[href^="#"]').evaluateAll(links=>links.map(a=>a.hash.slice(1)))){
    assert.equal(await page.locator(`[id="${id}"]`).count(),1);
   }
  }
  // Both the menu heading and an individual deep link must work with a keyboard/click.
  await page.locator('.toc a[href="#setup"]').click();assert(page.url().endsWith('#setup'));
  await page.locator('.toc a[href="#setup-7"]').click();assert(page.url().endsWith('#setup-7'));
  assert((await page.locator('#setup-7').innerText()).includes('ไม่ใช่จำนวนไฟล์ภาพ'));
  for(const a of await page.locator('footer a').all()){
   assert.equal(await a.getAttribute('target'),'_blank');assert((await a.getAttribute('rel')).includes('noopener'));
  }
  for(const a of await page.locator('.references a[href^="https://itsamachom.github.io/"]').all()){
   const link=new URL(await a.getAttribute('href'));const local=path.join(root,'docs',link.pathname.replace('/eos_rom_mlv_modifly/',''));
   await fs.access(local);
  }
  for(const name of ['/','/download.html','/videos.html']){
   for(const width of [1440,1024,768,390,320]){
    await page.setViewportSize({width,height:900});await page.goto(origin+name);
    assert.equal(await page.locator('header a[href="manual-th.html"]').count(),1);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   }
  }
  assert.deepEqual(failures,[]);assert.deepEqual(remote,[]);
  await page.goto(origin+'/manual-th.html');await page.evaluate(()=>document.fonts.ready);
  await page.emulateMedia({media:'print'});
  const out=path.join(root,'docs/manual',`Thai-Menu-${release}-Manual-TH.pdf`);await fs.mkdir(path.dirname(out),{recursive:true});
  await page.pdf({path:out,format:'A4',preferCSSPageSize:true,printBackground:false,tagged:true,outline:true,displayHeaderFooter:true,
   headerTemplate:'<span></span>',footerTemplate:`<div style="font-size:9px;color:#555;width:100%;text-align:center;font-family:Arial">Thai-Menu ${release} | Thai user manual | <span class="pageNumber"></span> / <span class="totalPages"></span></div>`});
  const bytes=await fs.readFile(out);assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
  if(process.env.MANUAL_PREVIEW_OUT){
   await page.emulateMedia({media:'screen'});await page.setViewportSize({width:1100,height:900});await page.goto(origin+'/manual-th.html#shoot-4');
   await page.screenshot({path:process.env.MANUAL_PREVIEW_OUT});
  }
  console.log('PASS 44 menu entries / 116 child explanations, 5 widths, Thai font, TOC/deep links, screenshots, creator tabs and entry-point navigation; PDF exported: '+out);
 }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exit(1);});
