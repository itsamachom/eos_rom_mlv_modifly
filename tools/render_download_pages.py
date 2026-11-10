"""Render latest-only download pages: first install, existing-ML update and source."""
from pathlib import Path
import hashlib
import html
import json
import re

root=Path(__file__).resolve().parents[1]
v=(root/'scripts/photo-ui-version.txt').read_text().strip()
assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*',v)
meta=json.loads((root/f'downloads/{v}/DOWNLOAD_INFO.json').read_text());assert meta['version']==v
repo='https://github.com/itsamachom/eos_rom_mlv_modifly'
raw='https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly'
github=f'{repo}/blob/site/eos-600d-bilingual/DOWNLOAD.md'
notes=f'{repo}/blob/{v}/PHOTO_UI_{v.upper()}.md'
sums=f'{raw}/site/eos-600d-bilingual/downloads/{v}/SHA256SUMS'
profiles=[('YouTube · Online2easy','https://www.youtube.com/@Online2easy'),('Facebook · Online2easy','https://www.facebook.com/online2easy'),('Blog · Online2hobby','https://online2hobby.blogspot.com/')]
css=hashlib.sha256((root/'docs/assets/site.css').read_bytes()).hexdigest()[:12]
urls={key:(item.get('url') or f'{raw}/site/eos-600d-bilingual/{item["path"]}') for key,item in [(key,meta[key]) for key in ['first_install','camera','source']]}
mb=lambda item:f'{item["bytes"]/1_000_000:.2f} MB'
for lang in ['th','en']:
    th=lang=='th';assets='assets/' if th else '../assets/';other='en/download.html' if th else '../download.html'
    title=('ดาวน์โหลด Thai-Menu ' if th else 'Download Thai-Menu ')+v
    intro='ยังไม่เคยลง ML? เลือกติดตั้งครั้งแรกได้เลย ชุดนี้รวมตัวติดตั้ง ML กับเมนูไทยแล้ว ส่วนผู้ที่มี ML อยู่แล้วเลือกอัปเดต' if th else 'New to ML? Choose First installation: the original ML installer and current Thai-Menu are in one package. Existing ML users choose Update.'
    target='สำหรับ Canon EOS 600D / Canon firmware 1.0.2 ทั้งกล้องที่ยังไม่มี ML และกล้องที่มี ML แล้ว' if th else 'For Canon EOS 600D / Canon firmware 1.0.2, with or without an existing ML installation.'
    status=f'Public Experimental {v} ไม่ใช่ Stable ยังไม่ได้ทดสอบรุ่นนี้บนกล้องจริง/QEMU หรือยืนยัน first install บนฮาร์ดแวร์ ตัวติดตั้ง FIR เป็นไฟล์เดิมที่ตรวจ hash แล้ว และซอร์ส dietlibc เดิมยังยืนยันไม่ครบ' if th else f'Public Experimental {v}, not Stable. Camera/QEMU and first-install hardware behavior have not been verified for this version. The original FIR hash is checked; inherited dietlibc source verification remains outstanding.'
    headings=['ติดตั้งครั้งแรก — ยังไม่มี ML','อัปเดต — มี ML อยู่แล้ว','Source code — ผู้พัฒนา'] if th else ['First installation — no ML yet','Update — already using ML','Source code — developers']
    descriptions=['รวม autoexec.bin, ML/ และ ML-SETUP.FIR ไม่ต้องติดตั้ง ML จากไฟล์ชุดอื่นก่อน อ่านขั้นตอนด้านล่างก่อนเริ่ม','มี autoexec.bin กับ ML/ ไม่มี FIR ใช้กับกล้องและการ์ดที่บูต ML อยู่แล้ว ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู','ซอร์สของ fork ที่ตรงกับไบนารี ไม่ใช่ไฟล์สำหรับลงกล้อง และไม่ใช่หลักฐานว่าซอร์ส dietlibc เดิมถูกยืนยันครบแล้ว'] if th else ['Includes autoexec.bin, ML/ and the original ML-SETUP.FIR. No separate prior ML package is required. Read the steps below before starting.','Contains autoexec.bin and ML/ with no FIR. For an already-working ML camera/card; do not repeat Firmware Update for this menu update.','Matching fork source for development, not a camera installation. This does not establish completeness of inherited dietlibc source.']
    labels=['ดาวน์โหลดชุดติดตั้งครั้งแรก','ดาวน์โหลดชุดอัปเดต','ดาวน์โหลด Source — ไม่ใช้ลงกล้อง'] if th else ['Download first-install kit','Download camera update','Download source — not for the card']
    cards=[]
    for index,key in enumerate(['first_install','camera','source']):
        item=meta[key]
        cards.append(f'''<section class="download-card{' download-card-primary' if key=='first_install' else ''}" id="{'source-download' if key=='source' else key+'-download'}"><span class="eyebrow">0{index+1} · {key.upper().replace('_',' ')}</span><h2>{headings[index]}</h2><p>{descriptions[index]}</p><p class="file-name">{item['filename']}</p><p>{mb(item)} · {v}</p><a class="button{' primary' if key=='first_install' else ''}" data-download="{key}" href="{urls[key]}">{labels[index]}</a><p class="fine">SHA256<br><code class="checksum">{item['sha256']}</code></p></section>''')
    first_steps=['ตรวจ Canon firmware ให้เป็น 1.0.2 เลือกโหมด M ใช้แบตเตอรี่ Canon ที่ชาร์จเต็มและถอดอุปกรณ์เสริม','สำรองไฟล์ก่อนฟอร์แมต ใช้ SD/SDHC ไม่เกิน 32 GB สำหรับติดตั้งครั้งแรกตามคู่มือต้นทาง','ฟอร์แมตการ์ดในกล้องหลังสำรองข้อมูลแล้ว ปิดกล้อง รอไฟการ์ดดับ และรอ 5 วินาทีหลังเปิดฝาก่อนถอด','แตก FIRST-INSTALL.zip ลงรากการ์ด ให้ autoexec.bin, ML/ และ ML-SETUP.FIR อยู่ด้วยกัน ไม่ซ้อนในโฟลเดอร์ชื่อ ZIP','ใส่การ์ดกลับ เปิดกล้องในโหมด M เข้า Canon → Firmware Ver. → Firmware Update เพื่อเรียกตัวติดตั้ง ML','เมื่อจอเขียวยืนยันสำเร็จ / Please restart your camera. ให้รีสตาร์ตตามข้อความทันที อย่าค้างในหน้านับถอยหลัง 60 วินาที เพราะใช้ถอนการติดตั้ง','หลังเปิดใหม่ กดปุ่มถังขยะ ดู + → เวอร์ชั่น ให้เป็น Thai-Menu '+v+' แล้วทดสอบภาพปกติก่อนใช้งานจริง','หากพบ error จอดำหรือไฟกะพริบผิดปกติ ให้หยุดและอ่าน Troubleshooting ใน INSTALL_UPSTREAM.txt ที่แนบมา ไม่แฟลชซ้ำแบบสุ่ม'] if th else ['Verify Canon firmware 1.0.2, select M, fully charge an original Canon battery and remove accessories.','Back up files before formatting. Use an SD/SDHC card of 32 GB or less for first installation, as required upstream.','Format in the camera after backing up. Turn off, wait for card activity to stop and wait five seconds after opening the card door.','Extract FIRST-INSTALL.zip at the card root with autoexec.bin, ML/ and ML-SETUP.FIR together, without an extra folder layer.','Insert the card, turn on in M and select Canon Firmware Ver. → Firmware Update to launch the ML installer.','At the green confirmation / Please restart your camera. message, restart as instructed. Do not remain on the 60-second countdown screen: it leads to uninstalling.','After restart, press Delete and check Setup (+) → Version: Thai-Menu '+v+'. Test ordinary photos before relying on it.','If there is an error, black screen or abnormal LED activity, stop and read the included upstream Troubleshooting. Do not repeatedly flash random files.']
    update='สำรอง autoexec.bin และ ML/ เดิม ปิดกล้อง ใช้ card reader แทนที่สองรายการนี้จาก UPDATE.zip ที่รากการ์ด ไม่ต้องฟอร์แมตหรือเรียก Firmware Update ซ้ำ การ์ดใหม่ที่ยังไม่บูต ML ต้องเตรียมตามคู่มือต้นทาง' if th else 'Back up the existing autoexec.bin and ML/. With the camera off, use a reader to replace both at the card root from UPDATE.zip. No format or repeat Firmware Update is needed. A new card may need separate boot preparation as described upstream.'
    developer='ผู้พัฒนา' if th else 'Developer';home='หน้าหลัก' if th else 'Home'
    devlinks=' · '.join(f'<a href="{url}">{label}</a>' for label,url in profiles)
    page=f'''<!doctype html>
<!-- Project website; GPL-2.0-or-later. Retain upstream notices. -->
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} — FIRMWARE ADD-ON</title><meta name="description" content="{intro}"><link rel="icon" href="{assets}icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{assets}site.css?v={css}"><link rel="alternate" hreflang="{'en' if th else 'th'}" href="{other}"></head>
<body><a class="skip" href="#main">{'ข้ามไปเนื้อหา' if th else 'Skip to content'}</a><header class="top"><div class="wrap top-inner"><a class="brand" href="./"><span class="mark" aria-hidden="true">+</span><span><strong>EOS 600D</strong><small>FIRMWARE ADD-ON</small></span></a><nav aria-label="{'เมนูหลัก' if th else 'Main navigation'}"><a href="./">{home}</a><a href="./#creator">{developer}</a><a href="{github}">GitHub</a><a class="language" lang="{'en' if th else 'th'}" href="{other}">{'English' if th else 'ภาษาไทย'}</a></nav></div></header>
<main id="main" class="wrap"><section class="section download-lead"><div class="eyebrow">FIRMWARE ADD-ON · THAI-MENU {v}</div><h1>{title}</h1><p>{intro}</p><p><strong>{target}</strong></p><p class="download-note">{status}</p></section><div class="download-grid">{''.join(cards)}</div>
<section class="section" id="first-install-steps"><h2>{'วิธีติดตั้งครั้งแรก — ยังไม่มี ML' if th else 'First installation — no ML yet'}</h2><ol class="update-steps">{''.join('<li>'+html.escape(step)+'</li>' for step in first_steps)}</ol><p>{'ไม่ใช้กับกล้องหรือ Canon firmware รุ่นอื่น และไม่ใช้ ML-SETUP.FIR แทนตัวอัปเดต Canon' if th else 'Do not use on other cameras or Canon firmware versions. ML-SETUP.FIR is not a Canon firmware updater.'}</p></section>
<section class="section" id="update-instructions"><h2>{'วิธีอัปเดต — มี ML อยู่แล้ว' if th else 'Update — already using ML'}</h2><p>{update}</p><p><a href="{notes}">{'รายละเอียดรุ่นและคู่มือใน ZIP' if th else 'Release notes and included instructions'}</a></p></section>
<section class="section" id="checksums"><h2>{'ตรวจไฟล์ก่อนใช้' if th else 'Verify before use'}</h2><p>{'ตรวจ SHA256 ของไฟล์ที่เลือกกับค่าบนหน้านี้ หรือดาวน์โหลดทั้งสามไฟล์คู่กับ SHA256SUMS แล้วรัน sha256sum -c SHA256SUMS' if th else 'Compare the selected file with its SHA256 on this page, or download all three files and run sha256sum -c SHA256SUMS.'}</p><a class="button" data-download="checksums" href="{sums}">SHA256SUMS</a></section></main>
<footer class="footer wrap"><p><a href="{github}">{'หน้าดาวน์โหลด GitHub' if th else 'GitHub download guide'}</a> · <a href="./">{home}</a></p><div class="developer-links"><strong>{developer}:</strong> {devlinks}</div><p class="disclosure">Independent Codex/LLM-assisted fork. Preserve upstream credits/licenses. Not endorsed by Canon or Magic Lantern. Inherited dietlibc corresponding source remains unverified.</p></footer></body></html>
'''
    (root/('docs/download.html' if th else 'docs/en/download.html')).write_text(page)
