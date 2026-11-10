"""Package separate first-install/update ZIPs and matching source metadata. No installer rebuild."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

root=Path(__file__).resolve().parents[1]
release=(root/'scripts/photo-ui-version.txt').read_text().strip()
assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*',release)
raw='https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly'
folder=root/f'deliveries/photo-ui-{release}-full'
full=folder/f'600D-102-PHOTO-UI-{release}-FULL-EXPERIMENTAL.zip'
source=folder/f'600D-PHOTO-UI-{release}-source.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
tag=subprocess.run(['git','rev-parse','--verify',f'refs/tags/{release}^{{commit}}'],cwd=root,text=True,capture_output=True)
commit=tag.stdout.strip() if tag.returncode==0 else None
if commit:
    subprocess.run(['git','diff','--exit-code',release,'--',str(full.relative_to(root)),str(source.relative_to(root))],cwd=root,check=True)
with zipfile.ZipFile(full) as z:
    assert z.testzip() is None
    original={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
info=json.loads(original['BUILD_INFO.json'])
assert info['version']==f'PHOTO-UI-{release}.600D.102'
assert original['SOURCE/'+source.name]==source.read_bytes()
assert sha(source.read_bytes())==info['source_zip_sha256']
for line in original['PAYLOAD_SHA256SUMS'].decode().splitlines():
    expected,name=line.split('  ',1);assert sha(original[name])==expected,name
runtime={n:b for n,b in original.items() if n=='autoexec.bin' or n.startswith('ML/')}
assert sha(runtime['autoexec.bin'])==info['autoexec_sha256']
fir=original['ML-SETUP.FIR']
fir_hash='7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3'
assert len(fir)==65852 and sha(fir)==fir_hash
assert fir==(root/'firmware/platform/600D.102/ML-SETUP.FIR').read_bytes()
source_url=f'{raw}/{release}/{source.relative_to(root)}'
out=root/f'downloads/{release}'
outputs={}
for kind,suffix in [('first_install','FIRST-INSTALL'),('camera','UPDATE')]:
    dest=out/f'{kind}/600D-102-Thai-Menu-{release}-{suffix}.zip'
    assert not dest.exists(),'Do not overwrite a published download.'
    dest.parent.mkdir(parents=True,exist_ok=True)
    payload=dict(runtime)
    if kind=='first_install':payload['ML-SETUP.FIR']=fir
    metadata=dict(info,distribution=suffix,installer_included=kind=='first_install',
                  installer_sha256=fir_hash if kind=='first_install' else None,
                  matching_source_url=source_url,matching_source_tag=release)
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in payload.items():z.writestr(n,b)
        for n,b in original.items():
            if n in {'COPYING','AI_ASSISTANCE.md','THIRD_PARTY_NOTICES.md','GAMES_TH.md','UPDATE_TH.md','INSTALL_TH.md','INSTALL_EN.md','INSTALL_UPSTREAM.txt'} or n.startswith('release/v3r2/'):
                z.writestr(n,b)
        z.writestr('BUILD_INFO.json',json.dumps(metadata,indent=2)+'\n')
        z.writestr('SOURCE.txt',f'Project: https://itsamachom.github.io/eos_rom_mlv_modifly/\nMatching source: {source_url}\nSource SHA256: {sha(source.read_bytes())}\nInherited dietlibc source remains unverified; see included provenance and notices.\n')
        z.writestr('PAYLOAD_SHA256SUMS',''.join(f'{sha(b)}  {n}\n' for n,b in sorted(payload.items())))
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        assert not any(n.startswith('SOURCE/') or n.lower().endswith('.zip') for n in z.namelist())
        for n,b in runtime.items():assert z.read(n)==b,n
        if kind=='first_install':assert sha(z.read('ML-SETUP.FIR'))==fir_hash
        else:assert not any(n.lower().endswith('.fir') for n in z.namelist())
        for n in ['COPYING','SOURCE.txt','INSTALL_TH.md','INSTALL_EN.md','INSTALL_UPSTREAM.txt']:assert z.read(n)
    outputs[kind]={'filename':dest.name,'path':str(dest.relative_to(root)),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
outputs['source']={'filename':source.name,'url':source_url,'bytes':source.stat().st_size,'sha256':sha(source.read_bytes())}
metadata={'version':release,'target':'600D.102','status':'Public Experimental',
          'audience':'First installation or existing ML: choose the matching package',
          'project':'FIRMWARE ADD-ON Thai-Menu','project_website':'https://itsamachom.github.io/eos_rom_mlv_modifly/',
          'firmware_source_tag':release,'firmware_source_commit':commit,'source_base_commit':info['base_commit'],
          'full_zip_sha256':sha(full.read_bytes()),'autoexec_sha256':sha(runtime['autoexec.bin']),
          'installer_sha256':fir_hash,**outputs,
          'verified':['ZIP CRC','runtime bytes match Full ZIP in both packages','original installer size/hash and source-tree identity','FIR absent in update','source ZIP identity','licenses and upstream instructions retained'],
          'camera_tested':False,'first_install_hardware_tested':False,'qemu_tested':False,'installer_rebuilt':False,'inherited_dependency_source_verified':False}
(out/'DOWNLOAD_INFO.json').write_text(json.dumps(metadata,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f'{item["sha256"]}  {item["filename"]}\n' for item in outputs.values()))
print('PASS first-install and update archives: same firmware, original verified FIR only in first-install, matching source and instructions')
print(json.dumps(outputs,indent=2))
