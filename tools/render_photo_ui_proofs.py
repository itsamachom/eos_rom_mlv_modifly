"""Render host layout proofs using production Thai masks and shipped RBF glyphs.

All camera values in these host fixtures are simulated. These are not photos
or captures from Canon hardware. Requires a C compiler and Pillow.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    env=dict(os.environ,PHOTO_PROOF_RBF_DIR=str(root/'firmware/data/fonts'),PHOTO_PROOF_OUT=tmp)
    subprocess.run(['bash','tests/run-photo-menu-tests.sh'],cwd=root,env=env,check=True)
    palette={0:(0,0,0),1:(255,255,255),2:(20,75,150),3:(255,160,50),4:(80,220,255)}
    for i in range(10,41):palette[i]=(max(0,(i-10)*7),)*3
    out=Image.new('RGB',(1440,1020),'#111111');draw=ImageDraw.Draw(out)
    for i,name in enumerate(['shoot','games','camera-info','shutter-details-fixture']):
        raw=Image.open(Path(tmp)/(name+'.pgm'));im=raw.convert('RGB')
        im.putdata([palette.get(v,(255,0,255)) for v in raw.tobytes()])
        x=i%2*720;y=i//2*510;out.paste(im,(x,y+30))
        draw.text((x+12,y+7),'HOST LAYOUT PROOF - '+name+(' (simulated counts)' if 'shutter' in name else ''),fill='white')
    dest=root/'previews/photo-ui-v3r1-layout-proof.png';dest.parent.mkdir(exist_ok=True);out.save(dest)
    print(dest)
