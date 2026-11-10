"""Publish a new documentation revision without changing firmware or overwriting existing ZIPs."""
from pathlib import Path
import copy
import hashlib
import json
import re
import zipfile

root=Path(__file__).resolve().parents[1]
version=(root/'scripts/photo-ui-version.txt').read_text().strip()
folder=root/f'downloads/{version}'
meta=json.loads((folder/'DOWNLOAD_INFO.json').read_text())
revision=meta.get('documentation_revision',0)+1
guide=(root/'INSTALL_TH.md').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
raw='https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/site/eos-600d-bilingual/'
def revised(name):
    return re.sub(r'(-doc\d+)?\.zip$',f'-doc{revision}.zip',name)
def rewrite_zip(old,new,changes):
    assert not new.exists(),'Do not overwrite a published documentation revision.'
    new.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(old) as source,zipfile.ZipFile(new,'w') as out:
        assert source.testzip() is None
        for item in source.infolist():out.writestr(item,changes.get(item.filename,source.read(item.filename)))
    with zipfile.ZipFile(new) as z:assert z.testzip() is None
old_source=root/meta['source']['path'] if 'path' in meta['source'] else root/f'deliveries/photo-ui-{version}-full'/meta['source']['filename']
assert sha(old_source.read_bytes())==meta['source']['sha256']
new_source=folder/'source'/revised(meta['source']['filename'])
with zipfile.ZipFile(old_source) as z:
    entries=[n for n in z.namelist() if n.count('/')==1 and n.endswith('/INSTALL_TH.md')]
    assert len(entries)==1
rewrite_zip(old_source,new_source,{entries[0]:guide})
new_source_info={'filename':new_source.name,'path':str(new_source.relative_to(root)),
                 'url':raw+str(new_source.relative_to(root)),'bytes':new_source.stat().st_size,'sha256':sha(new_source.read_bytes())}
updated=copy.deepcopy(meta)
for kind in ['first_install','camera']:
    old=root/meta[kind]['path'];assert sha(old.read_bytes())==meta[kind]['sha256']
    new=old.with_name(revised(old.name))
    with zipfile.ZipFile(old) as z:
        build=json.loads(z.read('BUILD_INFO.json'))
        build.update(documentation_revision=revision,install_th_sha256=sha(guide),
                     original_source_zip_sha256=build.get('original_source_zip_sha256',build['source_zip_sha256']),
                     source_zip_sha256=new_source_info['sha256'],matching_source_url=new_source_info['url'])
        text=z.read('SOURCE.txt').decode().replace(meta['source']['url'],new_source_info['url']).replace(meta['source']['sha256'],new_source_info['sha256'])
    rewrite_zip(old,new,{'INSTALL_TH.md':guide,'BUILD_INFO.json':(json.dumps(build,indent=2)+'\n').encode(),'SOURCE.txt':text.encode()})
    with zipfile.ZipFile(old) as a,zipfile.ZipFile(new) as b:
        assert b.read('INSTALL_TH.md')==guide
        for n in a.namelist():
            if n=='autoexec.bin' or n.startswith('ML/') or n.lower().endswith('.fir'):assert a.read(n)==b.read(n),n
    updated[kind]={'filename':new.name,'path':str(new.relative_to(root)),'bytes':new.stat().st_size,'sha256':sha(new.read_bytes())}
updated.update(source=new_source_info,documentation_revision=revision,install_th_sha256=sha(guide),firmware_changed=False)
(folder/'DOWNLOAD_INFO.json').write_text(json.dumps(updated,indent=2)+'\n')
(folder/'SHA256SUMS').write_text(''.join(f'{updated[key]["sha256"]}  {updated[key]["filename"]}\n' for key in ['first_install','camera','source']))
print('PASS documentation revision',revision,': attached guide exact in source and both packages; firmware and FIR unchanged')
print('Guide SHA256:',sha(guide))
