"""Verify the actual captured active-name panel survives browsing and detects drift."""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]/'previews/jpeg-tones'
for lang in ('th','en'):
 def panel(kind):
  with Image.open(root/f'tone-{kind}-{lang}.png') as im:return im.crop((420,393,708,465)).tobytes()
 assert panel('active')==panel('browsing'),lang
 assert panel('active')!=panel('changed'),lang
print('PASS framed active-film panel stays pinned while browsing; external Canon change removes active marking in both languages')
