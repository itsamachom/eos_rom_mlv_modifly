"""Render the Thai/English download pages and GitHub download guide from verified package metadata."""
from pathlib import Path
import html
import json
import re

root = Path(__file__).resolve().parents[1]
version = (root/'scripts/photo-ui-version.txt').read_text().strip()
assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*',version)
info = json.loads((root/f'downloads/{version}/DOWNLOAD_INFO.json').read_text())
assert info['version'] == version
repo = 'https://github.com/itsamachom/eos_rom_mlv_modifly'
raw = 'https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly'
camera = info['camera']; source = info['source']
camera_url = f'{raw}/site/eos-600d-bilingual/{camera["path"]}'
sums_url = f'{raw}/site/eos-600d-bilingual/downloads/{version}/SHA256SUMS'
notes_url = f'{repo}/blob/{version}/PHOTO_UI_{version.upper()}.md'
github_url = f'{repo}/blob/site/eos-600d-bilingual/DOWNLOAD.md'
css_version = re.search(r'site.css\?v=([^"\s]+)',(root/'docs/index.html').read_text()).group(1)
mb = lambda size:f'{size/1_000_000:.2f} MB'
for lang in ['th','en']:
    th = lang=='th'
    home = './' if th else './'
    assets = 'assets/' if th else '../assets/'
    counterpart = 'en/download.html' if th else '../download.html'
    text = {
        'title':'ดาวน์โหลด Thai-Menu' if th else 'Download Thai-Menu',
        'skip':'ข้ามไปเนื้อหา' if th else 'Skip to content',
        'home':'หน้าหลัก' if th else 'Home',
        'language':'English' if th else 'ภาษาไทย',
        'intro':'เลือกไฟล์ให้ตรงกับการใช้งาน: ไฟล์อัปเดตสำหรับกล้อง และ Source สำหรับผู้พัฒนาแยกกัน' if th else 'Choose the camera update for your card. Source code is a separate download for developers.',
        'target':'สำหรับ Canon EOS 600D / Canon firmware 1.0.2 ที่ติดตั้ง Magic Lantern แล้วเท่านั้น' if th else 'For Canon EOS 600D / Canon firmware 1.0.2 already running Magic Lantern only.',
        'status':'Experimental ไม่ใช่ Stable — ยังไม่ได้ทดสอบ v3r4 บนกล้องจริงหรือ QEMU และซอร์ส dietlibc เดิมยังยืนยันไม่ครบ' if th else f'Experimental, not Stable — {version} camera/QEMU testing and inherited dietlibc source verification remain outstanding.',
        'camera_title':'ไฟล์สำหรับอัปเดตกล้อง' if th else 'Camera update',
        'camera_desc':'มี autoexec.bin และ ML/ สำหรับอัปเดตกล้อง ไม่รวม Source ZIP หรือตัวติดตั้ง FIR ไฟล์ใช้งานตรงกับ v3r4 Full เดิมทุกไบต์ ไม่มีการเปลี่ยนโค้ดเฟิร์มแวร์' if th else f'Contains autoexec.bin and ML/ for updating an existing installation. No source archive or FIR installer. Runtime files are byte-identical to the original {version} Full package.',
        'camera_button':'ดาวน์โหลดไฟล์สำหรับกล้อง' if th else 'Download camera update',
        'camera_hint':'ไฟล์นี้สำหรับนำไปอัปเดตในการ์ด ตามวิธีด้านล่าง' if th else 'Use this file for the card update described below.',
        'source_title':'Source code สำหรับผู้พัฒนา' if th else 'Source code for developers',
        'source_desc':'โค้ดของ fork ที่ตรงกับไบนารี v3r4 และเอกสารที่มา ใช้ศึกษาและพัฒนาต่อ ไม่ใช่ไฟล์ติดตั้งกล้อง' if th else f'The matching {version} fork source and provenance records, for study and development. This is not a camera update.',
        'source_button':'ดาวน์โหลด Source — ไม่ใช้ลงกล้อง' if th else 'Download source — not for the card',
        'source_hint':'ไม่ใช้ Code → Download ZIP หรือ Source code ที่ GitHub สร้างให้อัตโนมัติแทนไฟล์อัปเดตกล้อง' if th else 'Do not use Code → Download ZIP or automatic GitHub Source code archives as a camera update.',
        'instructions':'วิธีอัปเดตสำหรับกล้องที่มี ML แล้ว' if th else 'Update an existing ML installation',
        'steps':['สำรองข้อมูลในการ์ด รวมถึง autoexec.bin และ ML/ เดิม','ปิดกล้อง ใช้ card reader และแตกไฟล์ UPDATE.zip บนคอมพิวเตอร์','นำ autoexec.bin กับโฟลเดอร์ ML/ ทั้งชุดไปแทนที่ที่รากการ์ด อย่าเพิ่มโฟลเดอร์ซ้อน','เปิดกล้อง ตรวจ + → เวอร์ชั่น ว่าเป็น Thai-Menu '+version,'ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู อ่าน INSTALL_TH.md ที่แนบใน ZIP ก่อนใช้'] if th else ['Back up the card, including the existing autoexec.bin and ML/ directory.','Turn off the camera, use a card reader and extract UPDATE.zip on the computer.','Replace autoexec.bin and the entire ML/ directory at the card root, without adding another folder layer.','Turn on the camera and check Setup (+) → Version: Thai-Menu '+version+'.','Do not run Firmware Update again for this menu update. Read INSTALL_EN.md inside the ZIP first.'],
        'first_install':'ยังไม่มี ML บนกล้อง? แพ็กเกจนี้ไม่ใช่ตัวติดตั้งครั้งแรกและไม่มี FIR กรุณาอย่าใช้แทนขั้นตอนติดตั้ง ML รุ่นนี้ยังไม่มีผลทดสอบการติดตั้งครั้งแรกใหม่' if th else 'No ML on the camera yet? This package is not a first-install kit and has no FIR. It does not replace the ML installation procedure; first-install testing is not claimed.',
        'verify':'ตรวจสอบไฟล์ก่อนใช้' if th else 'Verify before use',
        'verify_desc':'ดาวน์โหลด SHA256SUMS แล้วตรวจ hash ของไฟล์ที่เลือก ถ้าดาวน์โหลดทั้งไฟล์กล้องกับ Source ให้วางคู่กันและรัน sha256sum -c SHA256SUMS' if th else 'Download SHA256SUMS and compare the hash for the selected file. If you download both camera and source ZIPs, place them together and run sha256sum -c SHA256SUMS.',
        'notes':'รายละเอียดรุ่นและข้อจำกัด' if th else 'Release notes and limitations',
        'github':'หน้าดาวน์โหลดบน GitHub' if th else 'GitHub download guide',
        'disclosure':'โครงการอิสระที่มี Codex/LLM ช่วยพัฒนา เก็บเครดิตและใบอนุญาต Magic Lantern และส่วนประกอบต้นทาง ไม่ใช่บิลด์ที่ Canon หรือทีม Magic Lantern รับรอง' if th else 'An independent Codex/LLM-assisted fork retaining Magic Lantern and dependency notices. Not endorsed by Canon or the Magic Lantern team.',
    }
    text['status'] = text['status'].replace('v3r4',version)
    text['camera_desc'] = text['camera_desc'].replace('v3r4',version)
    text['source_desc'] = text['source_desc'].replace('v3r4',version)
    steps = ''.join(f'<li>{html.escape(step)}</li>' for step in text['steps'])
    page = f'''<!doctype html>
<!-- Project download page; GPL-2.0-or-later. Retain upstream notices. -->
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{text['title']} {version} — FIRMWARE ADD-ON</title><meta name="description" content="{text['intro']}">
<link rel="icon" href="{assets}icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{assets}site.css?v={css_version}"><link rel="alternate" hreflang="{'en' if th else 'th'}" href="{counterpart}"></head>
<body><a class="skip" href="#main">{text['skip']}</a>
<header class="top"><div class="wrap top-inner"><a class="brand" href="{home}"><span class="mark" aria-hidden="true">+</span><span><strong>EOS 600D</strong><small>FIRMWARE ADD-ON</small></span></a><nav aria-label="{'เมนูหลัก' if th else 'Main navigation'}"><a href="{home}">{text['home']}</a><a href="{github_url}">GitHub</a><a class="language" href="{counterpart}" lang="{'en' if th else 'th'}" hreflang="{'en' if th else 'th'}">{text['language']}</a></nav></div></header>
<main id="main" class="wrap"><section class="section download-lead"><div class="eyebrow">FIRMWARE ADD-ON · Thai-Menu {version}</div><h1>{text['title']} {version}</h1><p>{text['intro']}</p><p><strong>{text['target']}</strong></p><p class="download-note">{text['status']}</p></section>
<div class="download-grid">
<section class="download-card download-card-primary" id="camera-download"><span class="eyebrow">01 · CAMERA UPDATE</span><h2>{text['camera_title']}</h2><p>{text['camera_desc']}</p><p class="file-name">{camera['filename']}</p><p>{mb(camera['bytes'])} · {version} · 600D.102</p><a class="button primary" data-download="camera" href="{camera_url}">{text['camera_button']}</a><p class="fine">{text['camera_hint']}</p><p class="fine">SHA256<br><code class="checksum">{camera['sha256']}</code></p></section>
<section class="download-card" id="source-download"><span class="eyebrow">02 · SOURCE CODE</span><h2>{text['source_title']}</h2><p>{text['source_desc']}</p><p class="file-name">{source['filename']}</p><p>{mb(source['bytes'])} · {version}</p><a class="button" data-download="source" href="{source['url']}">{text['source_button']}</a><p class="fine">{text['source_hint']}</p><p class="fine">SHA256<br><code class="checksum">{source['sha256']}</code></p></section>
</div>
<section class="section" id="update-instructions"><h2>{text['instructions']}</h2><ol class="update-steps">{steps}</ol><p class="download-note">{text['first_install']}</p><p><a href="{notes_url}">{text['notes']}</a></p></section>
<section class="section" id="checksums"><h2>{text['verify']}</h2><p>{text['verify_desc']}</p><a class="button" data-download="checksums" href="{sums_url}">SHA256SUMS</a></section>
</main><footer class="footer wrap"><p><a href="{github_url}">{text['github']}</a> · <a href="{home}">{text['home']}</a></p><p class="disclosure">{text['disclosure']}</p></footer></body></html>
'''
    (root/('docs/download.html' if th else 'docs/en/download.html')).write_text(page)

