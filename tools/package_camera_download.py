"""Create a camera-only update from an existing tagged Full delivery, without rebuilding firmware."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
release = (root/'scripts/photo-ui-version.txt').read_text().strip()
assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*',release)
repo = 'itsamachom/eos_rom_mlv_modifly'
raw = f'https://raw.githubusercontent.com/{repo}'
full_dir = root/f'deliveries/photo-ui-{release}-full'
full = full_dir/f'600D-102-PHOTO-UI-{release}-FULL-EXPERIMENTAL.zip'
source = full_dir/f'600D-PHOTO-UI-{release}-source.zip'
# This tool repackages a published version; it must match that version's immutable tag.
commit = subprocess.check_output(['git','rev-parse',f'{release}^{{commit}}'],cwd=root,text=True).strip()
subprocess.run(['git','diff','--exit-code',release,'--',str(full.relative_to(root)),str(source.relative_to(root))],cwd=root,check=True)
sha = lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(full) as z:
    assert z.testzip() is None
    original = {n:z.read(n) for n in z.namelist() if not n.endswith('/')}
    build_info = json.loads(original['BUILD_INFO.json'])
    assert build_info['version'] == f'PHOTO-UI-{release}.600D.102'
    assert original['SOURCE/'+source.name] == source.read_bytes()
    assert sha(source.read_bytes()) == build_info['source_zip_sha256']
    for line in original['PAYLOAD_SHA256SUMS'].decode().splitlines():
        expected,name = line.split('  ',1)
        assert sha(original[name]) == expected,name
payload = {n:b for n,b in original.items() if n=='autoexec.bin' or n.startswith('ML/')}
assert sha(payload['autoexec.bin']) == build_info['autoexec_sha256']
out = root/f'downloads/{release}'
zip_path = out/f'camera/600D-102-Thai-Menu-{release}-UPDATE.zip'
assert not zip_path.exists(),'Camera download exists; do not overwrite a published artifact.'
zip_path.parent.mkdir(parents=True,exist_ok=True)
source_url = f'{raw}/{release}/{source.relative_to(root)}'
update_th = f'''# FIRMWARE ADD-ON Thai-Menu {release} — อัปเดตกล้องที่มี ML แล้ว

สำหรับ Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น เป็น Experimental ไม่ใช่ Stable

แพ็กเกจนี้เป็นไฟล์อัปเดตเมนูสำหรับกล้องที่ติดตั้ง Magic Lantern และใช้งานอยู่แล้ว ไม่รวม Source ZIP หรือตัวติดตั้ง .FIR สำหรับเริ่มติดตั้ง ML ครั้งแรก

1. สำรองไฟล์ในการ์ดก่อน รวมถึง autoexec.bin และ ML/ เดิม
2. ปิดกล้องและใช้ card reader แตกไฟล์ ZIP ลงคอมพิวเตอร์
3. นำ autoexec.bin และโฟลเดอร์ ML/ ทั้งชุดไปแทนที่ที่รากการ์ด อย่าวางซ้อนในโฟลเดอร์ ZIP อีกชั้น
4. นำการ์ดกลับเข้ากล้อง เปิดและตรวจ + → เวอร์ชั่น: Thai-Menu {release}
5. ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู และไม่นำ Source ZIP ไปลงการ์ด

หากยังไม่มี ML บนกล้อง อย่าใช้แพ็กเกจนี้เป็นตัวติดตั้งครั้งแรก รุ่นนี้ยังไม่ผ่านการทดสอบการติดตั้งครั้งแรกใหม่หรือการทดสอบฮาร์ดแวร์ {release}

ไฟล์ autoexec.bin และ ML/ ตรงกับ Full {release} เดิมทุกไบต์ ไม่มีการ rebuild หรือแก้เฟิร์มแวร์ในขั้นตอนแยกแพ็กเกจ

เว็บไซต์: https://itsamachom.github.io/eos_rom_mlv_modifly/
ซอร์สที่ตรงกัน: {source_url}
SHA256 source ZIP: {sha(source.read_bytes())}

ดู SOURCE.txt, THIRD_PARTY_NOTICES.md และ release/v3r2/PROVENANCE.md สำหรับเครดิตและข้อจำกัด corresponding source ของ inherited dietlibc ที่ยังไม่ถูกยืนยัน เก็บประกาศลิขสิทธิ์และใบอนุญาตเดิม
'''
update_en = f'''# FIRMWARE ADD-ON Thai-Menu {release} — camera update

Canon EOS 600D / Canon firmware 1.0.2 only. Public Experimental, not Stable.
For cameras already running Magic Lantern. This ZIP is not a first-install kit: it contains no FIR installer or source archive.

Back up the card, turn off the camera and use a card reader. Extract this ZIP on the computer and replace autoexec.bin and the entire ML/ directory at the card root. Avoid adding another folder layer. Turn on the camera and check Setup (+) > Version: Thai-Menu {release}. Do not run Firmware Update again for this menu update. Do not put the source ZIP on the card.

Runtime files are byte-identical to the tagged Full {release} package; no firmware rebuild was performed. Camera/QEMU and first-install testing are not claimed for this version.

Project: https://itsamachom.github.io/eos_rom_mlv_modifly/
Matching source: {source_url}
Source ZIP SHA256: {sha(source.read_bytes())}

Preserve all notices. Inherited dietlibc corresponding source remains unverified; see SOURCE.txt, THIRD_PARTY_NOTICES.md and the included provenance records. Experimental status does not resolve the source audit.
'''
metadata = dict(build_info, distribution='camera-update-only; no source archive or FIR',
                matching_source_url=source_url, matching_source_commit=commit)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for n,b in payload.items():z.writestr(n,b)
    for n,b in original.items():
        if n in {'COPYING','AI_ASSISTANCE.md','THIRD_PARTY_NOTICES.md','GAMES_TH.md','UPDATE_TH.md'} or n.startswith('release/v3r2/'):
            z.writestr(n,b)
    z.writestr('INSTALL_TH.md',update_th)
    z.writestr('INSTALL_EN.md',update_en)
    z.writestr('BUILD_INFO.json',json.dumps(metadata,indent=2)+'\n')
    z.writestr('SOURCE.txt',f'Matching source ZIP: {source_url}\nSHA256: {sha(source.read_bytes())}\nTagged source: https://github.com/{repo}/tree/{release}\nInherited dietlibc corresponding source remains unverified; see THIRD_PARTY_NOTICES.md and release/v3r2/PROVENANCE.md.\n')
    z.writestr('PAYLOAD_SHA256SUMS',''.join(f'{sha(b)}  {n}\n' for n,b in sorted(payload.items())))
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    assert not any(n.startswith('SOURCE/') or n.lower().endswith(('.zip','.fir')) for n in z.namelist())
    for n,b in payload.items():assert z.read(n)==b,n
    for n in ['COPYING','THIRD_PARTY_NOTICES.md','SOURCE.txt','INSTALL_TH.md','INSTALL_EN.md']:assert z.read(n)
info = {'version':release,'target':'600D.102','status':'Public Experimental',
        'audience':'Cameras already running ML; not first installation',
        'project':'FIRMWARE ADD-ON Thai-Menu','project_website':'https://itsamachom.github.io/eos_rom_mlv_modifly/',
        'firmware_source_commit':commit,'full_zip_sha256':sha(full.read_bytes()),
        'autoexec_sha256':sha(payload['autoexec.bin']),
        'camera':{'filename':zip_path.name,'path':str(zip_path.relative_to(root)),'bytes':zip_path.stat().st_size,'sha256':sha(zip_path.read_bytes())},
        'source':{'filename':source.name,'url':source_url,'bytes':source.stat().st_size,'sha256':sha(source.read_bytes())},
        'verified':['ZIP CRC','all autoexec/ML bytes match tagged Full ZIP','not a first-install package','source ZIP identity','licenses retained'],
        'camera_tested':False,'qemu_tested':False,'inherited_dependency_source_verified':False}
(out/'DOWNLOAD_INFO.json').write_text(json.dumps(info,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f'{item["sha256"]}  {item["filename"]}\n' for item in [info['camera'],info['source']]))
print('PASS camera-only ZIP: runtime identity, CRC, no nested source ZIP or FIR, matching source and retained notices')
print(json.dumps(info,indent=2))
