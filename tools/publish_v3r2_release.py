"""Publish a v3r2 fork prerelease only after source/network release gates pass."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
mode=p.add_mutually_exclusive_group(required=True)
mode.add_argument('--check',action='store_true')
mode.add_argument('--publish',action='store_true')
p.add_argument('--staging',type=Path,default=Path('/workspace/release-staging/v3r2'))
a=p.parse_args()
s=json.loads((root/'release/v3r2/READINESS.json').read_text())
if s['blockers']:
    print('BLOCKED: no tag, GitHub release or external write was attempted.')
    for b in s['blockers']:print(f"- {b['id']}: {b['detail']}")
    sys.exit(2)
assert s['intended_prerelease'] is True
assert all(s['checks'].values()),'Unmet release checks'
for line in (a.staging/'SHA256SUMS').read_text().splitlines():
    sha,name=line.split('  ',1);assert Path(name).name==name
    assert hashlib.sha256((a.staging/name).read_bytes()).hexdigest()==sha,name
report=json.loads((a.staging/'RELEASE_AUDIT.json').read_text())
assert report['publication_ready'] and not report['blockers'],'Regenerate staging after gate resolution'
print('Release gates and staged checksums passed; target is a fork prerelease.')
if a.check:sys.exit(0)
repo=s['repository'];tag=s['release']
assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip(),'Commit changes before publication'
# Test the configured API normally. Do not remove proxies or replace credentials.
subprocess.run(['gh','api',f'repos/{repo}','--jq','.full_name'],cwd=root,check=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
subprocess.run(['git','push','origin','HEAD'],cwd=root,check=True)
# Never overwrite an existing tag or release. Annotation is not a signing claim.
subprocess.run(['git','tag','-a',tag,'-m','Photo UI v3r2 / Canon 600D 1.0.2 / experimental independent fork',head],cwd=root,check=True)
subprocess.run(['git','push','origin',f'refs/tags/{tag}'],cwd=root,check=True)
assets=[str(path) for path in sorted(a.staging.iterdir()) if path.is_file()]
subprocess.run(['gh','release','create',tag,*assets,'--repo',repo,'--verify-tag',
                '--title','Photo UI v3r2 — Canon 600D 1.0.2 (Experimental fork)',
                '--notes-file',str(root/'release/v3r2/RELEASE_NOTES.md'),
                '--prerelease','--latest=false'],cwd=root,check=True)
subprocess.run(['gh','release','view',tag,'--repo',repo,'--json','url,isDraft,isPrerelease,tagName'],cwd=root,check=True)
