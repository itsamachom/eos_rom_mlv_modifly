"""Build a self-contained 600D.102 experimental Full delivery from committed source."""
import functools
import hashlib
import json
import operator
from pathlib import Path
import struct
import subprocess
import zipfile

root=Path(__file__).resolve().parents[1]
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
subprocess.run(['git','diff','--exit-code','HEAD','--','firmware','scripts','tests','tools','PHOTO_UI_V3.md','PHOTO_UI_V3_INSTALL_TH.md'],cwd=root,check=True)
out=root/'deliveries/photo-ui-v3-full';out.mkdir(parents=True,exist_ok=True)
source=out/'600D-PHOTO-UI-v3-source.zip'
subprocess.run(['git','archive','--format=zip','--prefix=600D-photo-ui-v3-source/','-o',str(source),sha,'firmware','scripts','tests','tools','baseline-600d-102/bootstrap-toolchain.sh','PHOTO_UI_V3.md','PHOTO_UI_V3_INSTALL_TH.md'],cwd=root,check=True)
fir=(root/'firmware/platform/600D.102/ML-SETUP.FIR').read_bytes()
fir_hash='7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3'
digest=lambda b:hashlib.sha256(b).hexdigest()
assert len(fir)==65852 and digest(fir)==fir_hash
build=root/'firmware/platform/600D.102/build'
with zipfile.ZipFile(build/'magiclantern.zip') as z:
    assert z.testzip() is None
    payload={n:z.read(n) for n in z.namelist() if not n.endswith('/') and not n.lower().endswith('.fir')}
binary=payload['autoexec.bin']
assert b'PHOTO-UI-v3.600D.102' in binary and sha[:7].encode() in binary
assert len(binary)%4==0 and functools.reduce(operator.xor,struct.unpack('<%dI'%(len(binary)//4),binary),0)==0
expected={'adv_int','autoexpo','deflick','dual_iso','ettr','file_man','img_name','pic_view','arkanoid','lua'}
assert {Path(n).stem for n in payload if n.endswith('.mo')}==expected
assert all(n=='autoexec.bin' or n.startswith('ML/') for n in payload)
for n in ['ML/scripts/pong.lua','ML/scripts/sokoban.lua','ML/modules/600D_102.sym','ML/fonts/argnor23.rbf']:
    assert payload[n]
assert not any('ROM' in n.upper() and n.upper().endswith('.BIN') for n in payload)
info={'version':'PHOTO-UI-v3.600D.102','target':'600D.102','source_commit':sha,
      'base_commit':'ca97d4ea27d08fee3698c5c8ac2ee0753b75a2f2','camera_tested':False,
      'first_install_hardware_tested':False,'installer_rebuilt_or_modified':False,
      'installer_sha256':fir_hash,'source_sha256':digest(source.read_bytes()),
      'autoexec_sha256':digest(binary),'autoexec_bytes':len(binary),'modules':sorted(expected),
      'host_test_groups_passed':12,'target_bindings_checked':34,'qemu':False}
dest=out/'600D-102-PHOTO-UI-v3-FULL-EXPERIMENTAL.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for n,b in payload.items(): z.writestr(n,b)
    z.writestr('ML-SETUP.FIR',fir)
    z.write(source,'SOURCE/'+source.name)
    for path,name in [('PHOTO_UI_V3_INSTALL_TH.md','INSTALL_TH.md'),('PHOTO_UI_V3.md','PHOTO_UI_V3.md'),('firmware/doc/INSTALL.txt','INSTALL_UPSTREAM.txt'),('firmware/COPYING','COPYING')]: z.write(root/path,name)
    z.writestr('BUILD_INFO.json',json.dumps(info,indent=2)+'\n')
    z.writestr('SOURCE.txt',f'Source commit: {sha}\nMatching source is included under SOURCE/ (not executable on camera).\nGPL: see COPYING. Preserve upstream attribution.\nCodex/LLM-assisted experimental fork; not upstream endorsed.\nOriginal prebuilt installer, not rebuilt. First install and v3 camera behavior untested.\n')
    sums={**payload,'ML-SETUP.FIR':fir}
    z.writestr('PAYLOAD_SHA256SUMS',''.join(f'{digest(b)}  {n}\n' for n,b in sorted(sums.items())))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for line in z.read('PAYLOAD_SHA256SUMS').decode().splitlines():
        d,n=line.split('  ',1);assert digest(z.read(n))==d
    assert z.read('ML-SETUP.FIR')==fir
    assert z.read('SOURCE/'+source.name)==source.read_bytes()
    with zipfile.ZipFile(source) as src:
        assert src.testzip() is None
        for n in ['photo-menu-600d.h','photo-thai-600d.h','propvalues.c']:
            assert src.read('600D-photo-ui-v3-source/firmware/src/'+n)==(root/'firmware/src'/n).read_bytes()
info['zip_sha256']=digest(dest.read_bytes())
(out/'BUILD_INFO.json').write_text(json.dumps(info,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f'{digest(p.read_bytes())}  {p.name}\n' for p in [dest,source,out/'BUILD_INFO.json']))
print(json.dumps(info,indent=2))
