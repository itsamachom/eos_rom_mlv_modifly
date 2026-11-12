/* Verify catalog coverage and PNG integrity, then exercise the offline gallery. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const http = require('node:http');
const root = path.resolve(__dirname, '..');
(async () => {
  const release = (await fs.readFile(path.join(root, 'scripts/photo-ui-version.txt'), 'utf8')).trim();
  const dir = path.join(root, 'docs/menu-previews', release);
  const m = JSON.parse(await fs.readFile(path.join(dir, 'manifest.json'), 'utf8'));
  assert.equal(m.release, release);
  assert.equal(m.kind, 'production-renderer-host-capture');
  const ids = new Set();
  for (const s of m.screens) {
    assert(!ids.has(s.id)); ids.add(s.id);
    const bytes = await fs.readFile(path.join(dir, s.png));
    assert.equal(bytes.readUInt32BE(16), 720); assert.equal(bytes.readUInt32BE(20), 510);
    assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), s.sha256);
    if (s.label === 'Shutter Count') {
      assert(!s.drawn_ascii.includes('12345')); // Do not borrow the behavioral test's simulated counts.
      if (s.language === 'en') assert(s.drawn_ascii.filter(x => x === 'Unavailable').length === 3);
    }
    if (s.label === 'Version') {
      assert(s.drawn_ascii.includes(release)); assert(s.drawn_ascii.includes('FIRMWARE ADD-ON'));
    }
  }
  const counts = [6, 7, 7, 8, 4, 7, 5];
  for (const lang of ['th', 'en']) {
    for (let c = 0; c < counts.length; c++) {
      for (let item = 0; item < counts[c]; item++) {
        const rows = m.screens.filter(s => s.language === lang && s.category === c && s.item === item);
        assert.equal(rows.filter(s => s.pane === 'item').length, 1);
        const n = rows[0].detail_count;
        assert.equal(rows.filter(s => s.pane === 'options').length, Math.ceil(n / (lang === 'th' ? 3 : 4)));
      }
    }
  }
  const mirror = m.source_registry.find(x => x.name === 'Mirror Lockup');
  assert.deepEqual(mirror.children.map(x => x.name), ['MLU mode', 'Normal MLU Delay']);
  assert(!mirror.children[0].fields.choices.includes('Handheld'));
  const archive = path.join(root, 'docs/menu-previews', `Thai-Menu-${release}-menu-captures.zip`);
  const zip = await fs.readFile(archive);
  const checksum = await fs.readFile(archive + '.sha256', 'utf8');
  assert(checksum.startsWith(crypto.createHash('sha256').update(zip).digest('hex')));
  const server = http.createServer(async (req, res) => {
    try {
      let name = decodeURIComponent(new URL(req.url, 'http://local.test').pathname);
      if (name.endsWith('/')) name += 'index.html';
      const file = path.resolve(root, '.' + name);
      if (!file.startsWith(path.join(root, 'docs') + path.sep)) { res.writeHead(404).end(); return; }
      const types = {'.html': 'text/html; charset=utf-8', '.png': 'image/png', '.json': 'application/json', '.zip': 'application/zip'};
      res.writeHead(200, {'Content-Type': types[path.extname(file)] || 'text/plain; charset=utf-8'}).end(await fs.readFile(file));
    } catch { res.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser = await chromium.launch({executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox']});
    const page = await browser.newPage();
    const requests = [];
    page.on('request', r => { if (/^https?:/.test(r.url()) && !r.url().startsWith(origin + '/')) requests.push(r.url()); });
    for (const width of [1440, 768, 390, 320]) {
      await page.setViewportSize({width, height: 900});
      await page.goto(`${origin}/docs/menu-previews/${release}/`);
      assert.equal(await page.locator('figure img').count(), m.screens.length);
      await page.evaluate(async () => {
        const imgs = [...document.querySelectorAll('figure img')];
        imgs.forEach(img => img.loading = 'eager');
        await Promise.all(imgs.map(img => img.decode()));
      });
      assert.equal(await page.locator('img').evaluateAll(imgs => imgs.every(i => i.naturalWidth === 720 && i.naturalHeight === 510)), true);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      assert.equal(await page.locator('script, iframe').count(), 0);
    }
    await page.locator('nav a[href="#en"]').click(); assert(page.url().endsWith('#en'));
    const imageLink = page.locator('#en figure a').first();
    const popupWait = page.waitForEvent('popup'); await imageLink.click(); const popup = await popupWait;
    await popup.waitForLoadState(); assert(popup.url().endsWith('.png')); assert.equal(await popup.evaluate(() => window.opener), null); await popup.close();
    for (const a of await page.locator('footer a[target="_blank"]').all()) assert((await a.getAttribute('rel')).includes('noopener'));
    assert.equal(requests.length, 0);
  } finally { if (browser) await browser.close(); await new Promise(resolve => server.close(resolve)); }
  console.log(`PASS ${m.screens.length} PNG hashes/dimensions; 44 items in both languages; every option page; current version; no invented shutter counts; removed handheld rows; ZIP SHA256; gallery local/mobile/new-tab links with no third-party requests`);
})().catch(e => { console.error(e); process.exit(1); });
