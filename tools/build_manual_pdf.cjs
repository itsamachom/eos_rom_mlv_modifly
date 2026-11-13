/* Validate the Thai manual's browser layout and export a printable, tagged PDF. */
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const release=(await fs.readFile(path.join(root,'scripts/photo-ui-version.txt'),'utf8')).trim();
 const catalog=JSON.parse(await fs.readFile(path.join(root,'docs/menu-previews',release,'manifest.json'),'utf8'));
 const captures=new Map(catalog.screens.map(s=>[s.id,s]));
 const manual=JSON.parse(await fs.readFile(path.join(root,'website-content/manual-th.json'),'utf8'));
 const explanations=new Map(manual.items.map(e=>[e.key,e]));
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
   await page.setViewportSize({width,height:900});await page.goto(origin+'/manual-th.html');await page.evaluate(async()=>{await document.fonts.load('11pt ManualThai','คู่มือภาษาไทย');await document.fonts.ready;});
   assert.equal(await page.locator('.menu-entry').count(),44);
   assert.equal(await page.locator('.menu-group').count(),7);
   assert.equal(await page.locator('article dt').count(),116);
   assert.equal(await page.locator('article.menu-entry table.menu-table').count(),44);
   assert.equal(await page.locator('tr.overview-row .menu-image-link').count(),44);
   await page.locator('.menu-table img').evaluateAll(async imgs=>{
    imgs.forEach(img=>img.loading='eager');await Promise.all(imgs.map(img=>img.decode()));
   });
   assert(await page.locator('.menu-table img').evaluateAll(imgs=>imgs.every(img=>img.naturalWidth===720&&img.naturalHeight===510&&img.getBoundingClientRect().width<=221)));
   const rows=await page.locator('.menu-table tbody tr').evaluateAll(rows=>rows.map(row=>({
    id:row.dataset.capture,key:row.closest('article').dataset.menuKey,
    keys:[...row.querySelectorAll('dt')].map(dt=>dt.dataset.optionKey),
    src:row.querySelector('img').getAttribute('src'),href:row.querySelector('a').href,
    target:row.querySelector('a').target,rel:row.querySelector('a').rel,
    note:row.querySelector('.capture-note')?.textContent||''
   })));
   for(const row of rows){
    const capture=captures.get(row.id);assert(capture);assert.equal(capture.label,row.key);
    assert.equal(row.src,`menu-previews/${release}/${capture.png}`);
    assert.equal(row.href,'https://itsamachom.github.io/eos_rom_mlv_modifly/'+row.src);
    assert.equal(row.target,'_blank');assert(row.rel.includes('noopener'));
    const entry=explanations.get(row.key);const keys=Object.keys(entry.options);
    for(const key of row.keys){
     if(capture.pane==='options'){
      const offset=capture.detail_count-keys.length;assert(offset===0||offset===1);
      assert.equal(Math.floor((keys.indexOf(key)+offset)/3)+1,capture.option_page);
     }else assert(row.note.includes('ยังไม่โหลดโมดูล'));
    }
   }
   // Desktop pairs image/text; narrow screens stack each row without enlarging images.
   const positions=await page.locator('#shoot-1 .overview-row').evaluate(row=>{
    const image=row.querySelector('.image-cell').getBoundingClientRect();const text=row.querySelector('.explanation-cell').getBoundingClientRect();
    return {imageX:image.x,imageBottom:image.bottom,textX:text.x,textY:text.y};
   });
   if(width>700)assert(positions.textX>positions.imageX+100);else assert(positions.textY>=positions.imageBottom-1);
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
  // Fulfill the full-size image locally: verify popup behavior without external network access.
  await page.context().route('https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/**',async route=>{
   const pathname=new URL(route.request().url()).pathname.replace('/eos_rom_mlv_modifly/','');
   await route.fulfill({contentType:'image/png',body:await fs.readFile(path.join(root,'docs',pathname))});
  });
  const fullImage=page.locator('#setup-7 .menu-image-link').first();const destination=await fullImage.getAttribute('href');
  const popupWait=page.waitForEvent('popup');await fullImage.click();const popup=await popupWait;await popup.waitForLoadState();
  assert.equal(popup.url(),destination);assert.equal(await popup.evaluate(()=>window.opener),null);await popup.close();
  for(const a of await page.locator('footer a').all()){
   assert.equal(await a.getAttribute('target'),'_blank');assert((await a.getAttribute('rel')).includes('noopener'));
  }
  for(const a of await page.locator('.references a[href^="https://itsamachom.github.io/"]').all()){
   const link=new URL(await a.getAttribute('href'));const local=path.join(root,'docs',link.pathname.replace('/eos_rom_mlv_modifly/',''));
   await fs.access(local);
  }
  const referenceStyles=new Map();
  for(const name of ['/','/download.html','/videos.html','/manual-th.html']){
   for(const width of [1440,1024,768,390,320]){
    await page.setViewportSize({width,height:900});await page.goto(origin+name);
    assert.equal(await page.locator('header a[href="manual-th.html"]').count(),1);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    const menu=await page.locator('header nav a').allTextContents();
    assert.equal(menu.indexOf('คู่มือภาษาไทย'),menu.indexOf('วิดีโอ')+1);
    const typography=await page.evaluate(()=>{
     const body=getComputedStyle(document.body),nav=getComputedStyle(document.querySelector('header nav')),
      link=getComputedStyle(document.querySelector('header nav a')),brand=getComputedStyle(document.querySelector('.brand'));
     return {family:body.fontFamily,size:body.fontSize,line:body.lineHeight,navSize:nav.fontSize,navLine:nav.lineHeight,linkColor:link.color,brandSize:brand.fontSize};
    });
    if(name==='/')referenceStyles.set(width,typography);
    if(name==='/manual-th.html'){
     assert.deepEqual(typography,referenceStyles.get(width));
     assert.equal(await page.locator('header.top .brand .mark').count(),1);
     for(const href of await page.locator('header nav a').evaluateAll(links=>links.map(a=>a.getAttribute('href'))))assert(!href.startsWith('#'));
    }
   }
  }
  assert.deepEqual(failures,[]);assert.deepEqual(remote,[]);
  await page.goto(origin+'/manual-th.html');await page.evaluate(async()=>{await document.fonts.load('11pt ManualThai','คู่มือภาษาไทย');await document.fonts.ready;});
  await page.locator('.menu-table img').evaluateAll(async imgs=>{
   imgs.forEach(img=>img.loading='eager');await Promise.all(imgs.map(img=>img.decode()));
  });
  await page.emulateMedia({media:'print'});
  const out=path.join(root,'docs/manual',`Thai-Menu-${release}-Manual-TH.pdf`);await fs.mkdir(path.dirname(out),{recursive:true});
  if(!process.env.MANUAL_SKIP_PDF)await page.pdf({path:out,format:'A4',preferCSSPageSize:true,printBackground:false,tagged:true,outline:true,displayHeaderFooter:true,
   headerTemplate:'<span></span>',footerTemplate:`<div style="font-size:9px;color:#555;width:100%;text-align:center;font-family:Arial">Thai-Menu ${release} | Thai user manual | <span class="pageNumber"></span> / <span class="totalPages"></span></div>`});
  const bytes=await fs.readFile(out);assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
  if(process.env.MANUAL_PREVIEW_OUT){
   await page.emulateMedia({media:'screen'});await page.setViewportSize({width:1100,height:900});await page.goto(origin+'/manual-th.html');
   await page.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';document.getElementById('shoot-4').scrollIntoView();});
   await page.screenshot({path:process.env.MANUAL_PREVIEW_OUT});
  }
  console.log('PASS 44 illustrated tables / 116 child explanations, exact capture-page mapping, image decode/new-tab enlargement, 5 widths, Thai font, TOC/deep links, creator tabs and entry-point navigation; illustrated PDF '+(process.env.MANUAL_SKIP_PDF?'preserved: ':'exported: ')+out);
 }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exit(1);});
