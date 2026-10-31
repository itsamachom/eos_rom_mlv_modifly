"""Regression checks for menu inventory and camera-property availability semantics."""
import re
import sys
import json
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
h=(root/'firmware/src/photo-menu-600d.h').read_text()
old=subprocess.check_output(['git','show','ca97d4ea27d08fee3698c5c8ac2ee0753b75a2f2:firmware/src/photo-menu-600d.h'],cwd=root,text=True)
parse=lambda s: set(re.findall(r'\{"[^"]+", "([^"]+)", ("[^"]+"|NULL)\}',s))
assert parse(old)-{('Shoot','"Silent Picture"')} <= parse(h)
assert ('Shoot','"Silent Picture"') not in parse(h)
for label in ['Histogram','Waveform','Time-lapse','Bracketing','zebra settings','Bitrate (CBR)']:
    assert '{"'+label+'",' in h
modules=(root/'firmware/platform/600D.102/modules.included').read_text().splitlines()
assert 'silent' not in modules and {'arkanoid','lua'} <= set(modules)
for game in ['pong.lua','sokoban.lua']:
    assert (root/'firmware/scripts'/game).read_bytes()==subprocess.check_output(['git','show','359f828:firmware/scripts/'+game],cwd=root)
# Rendering assets must regenerate identically when the authoring tools are available.
asset=root/'firmware/data/photo_thai/PHOTO_TH.BIN'
before=asset.read_bytes()
subprocess.run([sys.executable,str(root/'tools/generate_photo_thai.py')],check=True)
assert asset.read_bytes()==before
# Restore every existing translation except the explicitly requested names.
old_lex=json.loads((root/'translations/photo_th.original.json').read_text())
lex=json.loads((root/'translations/photo_th.json').read_text())
renamed={'Intervalometer','Advanced Bracket','Zebras','Histogram','Waveform'}
for key,value in old_lex.items():
    if key not in renamed: assert lex[key]==value, key
assert 'PHOTO_PAGE("Games", "G", photo_games)' in h
assert 'int h=30*w/t->width' not in (root/'firmware/src/photo-thai-600d.h').read_text()
print('PASS retained menu inventory, original translations/font sizes, separate Games category, original games and reproducible atlas')
# Compile the actual production property-handler body, not a duplicated formula.
import tempfile
body=(root/'firmware/src/propvalues.c').read_text().split('PROP_HANDLER(PROP_SHUTTER_COUNTER)\n{',1)[1].split('\n}',1)[0]
program='#include <assert.h>\nunsigned shutter_count_valid, shutter_count, shutter_count_plus_lv_actuations;\nvoid handler(unsigned *buf, unsigned len) {\n'+body+'\n}\nint main(void) {\n unsigned b[2]={10,20};handler(b,4);assert(!shutter_count_valid);\n b[0]=20;b[1]=10;handler(b,8);assert(!shutter_count_valid);\n b[0]=0xffffffff;b[1]=0xffffffff;handler(b,8);assert(!shutter_count_valid);\n b[0]=0;b[1]=0;handler(b,8);assert(shutter_count_valid && shutter_count==0);\n b[0]=123;b[1]=130;handler(b,8);assert(shutter_count==123 && shutter_count_plus_lv_actuations==130);\n}\n'
with tempfile.TemporaryDirectory() as d:
    c=Path(d)/'counter.c';c.write_text(program)
    subprocess.run(['gcc','-Wall','-Wextra','-Werror',str(c),'-o',d+'/counter'],check=True)
    subprocess.run([d+'/counter'],check=True)
print('PASS production shutter-property handler rejects short/invalid values and accepts real zero/valid counts')