md=f'''# FIRMWARE ADD-ON Thai-Menu {v} — ดาวน์โหลด / Downloads

Canon EOS 600D / Canon firmware **1.0.2** · Public Experimental

**ยังไม่เคยลง ML ก็ติดตั้งจากชุด FIRST-INSTALL ได้ ไม่ต้องลง ML จาก ZIP อื่นก่อน**

[หน้าเว็บดาวน์โหลด](https://itsamachom.github.io/eos_rom_mlv_modifly/download.html) · [English](https://itsamachom.github.io/eos_rom_mlv_modifly/en/download.html)

'''
for i,key in enumerate(['first_install','camera','source']):
    item=meta[key];title={'first_install':'ติดตั้งครั้งแรก / First installation','camera':'อัปเดต ML ที่มีแล้ว / Update','source':'Source สำหรับผู้พัฒนา'}[key]
    desc={'first_install':'รวม autoexec.bin, ML/ และ ML-SETUP.FIR เดิม พร้อมคู่มือไทย/อังกฤษและต้นทาง ต้องอ่านคู่มือติดตั้งก่อน ไม่ใช่ไฟล์ Canon firmware update','camera':'autoexec.bin และ ML/ ไม่มี FIR ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู','source':'ซอร์ส fork ที่ตรงกับไบนารี ไม่ใช่ไฟล์ลงกล้อง ไม่ใช้ Code → Download ZIP แทนไฟล์ติดตั้ง'}[key]
    md+=f'## {i+1}. {title}\n\n### [ดาวน์โหลด {item["filename"]}]({urls[key]})\n\n**{mb(item)}** — {desc}\n\nSHA256: `{item["sha256"]}`\n\n'
