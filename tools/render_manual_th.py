"""Render the Thai user manual from reviewed explanations and current menu labels.

This renders documentation only; it never changes the firmware or release ZIPs.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://itsamachom.github.io/eos_rom_mlv_modifly/'
data = json.loads((ROOT / 'website-content/manual-th.json').read_text())
lex = json.loads((ROOT / 'translations/photo_th.json').read_text())
release = (ROOT / 'scripts/photo-ui-version.txt').read_text().strip()
assert data['release'] == release, 'Review the manual for the new release before regenerating'
front = (ROOT / 'firmware/src/photo-menu-600d.h').read_text()
pages = []
for m in re.finditer(r'static const struct photo_item (\w+)\[\] = \{(.*?)\n\};', front, re.S):
    pages.append([(r[1], r[2], r[4]) for r in re.finditer(r'\{"([^"]+)", "([^"]+)", ("([^"]+)"|NULL)\}', m[2])])
assert len(pages) == 7 and sum(map(len, pages)) == 44
entries = {entry['key']: entry for entry in data['items']}
assert len(entries) == len(data['items'])
assert set(entries) == {label for page in pages for label, _, _ in page}
groups = [('shoot', 'S', 'ถ่ายภาพ'), ('focus', 'F', 'โฟกัส'), ('expo', 'E', 'ค่าแสง'),
          ('overlay', 'O', 'ตัวช่วยแสดงภาพ'), ('movie', 'V', 'วิดีโอ'), ('setup', '+', 'ตั้งค่า'), ('games', 'G', 'เกมและสคริปต์')]
source_for_menu = {'Shoot': 'firmware/src/shoot.c', 'Focus': 'firmware/src/focus.c', 'Expo': 'firmware/src/shoot.c',
                   'Overlay': 'firmware/src/zebra.c', 'Movie': 'firmware/src/movtweaks.c', 'Movie Tweaks': 'firmware/src/bitrate.c',
                   'Prefs': 'firmware/src/menu.c', 'Modules': 'firmware/src/module.c', 'Display': 'firmware/src/tweaks.c',
                   'Help': 'firmware/src/photo-camera-info-600d.h', 'Debug': 'firmware/src/photo-camera-info-600d.h',
                   'Games': 'firmware/modules/arkanoid/arkanoid.c', 'Scripts': 'firmware/modules/lua/lua.c'}
source_for_item = {'Picture Style': 'firmware/src/picstyle.c', 'Cropmarks': 'firmware/src/cropmarks.c',
                   'Bitrate (CBR)': 'firmware/src/bitrate.c', 'Dual ISO': 'firmware/modules/dual_iso/dual_iso.c',
                   'Auto ETTR': 'firmware/modules/ettr/ettr.c', 'Pong': 'firmware/scripts/pong.lua', 'Sokoban': 'firmware/scripts/sokoban.lua'}
for source in source_for_item.values(): assert (ROOT / source).is_file(), source
esc = html.escape
translated = lambda key: lex.get(key, {}).get('th', key)
labeltext = lambda key: translated(key) + (f' ({key})' if translated(key) != key else '')
intro = [
('ใช้คู่มือนี้กับรุ่นใด', f'คู่มือสำหรับ FIRMWARE ADD-ON Thai-Menu {release} บน Canon EOS 600D / Rebel T3i / Kiss X5 และ Canon firmware 1.0.2 ชื่อเมนูอ้างอิงโค้ดรุ่นนี้ ไม่ใช่คู่มือเฟิร์มแวร์ Canon ทั้งระบบ'),
('ขอบเขต', 'อธิบาย 44 รายการใน Photo UI และตัวเลือกย่อยที่ผูกไว้กับเมนูเหล่านี้ ส่วน Modules, Preferences, Display และ Scripts เป็นทางเข้าหน้าระบบเดิม รายการภายในอาจต่างตามโมดูลและสถานะกล้อง จึงไม่ถือว่าเป็นรายการตายตัวครบทุกหน้า Classic'),
('การติดตั้ง', 'หากยังไม่ได้ติดตั้ง ให้อ่านคู่มือติดตั้งที่หน้าดาวน์โหลดและดูคลิปก่อน คู่มือนี้ใช้สำหรับทำความเข้าใจเมนู ไม่ใช้แทนขั้นตอนติดตั้ง'),
('สถานะรุ่น', 'รุ่นนี้เป็น Public Experimental คู่มืออธิบายพฤติกรรมตามโค้ด ไม่ใช่การยืนยันว่าทุกฟังก์ชันผ่านการทดสอบบนกล้องจริง ภาพเมนูที่ลิงก์ไว้เป็นภาพจำลองจากตัววาดเมนูบนคอมพิวเตอร์'),
]
controls = [
('ปุ่มถังขยะ', 'เปิดเมนู Magic Lantern ตามการทำงานปกติของแพ็ก'),
('ขึ้น/ลง หรือวงล้อ', 'เลื่อนรายการในคอลัมน์ที่เลือก หากอยู่คอลัมน์รายการ เมื่อผ่านท้ายหมวดจะไปหมวดถัดไป เช่น S ไป F'),
('ขวา / SET', 'จากหมวดเข้าไปรายการ และจากรายการเข้าแผงตัวเลือกด้านขวา'),
('SET ในแผงตัวเลือก', 'แถวค่าที่แก้ได้: เข้าโหมดแก้ ใช้ซ้าย/ขวาปรับ แล้ว SET จบ; แถวคำสั่งแบบ Action: อาจต้อง SET ยืนยันอีกครั้ง อ่านคำถามบนจอก่อนรัน'),
('ซ้าย', 'ย้อนกลับหนึ่งคอลัมน์เมื่อไม่ได้แก้ค่า หากกำลังแก้ค่า ซ้ายใช้ลด/เปลี่ยนค่า จึงให้กด SET จบก่อนย้อนกลับ'),
('Q / PLAY ในแผงตัวเลือก', 'เปิดตัวเลือกหรือหน้าควบคุมเดิมของรายการนั้นเมื่อรองรับ บางหน้าจึงมีหน้าตาต่างจาก Photo UI'),
('MENU', 'จบการแก้หรือยกเลิกการยืนยันก่อน; เมื่อไม่ได้แก้/ยืนยัน ใช้ปิดเมนู'),
('INFO', 'เมื่อไม่ได้บันทึกวิดีโอ สลับ Photo UI กับ Classic หรือกลับจากตัวแก้ไขเดิม; ระหว่างบันทึก INFO ทำหน้าที่แบบ Q จึงไม่สลับหน้าแบบเดียวกัน'),
('หน้าที่ 1/2 หรือ Options', 'ยังมีรายการหรือตัวเลือกต่ออีกหน้า ใช้ขึ้น/ลงเลื่อนให้ครบ ไม่ได้หมายความว่าเมนูหาย'),
('ค่าปัจจุบัน / ยังใช้งานไม่ได้', 'ค่าปัจจุบันคือสถานะของรายการหลัก; ยังใช้งานไม่ได้อาจเกิดจากยังไม่โหลดโมดูล ไม่รองรับสถานะปัจจุบัน หรืออ่านข้อมูลไม่ได้ ไม่ได้แปลว่าเป็นเลขศูนย์หรือฟังก์ชันถูกลบ'),
]
examples = [
('Timelapse ครั้งแรก', ['ตั้งกล้องบนขาตั้ง ล็อกค่าแสง/โฟกัสให้เหมาะสม', 'S → ตั้งค่าการถ่ายภาพ → จำนวนภาพต่อครั้ง ใช้ 1 (OFF) และปิด Snap Simulation', 'S → Time-lapse ตั้งทุก 5 วินาที หยุดหลัง 120 ภาพ แล้วเลือกวิธีเริ่มที่สะดวก', 'ตรวจภาพช่วงสั้นก่อนปล่อยถ่ายยาว และเว้นช่วงให้กล้องเปิดรับแสง/บันทึกทัน']),
('ถ่ายคร่อมค่าแสง', ['ปิด Canon AEB ก่อน', 'S → ถ่ายคร่อม เลือกชนิดคร่อมค่าแสง จำนวน 3 ภาพ และความต่าง 1 EV เป็นจุดเริ่มทดลอง', 'เลือก Sequence ที่ต้องการ เช่น 0 - + -- ++; จำนวนภาพยังขึ้นกับ Frames', 'ถ่ายหนึ่งชุดแล้วตรวจภาพทั้งสามบนคอมพิวเตอร์ ก่อนเพิ่มระยะ EV หรือจำนวนภาพ']),
('ใช้ตัวช่วยโฟกัสมือหมุน', ['เปิด Live View และ O → เปิดตัวช่วยแสดงภาพ', 'เปิด Focus Peaking เพื่อเห็นบริเวณคม แล้วใช้ Magic Zoom ตรวจซ้ำ', 'ภาพที่เห็นบนจอเป็นตัวช่วย ไม่ได้เพิ่มรายละเอียดหรือซูมเลนส์ในไฟล์ภาพ']),
]
troubles = [
('ถ่ายหลายภาพทั้งที่กดครั้งเดียว', 'ตรวจจำนวนภาพต่อครั้งใน Shoot Preferences, Frames ในถ่ายคร่อม และจำนวนภาพของโหมดตั้งเวลาถ่าย Canon ตัวนับ 2/10 วินาทีบอกเวลาเริ่ม ไม่ใช่จำนวนภาพเสมอไป'),
('เปิด Zebra/Peaking แล้วไม่เห็น', 'ตรวจ Global Draw, สถานะ Live View, ตัวเลือกซ่อนระหว่างบันทึก และเงื่อนไขของตัวช่วยนั้น'),
('Dual ISO / Auto ETTR / เกมยังใช้งานไม่ได้', 'ตรวจไฟล์โมดูล เปิดใน Modules แล้วรีสตาร์ตตามปกติ ต้องเห็น OK ก่อน สำหรับ Pong/Sokoban ใช้ lua ไม่ใช่โมดูลชื่อเกม'),
('จำนวนชัตเตอร์ไม่ขึ้น', 'เป็นข้อมูลอ่านอย่างเดียว หากระบบอ่านจาก Canon ไม่สำเร็จจะไม่สร้างตัวเลขขึ้นมา เก็บภาพอาการและรุ่นที่ใช้เพื่อแจ้งปัญหา'),
('เมนูเป็นอังกฤษบางส่วน', 'ภาษาไทยใช้กับ Photo UI และวลีที่มีในชุดฟอนต์ หน้า Classic คำเตือนจากโมดูล หรือข้อความที่ยังไม่มีคำแปลอาจยังเป็นอังกฤษ'),
]
glossary = [('Tv', 'ค่า APEX ที่เกี่ยวกับเวลารับแสง/ชัตเตอร์'), ('Av', 'ค่า APEX ที่เกี่ยวกับรูรับแสง'), ('Ae / AE compensation', 'การชดเชยแสงอัตโนมัติ ไม่ใช่คำเดียวกับ Av'), ('EV', 'หน่วยความต่างค่าแสง 1 EV ต่างประมาณหนึ่งสต็อป'), ('MLU', 'Mirror Lock-Up: ยกและล็อคกระจกสะท้อนก่อนถ่าย'), ('DOF', 'Depth of Field: ระยะชัด'), ('ETTR', 'Expose To The Right: จัดค่าแสงให้ข้อมูล RAW เข้าใกล้ด้านสว่างโดยคุมไฮไลต์'), ('CBR / VBR', 'วิธีควบคุมอัตราข้อมูลวิดีโอ; CBR ของเมนูนี้ใช้ตัวคูณเทียบค่าปกติ ส่วน VBR ใช้ QScale'), ('SNR', 'อัตราส่วนสัญญาณต่อสัญญาณรบกวน'), ('Live View', 'การแสดงภาพจากเซนเซอร์บนจอแทนการมองผ่านช่องมองภาพ')]
md = [f'# คู่มือเมนูภาษาไทย — Thai-Menu {release}', '', 'สำหรับ Canon EOS 600D / Canon firmware 1.0.2', '']
body = '<section id="before"><h2>ก่อนเริ่มใช้</h2>'
for title, text in intro:
    body += f'<h3>{title}</h3><p>{esc(text)}</p>'; md += ['## ' + title, '', text, '']
body += f'<p><a href="{BASE}download.html#first-install-steps">อ่านวิธีติดตั้ง</a> · <a href="{BASE}videos.html">วิดีโอสอนติดตั้ง</a> · <a href="{BASE}menu-previews/{release}/">แกลเลอรีภาพเมนูจากโค้ด</a></p></section>'
body += '<section id="controls"><h2>ปุ่มและการเลื่อนเมนู</h2><dl>'
md += ['## ปุ่มและการเลื่อนเมนู', '']
for title, text in controls:
    body += f'<dt>{esc(title)}</dt><dd>{esc(text)}</dd>'; md += [f'- **{title}:** {text}']
body += '</dl></section>'; md += ['']
toc = '<nav class="toc" aria-label="สารบัญ"><h2>สารบัญเมนู</h2><a href="#controls">ปุ่มและการเลื่อนเมนู</a>'
for p, (slug, badge, title) in enumerate(groups):
    toc += f'<div class="toc-group"><a href="#{slug}">{badge} · {title}</a><ul>'
    body += f'<section class="menu-group" id="{slug}"><h2>{badge} · {title}</h2>'
    md += [f'## {badge} · {title}', '']
    for i, (key, menu, entry) in enumerate(pages[p]):
        content = entries[key]; ident = slug + '-' + str(i + 1)
        name = labeltext(key)
        toc += f'<li><a href="#{ident}">{esc(translated(key))}</a></li>'
        screenshot = f'{BASE}menu-previews/{release}/th/th-{p+1:02d}-{i+1:02d}-item-01.png'
        source = source_for_item.get(key, source_for_menu[menu])
        assert (ROOT / source).is_file()
        src = f'https://github.com/itsamachom/eos_rom_mlv_modifly/blob/{data["reviewed_source_commit"]}/{source}'
        body += f'<article class="menu-entry" id="{ident}" data-menu-key="{esc(key, quote=True)}"><h3>{esc(name)}</h3><p>{esc(content["purpose"])}</p><p><strong>วิธีใช้:</strong> {esc(content["use"])}</p>'
        md += [f'### {name}', '', content['purpose'], '', '**วิธีใช้:** ' + content['use'], '']
        if content['options']:
            body += '<h4>ตัวเลือกในเมนูนี้</h4><dl>'
            for opt, explanation in content['options'].items():
                body += f'<dt>{esc(labeltext(opt))}</dt><dd>{esc(explanation)}</dd>'
                md += [f'- **{labeltext(opt)}:** {explanation}']
            body += '</dl>'; md += ['']
        if content['notes']:
            body += '<ul class="notes">'
            for note in content['notes']:
                body += '<li>' + esc(note) + '</li>'; md += ['- ' + note]
            body += '</ul>'; md += ['']
        body += f'<p class="references"><a href="{screenshot}" target="_blank" rel="noopener noreferrer">ดูภาพเมนูจำลอง</a> · <a href="{src}" target="_blank" rel="noopener noreferrer">อ้างอิงโค้ด</a> · <a href="#toc">กลับสารบัญ</a></p></article>'
        md += [f'[ภาพเมนูจำลอง]({screenshot}) · [อ้างอิงโค้ด]({src})', '']
    body += '</section>'; toc += '</ul></div>'
toc += '<a href="#examples">ตัวอย่างการตั้งค่า</a><a href="#troubleshooting">เมื่อผลไม่เป็นอย่างที่คาด</a><a href="#glossary">คำศัพท์</a></nav>'
body += '<section id="examples"><h2>ตัวอย่างการตั้งค่า</h2>'
md += ['## ตัวอย่างการตั้งค่า', '']
for title, steps in examples:
    body += f'<h3>{title}</h3><ol>'; md += ['### ' + title, '']
    for i, step in enumerate(steps): body += f'<li>{esc(step)}</li>'; md += [f'{i+1}. {step}']
    body += '</ol>'; md += ['']
body += '</section><section id="troubleshooting"><h2>เมื่อผลไม่เป็นอย่างที่คาด</h2><dl>'; md += ['## เมื่อผลไม่เป็นอย่างที่คาด', '']
for title, text in troubles:
    body += f'<dt>{title}</dt><dd>{esc(text)}</dd>'; md += [f'### {title}', '', text, '']
body += '</dl></section><section id="glossary"><h2>คำศัพท์</h2><dl>'; md += ['## คำศัพท์', '']
for title, text in glossary:
    body += f'<dt>{esc(title)}</dt><dd>{esc(text)}</dd>'; md += [f'- **{title}:** {text}']
body += '</dl></section>'
footer = '<footer><p>ผู้พัฒนา: <a href="https://www.youtube.com/@Online2easy" target="_blank" rel="noopener noreferrer">YouTube Online2easy</a> · <a href="https://www.facebook.com/online2easy" target="_blank" rel="noopener noreferrer">Facebook Online2easy</a> · <a href="https://online2hobby.blogspot.com/" target="_blank" rel="noopener noreferrer">Online2hobby Blog</a></p><p class="fine">โครงการอิสระบน Magic Lantern มี Codex/LLM ช่วยพัฒนาและเรียบเรียงคู่มือ เก็บเครดิตและใบอนุญาตต้นทาง การอธิบายตามโค้ดไม่ใช่ผลทดสอบฮาร์ดแวร์</p></footer>'
stylesheet = '''@font-face{font-family:ManualThai;src:url("assets/manual/NotoSansThai.ttf") format("truetype");font-weight:100 900;font-display:swap}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{overflow-wrap:anywhere;margin:0;background:#101512;color:#f3f5eb;font:18px/1.95 ManualThai,Arial,sans-serif}main,header,footer{width:min(1060px,calc(100% - 40px));margin:auto}header{padding:28px 0;border-bottom:1px solid #36473b}header nav,.actions{display:flex;flex-wrap:wrap;gap:12px 24px}a{color:#74d7f7;overflow-wrap:anywhere}a:focus-visible{outline:3px solid #ffb99a;outline-offset:4px}h1,h2,h3,h4{line-height:1.55}h1{font-size:clamp(30px,5vw,48px)}h2{color:#c7fb73;font-size:30px}h3{font-size:24px}h4{font-size:19px;color:#c7fb73}p{margin:14px 0}section{padding:30px 0;border-bottom:1px solid #36473b}.lead{padding:40px 0 16px}.fine,.references{font-size:15px;color:#bac9ba}.toc{padding:24px;background:#18201b;border:1px solid #36473b}.toc-group{display:inline-block;vertical-align:top;width:48%;padding:16px}.toc>a{display:block}.toc ul{padding-left:22px}.menu-entry{padding:12px 0 28px;border-bottom:1px solid #36473b;scroll-margin-top:20px}.menu-entry:last-child{border-bottom:0}dt{font-weight:700;margin-top:20px;color:#d4f49f}dd{margin:6px 0 0 18px}li{margin:9px 0}.notes{border-left:3px solid #ffb99a;padding:8px 10px 8px 32px}.button{border:1px solid #c7fb73;padding:8px 15px;border-radius:4px;text-decoration:none}footer{padding:35px 0}code{overflow-wrap:anywhere}@media(max-width:600px){.toc-group{display:block;width:100%;padding:10px 0}body{font-size:17px}h2{font-size:26px}h3{font-size:22px}dd{margin-left:0}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@page{size:A4;margin:17mm 16mm 20mm}@media print{html{scroll-behavior:auto}body{background:white;color:#111;font-size:11pt;line-height:1.65}main,footer{width:100%}header,.actions,.references,.screen-only{display:none!important}.toc{background:transparent;border-color:#aaa;break-after:page;padding:8px}.toc-group{display:inline-block;width:48%;padding:6px}.toc li{margin:2px 0;font-size:10pt}h1{font-size:25pt}h2{font-size:19pt;color:#111}h3{font-size:14pt}h4,dt{color:#111}a{color:#16404e;text-decoration:none}section{border-color:#bbb;padding:12px 0}.menu-group{break-before:auto}.menu-entry{padding-bottom:12px}h2,h3,h4,dt{break-after:avoid}li,p,dd{orphans:3;widows:3}.notes{border-color:#777}.fine{color:#444;font-size:9pt}footer{border-top:1px solid #aaa}p{margin:6px 0}dt{margin-top:12px}dd{margin-top:3px}li{margin:5px 0}.notes{padding:5px 8px 5px 24px;break-inside:avoid}dl:has(+ul.notes) dd:last-child{break-after:avoid}section:last-child{break-after:auto}}'''
page = f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>คู่มือเมนูภาษาไทย — Thai-Menu {release}</title><meta name="description" content="คู่มือภาษาไทย 44 เมนูสำหรับ Canon EOS 600D Thai-Menu {release} อธิบายหน้าที่ ตัวเลือก และตัวอย่างการใช้"><link rel="icon" href="assets/icon.svg" type="image/svg+xml"><style>{stylesheet}</style></head><body><header><nav aria-label="เมนูหลัก"><a href="./">หน้าหลัก</a><a href="download.html">ดาวน์โหลด</a><a href="videos.html">วิดีโอ</a><a href="#toc">สารบัญคู่มือ</a></nav></header><main id="main"><div class="lead"><p>FIRMWARE ADD-ON · THAI-MENU {release}</p><h1>คู่มือเมนูภาษาไทย</h1><p>รู้ว่าแต่ละเมนูทำอะไร แล้วเลือกใช้ให้เหมาะกับภาพที่ต้องการ</p><p class="fine">สำหรับ Canon EOS 600D / Canon firmware 1.0.2 · อ้างอิงโค้ด {esc(data['reviewed_source_commit'])} · 44 รายการใน 7 หมวด</p><div class="actions"><a class="button" href="manual/Thai-Menu-{release}-Manual-TH.pdf" download>ดาวน์โหลด PDF ภาษาไทย</a><a class="button" href="{BASE}menu-previews/{release}/">ดูภาพเมนู</a></div></div><div id="toc">{toc}</div>{body}</main>{footer}</body></html>'''
(ROOT / 'docs/manual-th.html').write_text(page)
md += ['', '## แหล่งที่มาและผู้พัฒนา', '', f'อ้างอิงโค้ด `{data["reviewed_source_commit"]}`; เนื้อหาคู่มือ: website-content/manual-th.json', '', f'[คู่มือบนเว็บ]({BASE}manual-th.html) · [คู่มือติดตั้ง]({BASE}download.html#first-install-steps) · [วิดีโอ]({BASE}videos.html)', '', '[YouTube Online2easy](https://www.youtube.com/@Online2easy) · [Facebook Online2easy](https://www.facebook.com/online2easy) · [Online2hobby Blog](https://online2hobby.blogspot.com/)', '', 'โครงการอิสระบน Magic Lantern มี Codex/LLM ช่วยพัฒนาและเรียบเรียงคู่มือ เก็บเครดิต/ใบอนุญาตต้นทาง คู่มือไม่ใช่ผลยืนยันการทดสอบบนกล้องจริง', '']
(ROOT / 'MANUAL_TH.md').write_text('\n'.join(md))
# Link the manual from existing public entry points; keep generated-page renderers in sync.
for relative in ['index.html', 'download.html', 'videos.html']:
    p = ROOT / 'docs' / relative; text = p.read_text()
    if 'href="manual-th.html"' not in text:
        text = re.sub(r'(<nav\b[^>]*>)', r'\1<a href="manual-th.html">คู่มือภาษาไทย</a>', text, count=1)
    p.write_text(text)
print('Rendered Thai HTML and Markdown manual: 44 menu entries, 7 groups')
