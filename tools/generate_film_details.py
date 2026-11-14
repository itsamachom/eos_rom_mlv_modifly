"""Shape Thai detail descriptions offline; emit bounded 1-bit masks with CRC."""
from pathlib import Path
import json,struct,zlib
from PIL import Image,ImageDraw,ImageFont,features
root=Path(__file__).resolve().parents[1];assert features.check_feature('raqm')
items=json.loads((root/'research/film-labels/DETAILS_TH.json').read_text())['items']
assert [x['key'] for x in items]==[x['key'] for x in json.loads((root/'research/jpeg-tones/UPSTREAM_ORIGINAL_CATALOG.json').read_text())['recipes']]
records=[(x['lines'],23) for x in items]+[(['ลักษณะอ้างอิง'],23),(['SET ใช้โทนนี้    MENU ย้อนกลับ'],23),(['สูตร JPEG ต้นทาง หลายรายการใช้ค่าซ้ำกัน'],20),(['รายละเอียดโทน'],25)]
font_path=root/'assets/fonts/noto-sans-thai/NotoSansThai.ttf'
def packbits(raw):
 out=bytearray();i=0
 while i<len(raw):
  if raw[i]==0 and i+1<len(raw) and raw[i+1]==0:
   end=i
   while end<len(raw) and raw[end]==0 and end-i<128:end+=1
   out.append(128+end-i-1)
  else:
   end=i+1
   while end<len(raw) and end-i<128 and not(raw[end]==0 and end+1<len(raw) and raw[end+1]==0):end+=1
   out.append(end-i-1);out+=raw[i:end]
  i=end
 return out
blobs=[];dims=[]
for lines,size in records:
 f=ImageFont.truetype(str(font_path),size,layout_engine=ImageFont.Layout.RAQM);f.set_variation_by_axes([600,100])
 width=max(int(f.getlength(x))+3 for x in lines);height=(size+11)*len(lines)
 assert width<=368,(lines,width)
 im=Image.new('L',(width,height));d=ImageDraw.Draw(im)
 for i,line in enumerate(lines):d.text((1,i*(size+11)),line,font=f,fill=255,language='th')
 stride=(width+7)//8;b=bytearray(stride*height)
 for y in range(height):
  for x in range(width):
   if im.getpixel((x,y))>=100:b[y*stride+x//8]|=128>>(x&7)
 dims.append((width,height));blobs.append(packbits(b))
count=len(blobs);offset=16+count*12;table=bytearray();payload=bytearray()
for (w,h),b in zip(dims,blobs):table+=struct.pack('<HHII',w,h,offset,len(b));payload+=b;offset+=len(b)
english_offset=16+len(table)+len(payload)
english=bytearray()
for x in items:
 b=x['en'].encode('ascii');assert len(b)<64
 english+=b+bytes(64-len(b))
data=struct.pack('<4sIII',b'FTD6',count,72,2)+table+payload+english
assert len(data)<256*1024
out=root/'firmware/data/photo_thai/TONEINFO.BIN';out.write_bytes(data)
(root/'firmware/src/photo-film-details-data.h').write_text(f'/* Generated Thai masks metadata; text GPL, Noto-derived masks OFL. */\n#define PHOTO_FILM_INFO_BYTES {len(data)}u\n#define PHOTO_FILM_INFO_CRC 0x{zlib.crc32(data):08x}u\n#define PHOTO_FILM_INFO_COUNT {count}\n#define PHOTO_FILM_EN_OFFSET {english_offset}u\n')
print('Generated',count,'detail masks,',len(data),'bytes')
