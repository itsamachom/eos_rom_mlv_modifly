"""Audit manual coverage against the actual 600D-enabled menu declarations."""
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_menu_catalog import preprocess

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'website-content/manual-th.json').read_text())
manual = {x['key']: x for x in data['items']}
assert len(manual) == 43
front = (root / 'firmware/src/photo-menu-600d.h').read_text()
rows = [(m[1],m[2],m[4]) for m in re.finditer(r'\{"([^"]+)", "([^"]+)", ("([^"]+)"|NULL)\}', front)]
assert len(rows) == 44 and {r[0] for r in rows} == set(manual)
assert data['release'] == (root / 'scripts/photo-ui-version.txt').read_text().strip()
files = ['shoot.c','focus.c','picstyle.c','zebra.c','cropmarks.c','movtweaks.c','bitrate.c','menu.c','debug.c','photo-camera-info-600d.h', '../modules/dual_iso/dual_iso.c', '../modules/ettr/ettr.c']
tables = {f: preprocess(f) for f in files}
arrays = {name: entries for table in tables.values() for name,entries in table.items()}
# Root entries use the same declarations audited for the screenshot gallery.
registry = json.loads((root/'docs/menu-previews/v3r5/manifest.json').read_text())['source_registry']
by_name = {n['name']:n for n in registry}
for f, name in [('../modules/dual_iso/dual_iso.c','dual_iso_menu'),('../modules/ettr/ettr.c','ettr_menu')]:
 for node in tables[f][name]: by_name[node['name']] = node
checked=0
for key,menu,entry in rows:
 if not entry or entry not in by_name: continue
 node=by_name[entry]
 children=node.get('children',arrays.get(node.get('children_ref'),[]))
 expected={c['name'] for c in children}
 actual=set(manual[key]['options'])
 assert actual==expected,(key,'missing',expected-actual,'extra',actual-expected)
 checked+=len(expected)
text=(root/'MANUAL_TH.md').read_text()
assert 'Exposure (Tv,Ae)' in text and 'การคร่อมรูรับแสงใช้ DOF' in text
assert 'ไม่ใช่จำนวนไฟล์ภาพที่ถ่ายใน Live View โดยตรง' in text
assert 'ไม่มีโมดูล pong.mo' in text and 'ไม่มีโมดูล sokoban.mo' in text
assert text.count('### โมดูลเสริม (Modules)') == 2
assert len(re.findall(r'^### ',text,re.M)) > 44
print(f'PASS 44 menu entries; {checked} source-defined child explanations incl. Dual ISO/ETTR; current release; Tv/Ae versus Av; Live View counter meaning; real game module names')