md+=f'''## คู่มือและข้อจำกัด

[คู่มือติดตั้ง](INSTALL_TH.md) · [รายละเอียด {v}]({notes}) · [SHA256SUMS]({sums})

การติดตั้งครั้งแรกอ้างอิงคู่มือต้นทาง ใช้แบตเตอรี่ Canon เต็ม, โหมด M, SD/SDHC ไม่เกิน 32 GB, สำรองก่อนฟอร์แมต และรีสตาร์ตเมื่อ installer ขึ้นจอเขียว/Please restart your camera. ไม่ปล่อยค้างนับถอยหลังถอนการติดตั้ง

ตัวติดตั้ง FIR เดิมตรวจ hash/size แล้ว ไม่ได้ rebuild รุ่นนี้ยังไม่ได้ทดสอบบนกล้องจริง/QEMU หรือยืนยัน first install บนฮาร์ดแวร์ ไม่ใช่ Stable และ inherited dietlibc corresponding source ยังยืนยันไม่ครบ เก็บเครดิต/ใบอนุญาตเดิม ไม่ใช่บิลด์ที่ Canon หรือ Magic Lantern รับรอง

## ผู้พัฒนา / Developer

[YouTube Online2easy](https://www.youtube.com/@Online2easy) · [Facebook Online2easy](https://www.facebook.com/online2easy) · [Online2hobby Blog](https://online2hobby.blogspot.com/)

[รุ่นเก่าในประวัติ Git](ARCHIVE.md) — หน้านี้แสดงเฉพาะรุ่นล่าสุด
'''
(root/'DOWNLOAD.md').write_text(md)
(root/f'downloads/{v}/README.md').write_text(f'# {v} downloads\n\n[คู่มือเลือกไฟล์ / Download guide](../../DOWNLOAD.md)\n\nFirst-install ZIP includes the original verified FIR; update ZIP omits FIR. Both contain the same {v} runtime bytes and no nested source archive. Matching source and SHA256 are listed in DOWNLOAD_INFO.json. No hardware first-install claim is made.\n')
print('Rendered first-install/update/source pages and developer links for',v)
