"""Audit label/preset mapping and independently captured on-screen label identities."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
root=Path(__file__).resolve().parents[1]
recipes=json.loads((root/'research/jpeg-tones/UPSTREAM_ORIGINAL_CATALOG.json').read_text())['recipes']
labels=json.loads((root/'research/film-labels/CATALOG.json').read_text())['labels']
header=(root/'firmware/src/photo-film-labels-600d.h').read_text()
keys=re.findall(r'\}, /\* ([a-z0-9]+) \*/',header)
assert keys==[r['key'] for r in recipes]==[r['key'] for r in labels]
assert len(keys)==72
for r,l in zip(recipes,labels):
 assert r['name']==l['name'] and r['brand']==l['brand']
 assert l['word'] and l['num_s'] and l['reference_status']
 assert l['style'] in (0,1,2)
 # All side-name characters fit without elision in the actual 20-character field.
 assert len(r['name'])<=20 and len(r['brand'])<=20
rows={l['key']:l for l in labels}
assert rows['gold200']['bg'][0]==2 and rows['gold200']['band'][0]==3
assert rows['superia400']['bg'][0]==6 and rows['ektar100']['bg'][0]==5
assert rows['kodak2383']['num_s']=='2383' # stock identifier, not ISO
assert 'not a retail' in rows['fuji3513']['reference_status']
# Compare label-only crops, excluding the menu title / stock name / status text.
# A selection-index bug or generic category graphic cannot satisfy 72 identities.
seen={};positions={g:0 for g in range(4)}
for i,r in enumerate(recipes):
 pos=positions[r['group']];positions[r['group']]+=1
 x=24+234*(pos%3)
 crops=[]
 for lang in ('th','en'):
  p=root/f'previews/jpeg-tones/tones-{lang}-{i+1:02d}.png'
  with Image.open(p) as im:
   assert im.size==(720,510)
   crops.append(im.crop((x+54,30+175,x+146,30+309)).tobytes())
 assert crops[0]==crops[1],r['key']
 digest=hashlib.sha256(crops[0]).hexdigest()
 assert digest not in seen,(r['key'],seen.get(digest))
 seen[digest]=r['key']
print('PASS 72 exact label/preset identities, complete vertical names, 72 different rendered labels, same art in Thai/English')
