"""Package the version selected by scripts/photo-ui-version.txt, preserving older deliveries.

Build first with scripts/build-photo-ui.sh and run the documented host checks.
Source ZIP contains exact working files, rather than claiming HEAD alone built them.
"""
import functools
import hashlib
import json
import operator
from pathlib import Path
import re
import struct
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
release = (root / 'scripts/photo-ui-version.txt').read_text().strip()
assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*', release)
version = f'PHOTO-UI-{release}.600D.102'
notes = root/f'PHOTO_UI_{release.upper()}.md'
assert notes.is_file(), 'Add release notes for this version before packaging.'
out = root / f'deliveries/photo-ui-{release}-full'
out.mkdir(parents=True, exist_ok=True)
source = out / f'600D-PHOTO-UI-{release}-source.zip'
full = out / f'600D-102-PHOTO-UI-{release}-FULL-EXPERIMENTAL.zip'
assert not any(p.exists() for p in [source, full, out/'BUILD_INFO.json']), 'Delivery exists; bump scripts/photo-ui-version.txt first.'
subprocess.run(['git', 'ls-files', '--error-unmatch', 'scripts/photo-ui-version.txt'], cwd=root, check=True, stdout=subprocess.DEVNULL)
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
sha256 = lambda data: hashlib.sha256(data).hexdigest()
with zipfile.ZipFile(root/'firmware/platform/600D.102/build/magiclantern.zip') as z:
    assert z.testzip() is None
    payload = {name: z.read(name) for name in z.namelist() if not name.endswith('/')}
binary = payload['autoexec.bin']
assert version.encode() in binary, 'Build version differs from version file; rebuild first.'
assert len(binary) % 4 == 0
assert functools.reduce(operator.xor, struct.unpack('<%dI' % (len(binary)//4), binary), 0) == 0
assert payload['ML/data/PHOTO_TH.BIN'] == (root/'firmware/data/photo_thai/PHOTO_TH.BIN').read_bytes()
assert sha256(payload['ML-SETUP.FIR']) == '7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3'
assert {Path(n).stem for n in payload if n.endswith('.mo')} == {'adv_int','autoexpo','deflick','dual_iso','ettr','file_man','img_name','pic_view','arkanoid','lua'}
# Only indexed project sources: do not sweep local files or build outputs into the archive.
indexed = subprocess.check_output(['git','ls-files','-z'], cwd=root, text=True).split('\0')
files = sorted(n for n in indexed if n and (n.split('/')[0] in {'firmware','scripts','tests','tools','assets','translations','previews','release'} or '/' not in n or n=='baseline-600d-102/bootstrap-toolchain.sh'))
prefix = f'600D-photo-ui-{release}-source/'
with zipfile.ZipFile(source, 'w', zipfile.ZIP_DEFLATED) as z:
    for name in files:
        z.write(root/name, prefix+name)
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    for name in files:
        assert z.read(prefix+name) == (root/name).read_bytes()
info = {
    'project':'FIRMWARE ADD-ON Thai-Menu',
    'project_website':'https://itsamachom.github.io/eos_rom_mlv_modifly/',
    'distribution_status':'Public Experimental; not Stable or source-audit complete',
    'version': version, 'target':'600D.102', 'base_commit':base,
    'source_state':'Exact indexed working files in source ZIP; base commit plus any working changes. Base alone is not necessarily the build source.',
    'source_zip_sha256':sha256(source.read_bytes()), 'autoexec_sha256':sha256(binary),
    'camera_tested':False, 'qemu_tested':False, 'installer_modified':False,
    'packager_checks':['build-version identity','ZIP CRC','autoexec XOR','Thai atlas identity','module inventory','unchanged installer','exact working-source bytes'],
    'dependency_source_status':'Inherited dietlibc corresponding source remains unverified; see included release/v3r2/PROVENANCE.md and READINESS.json.',
    'ai_assistance':'Codex/LLM-assisted fork; see AI_ASSISTANCE.md and release notes.',
}
with zipfile.ZipFile(full, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, data in payload.items():
        z.writestr(name, data)
    z.write(source, 'SOURCE/'+source.name)
    z.writestr('SOURCE/changes-from-base.patch', subprocess.check_output(['git','diff','--binary','HEAD'], cwd=root))
    z.writestr('BUILD_INFO.json', json.dumps(info,indent=2)+'\n')
    for path,name in [('PHOTO_UI_V3R2_INSTALL_TH.md','INSTALL_TH.md'),('GAMES_V3R2_TH.md','GAMES_TH.md'),('firmware/COPYING','COPYING'),('AI_ASSISTANCE.md','AI_ASSISTANCE.md'),('THIRD_PARTY_NOTICES.md','THIRD_PARTY_NOTICES.md')]:
        z.write(root/path, name)
    z.write(notes, 'UPDATE_TH.md')
    for name in files:
        if name.startswith('release/v3r2/'):
            z.write(root/name,name)
    z.writestr('PAYLOAD_SHA256SUMS',''.join(f'{sha256(data)}  {name}\n' for name,data in sorted(payload.items())))
with zipfile.ZipFile(full) as z:
    assert z.testzip() is None
    for name,data in payload.items():
        assert z.read(name) == data
    assert sha256(z.read('SOURCE/'+source.name)) == info['source_zip_sha256']
info['full_zip_sha256'] = sha256(full.read_bytes())
(out/'BUILD_INFO.json').write_text(json.dumps(info,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f'{sha256(p.read_bytes())}  {p.name}\n' for p in [full,source,out/'BUILD_INFO.json']))
print('PASS package version, source identity, module inventory, CRC and XOR')
print(full)
print(info['full_zip_sha256'])