(root/'DOWNLOAD.md').write_text(f'''# ดาวน์โหลด / Downloads — FIRMWARE ADD-ON Thai-Menu {version}

**Canon EOS 600D / Canon firmware 1.0.2 · Public Experimental**
[หน้าเว็บดาวน์โหลดภาษาไทย](https://itsamachom.github.io/eos_rom_mlv_modifly/download.html) · [English download page](https://itsamachom.github.io/eos_rom_mlv_modifly/en/download.html)

## 1. ไฟล์สำหรับอัปเดตกล้อง / Camera update

### [ดาวน์โหลด {camera['filename']}]({camera_url})

**{mb(camera['bytes'])}** — สำหรับกล้องที่ติดตั้ง ML แล้ว มี autoexec.bin และ ML/ ไม่มี Source ZIP หรือตัวติดตั้ง FIR ไม่ใช่แพ็กเกจสำหรับติดตั้ง ML ครั้งแรก

Back up the card; replace autoexec.bin and the entire ML/ directory at the card root. Do not run Firmware Update again for this UI update. Read INSTALL_TH.md / INSTALL_EN.md inside the ZIP.

SHA256: `{camera['sha256']}`

## 2. Source code สำหรับผู้พัฒนา / Developer source

### [ดาวน์โหลด {source['filename']}]({source['url']})

**{mb(source['bytes'])}** — ซอร์ส fork ที่ตรงกับไบนารี ใช้ศึกษา/พัฒนา **ไม่ใช่ไฟล์ลงกล้อง** ไม่ใช้ Code → Download ZIP หรือ Source code ที่ GitHub สร้างอัตโนมัติแทน camera update

Source is pinned to tag [{version}]({repo}/tree/{version}). Inherited dietlibc corresponding source remains unverified; including fork source does not close that audit.

SHA256: `{source['sha256']}`

## 3. Checksum และข้อมูลรุ่น

- [ดาวน์โหลด SHA256SUMS]({sums_url}) — ตรวจไฟล์ที่เลือก หรือวางทั้งสอง ZIP ไว้ด้วยกันแล้วรัน `sha256sum -c SHA256SUMS`
- [ข้อมูลแพ็กเกจ]({raw}/site/eos-600d-bilingual/downloads/{version}/DOWNLOAD_INFO.json)
- [รายละเอียด {version} และข้อจำกัด]({notes_url})

ไฟล์สำหรับกล้องใช้ runtime bytes เดียวกับ Full {version} เดิมทุกไบต์ เป็นการแยกแพ็กเกจโดยไม่ rebuild เฟิร์มแวร์ รุ่นนี้ยังไม่ได้ทดสอบบนกล้องจริง/QEMU และไม่ใช่ Stable ไม่ใช่บิลด์ที่ Canon/Magic Lantern รับรอง เครดิตและใบอนุญาตต้นทางยังคงอยู่ในแพ็กเกจ

The older Full ZIP bundles camera files and source together. It remains unchanged for archival use; the camera-only UPDATE ZIP above is the recommended download for an existing ML installation.
'''.replace('**  \n','**\n'))
(root/f'downloads/{version}/README.md').write_text(f'''# {version} downloads

[เปิดหน้าดาวน์โหลดที่แยกไฟล์กล้องและ Source / Download guide](../../DOWNLOAD.md)

- `camera/{camera['filename']}`: camera update only, {mb(camera['bytes'])}; for an existing ML installation, no source ZIP or FIR.
- Matching source is linked in DOWNLOAD_INFO.json and SOURCE.txt inside the camera ZIP. It is the immutable source ZIP from tag {version}.
- SHA256SUMS lists both the camera ZIP and separately downloaded source ZIP.
- Original Full delivery and tag {version} are unchanged. Runtime autoexec.bin and ML/ bytes are identical.
''')
print('Rendered docs/download.html, docs/en/download.html, DOWNLOAD.md and download-folder guide')
