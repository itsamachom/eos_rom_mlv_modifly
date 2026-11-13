"""Compare shipped C catalog to audited original values, including source ISO rounding."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'research/jpeg-tones/UPSTREAM_ORIGINAL_CATALOG.json').read_text())
header=(root/'firmware/src/photo-tone-recipes-600d.h').read_text()
rows=re.findall(r'^    \{(.*)\},$',header,re.M)
fields=('name','brand','key','process','group','style','contrast','sharpness','saturation','color_tone','kelvin','gm','ba','box_iso','camera_iso','raw_iso','effective_iso')
assert len(rows)==len(catalog['recipes'])==72
keys=set()
for line,r in zip(rows,catalog['recipes']):
    assert json.loads('['+line+']')==[r[k] for k in fields],r['key']
    assert r['key'] not in keys;keys.add(r['key'])
    raw=72;i=100
    while i<r['camera_iso']:raw+=8;i*=2
    assert (raw,i)==(r['raw_iso'],r['effective_iso'])
    assert r['style'] in (0x81,0x83,0x86) and r['group'] in range(4)
    assert -4<=r['contrast']<=4 and 0<=r['sharpness']<=7
    assert -4<=r['saturation']<=4 and -4<=r['color_tone']<=4
print('PASS 72 original names/ISO/WB/Picture Style values, no deduplication, upstream whole-stop ISO conversion')
