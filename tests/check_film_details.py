"""Audit detail text order, binary bounds/CRC, and complete reference masks."""
from pathlib import Path
import json,re,struct,zlib
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'research/film-labels/DETAILS_TH.json').read_text())['items']
recipes=json.loads((root/'research/jpeg-tones/UPSTREAM_ORIGINAL_CATALOG.json').read_text())['recipes']
assert [i['key'] for i in items]==[r['key'] for r in recipes]
b=(root/'firmware/data/photo_thai/TONEINFO.BIN').read_bytes()
h=(root/'firmware/src/photo-film-details-data.h').read_text()
value=lambda name:int(re.search(r'#define '+name+r' (0x[0-9a-f]+|[0-9]+)',h)[1],0)
assert len(b)==value('PHOTO_FILM_INFO_BYTES')<256*1024
assert zlib.crc32(b)==value('PHOTO_FILM_INFO_CRC')
assert struct.unpack_from('<4sIII',b)==(b'FTD6',76,72,2)
for i in range(76):
 w,hei,off,n=struct.unpack_from('<HHII',b,16+i*12)
 assert w<=368 and hei<=80 and n>0
 assert 16+76*12<=off and off+n<=value('PHOTO_FILM_EN_OFFSET')
 raw=bytearray();pos=off
 while pos<off+n:
  tag=b[pos];pos+=1;run=(tag&127)+1
  if tag&128:raw+=bytes(run)
  else:raw+=b[pos:pos+run];pos+=run
 assert len(raw)==((w+7)//8)*hei and any(raw),i
for i,x in enumerate(items):
 off=value('PHOTO_FILM_EN_OFFSET')+i*64
 assert b[off:off+64].split(b'\0',1)[0].decode()==x['en']
print('PASS 72 reference descriptions/keys, 76 bounded Thai masks, exact binary CRC and English text')
