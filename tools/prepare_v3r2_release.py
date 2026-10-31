"""Stage unchanged v3r2 artifacts plus release docs; never publish or claim ready."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path('/workspace/release-staging/v3r2'))
args=parser.parse_args()
output=args.output.resolve()
if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
    raise SystemExit('Commit release documentation before staging so docs_commit identifies the included files.')
if output.exists():
    raise SystemExit(f'Refusing to replace existing staging directory: {output}; choose a new --output.')
delivery=root/'deliveries/photo-ui-v3r2-full'
digest=lambda b:hashlib.sha256(b).hexdigest()
expected={}
for line in (delivery/'SHA256SUMS').read_text().splitlines():
    sha,name=line.split('  ',1)
    assert Path(name).name==name,name
    assert digest((delivery/name).read_bytes())==sha,name
    expected[name]=sha
info=json.loads((delivery/'BUILD_INFO.json').read_text())
commit=info['source_commit']
assert commit=='5f543089565c1574606ea2436315e6ea5419ce70'
full=delivery/'600D-102-PHOTO-UI-v3r2-FULL-EXPERIMENTAL.zip'
source=delivery/'600D-PHOTO-UI-v3r2-source.zip'
with zipfile.ZipFile(full) as z:
    assert z.testzip() is None
    assert digest(z.read('autoexec.bin'))==info['autoexec_sha256']
    assert z.read('SOURCE/'+source.name)==source.read_bytes()
    assert digest(z.read('ML-SETUP.FIR'))==info['installer_sha256']
    for line in z.read('PAYLOAD_SHA256SUMS').decode().splitlines():
        sha,name=line.split('  ',1);assert digest(z.read(name))==sha,name
# Every distributed source file must match its recorded source commit, not HEAD.
raw=subprocess.check_output(['git','ls-tree','-rz',commit],cwd=root)
tree={rec.split(b'\t',1)[1].decode():rec.split(b'\t',1)[0].decode().split()[2]
      for rec in raw.split(b'\0') if rec}
source_files=0
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    for name in z.namelist():
        if name.endswith('/'):continue
        rel=name.removeprefix('600D-photo-ui-v3r2-source/')
        assert rel!=name and rel in tree,name
        data=z.read(name)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[rel],name
        source_files+=1
notice_paths=['LICENSE','README.md','THIRD_PARTY_NOTICES.md','AI_ASSISTANCE.md','CONTRIBUTING.md',
              'PHOTO_UI_V3R2.md','PHOTO_UI_V3R2_INSTALL_TH.md','GAMES_V3R2_TH.md',
              'firmware/LLM_POLICY.md','firmware/COPYING','firmware/doc/CREDITS.txt',
              'assets/fonts/noto-sans-thai/SOURCE.md','assets/fonts/noto-sans-thai/OFL.txt',
              'tools/prepare_v3r2_release.py','tools/publish_v3r2_release.py']
notice_paths += [p.relative_to(root).as_posix() for p in sorted((root/'release/v3r2').rglob('*')) if p.is_file()]
for rel in notice_paths:assert (root/rel).is_file(),rel
assert (root/'LICENSE').read_bytes()==(root/'firmware/COPYING').read_bytes()
state=json.loads((root/'release/v3r2/READINESS.json').read_text())
output.parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='v3r2-stage-',dir=output.parent) as tmp:
    stage=Path(tmp)/'assets';stage.mkdir()
    for name in expected:shutil.copyfile(delivery/name,stage/name)
    docs=stage/'600D-PHOTO-UI-v3r2-release-docs-licenses.zip'
    with zipfile.ZipFile(docs,'w',zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(set(notice_paths)):z.write(root/rel,rel)
    report={'release':'v3r2','payload_source_commit':commit,'source_archive_files_verified':source_files,
            'payload_unchanged':True,'source_archive_unchanged':True,'blockers':state['blockers'],
            'publication_ready':not state['blockers'],'published':False,
            'docs_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()}
    (stage/'RELEASE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(p for p in stage.iterdir() if p.is_file())
    (stage/'SHA256SUMS').write_text(''.join(f'{digest(p.read_bytes())}  {p.name}\n' for p in files))
    shutil.move(str(stage),output)
print(json.dumps({'staging':str(output),'source_files_verified':source_files,'publication_ready':report['publication_ready'],
                  'blockers':[b['id'] for b in state['blockers']]},indent=2))
