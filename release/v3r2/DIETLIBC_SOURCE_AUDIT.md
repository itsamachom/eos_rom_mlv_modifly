# dietlibc source search — 5 November 2026

**พบซอร์ส implementation สำหรับรายการที่ core/Lua ใช้ครบแล้ว แต่ยังไม่ยืนยันว่าเป็น corresponding source ของ archive ปี 2013 ทั้งชุด จึงไม่ปลด gate ของ Release**

การตรวจนี้ไม่แก้ไบนารี v3r2 ไม่เปลี่ยนไลบรารีที่เฟิร์มแวร์ใช้ ไม่ส่งความคิดเห็นถึงใคร และไม่สร้าง tag/Release

## 1. แหล่งซอร์สที่พบ

- [ensc/dietlibc](https://github.com/ensc/dietlibc) เป็น unofficial CVS import ที่มีการแก้เพิ่มเติมใน default branch การตรวจนี้ใช้ **CVS snapshot** ไม่ใช่ default branch ที่มี patches เพิ่ม:
  [9689726fa931309b7662fb3cd7c2f29567f76d23](https://github.com/ensc/dietlibc/tree/9689726fa931309b7662fb3cd7c2f29567f76d23), dated 2013-02-22.
- [rsenn/dietlibc](https://github.com/rsenn/dietlibc) เป็นอีก CVS import พบ snapshot ของเหตุการณ์เดียวกัน:
  [9c3f1c7726133e8ec084c1743b2e107fff8a2704](https://github.com/rsenn/dietlibc/tree/9c3f1c7726133e8ec084c1743b2e107fff8a2704).
- ทั้งสอง snapshot มี Git tree ID เดียวกัน **59b130f2b25010bfb4c49410fa8488182e038c08**, 1,833 ไฟล์ รวมไฟล์ใบอนุญาต COPYING และเครดิตตามต้นฉบับ CHANGES ขึ้นต้น `0.33:`
- ผู้เขียนหลักตาม AUTHOR คือ Felix von Leitner พร้อมเครดิตเพิ่มเติมใน THANKS เก็บข้อความเหล่านี้ไว้ใน snapshot

เก็บ snapshot พร้อม GPL และ notices เดิมไว้ใน
[source-candidates/](source-candidates/) โดยติดป้าย **candidate** ชัดเจน นี่ไม่ใช่ release tarball ที่ยืนยันจากเว็บไซต์ผู้เขียนโดยตรง และการตรงกันของสอง mirror ไม่ได้ยืนยัน flags/patches ที่คนสร้าง archive เคยใช้

## 2. ตามที่มาของ archive ได้ถึงปี 2013

พบ mirror เก่าของ Magic Lantern ที่ [frantony/magic-lantern](https://github.com/frantony/magic-lantern) และ commit
[d3f6810facfaf3ac201fbfa6f27a2d1fbf10654f](https://github.com/frantony/magic-lantern/commit/d3f6810facfaf3ac201fbfa6f27a2d1fbf10654f), authored 2013-03-19 00:22:56 +02:00 โดย `alex`:

> Time to go on a diet :) switched to dietlib, needed for TCC. fPIC may be broken.

archive ที่เพิ่มใน commit นี้มี SHA256 ตรงกับไฟล์ของ v3r2 **ทั้งไฟล์**:

```text
21c61d561fbd852f46eb891052efaa8cd3c634261803793ffe600eac67861d9a
```

ชื่อ archive คือ `src/libs/dietlib-0.33-none-eabi-Os/dietlibc.a` การเปลี่ยนแปลงใน commit เพิ่มการดึง object จาก archive แต่ไม่ได้เพิ่ม source implementation, dietfeatures config หรือคำสั่ง build archive นั้น

Makefile.user.default ของ commit ระบุ GCC_VERSION=4.7.3 ขณะที่ bootstrap script ระบุ 4.6.2/ตัวเลือก Linaro จึงใช้เป็นเบาะแสได้ แต่ไม่ใช่หลักฐานว่า compiler ใดสร้าง archive จริง เพราะ object ถูก strip `.comment` และไม่พบ debug producer ที่ระบุ compiler

## 3. การตรวจไฟล์และทดลองคอมไพล์

อ่านรายการ object จาก Makefile ของ v3r2 จริง: core 18 รายการ, Lua 40 รายการ รวมหลังตัดซ้ำ **54 รายการ** พบ source `.c`/`.S` ตาม VPATH ของ snapshot ครบ 54/54 และทดลอง compile เป็น ARM ได้ครบ โดยไม่ link หรือรันเฟิร์มแวร์บนกล้อง

| ผลตรวจ | จำนวน |
| --- | ---: |
| รายการ object ที่ source candidate ครอบคลุม | 54 / 54 |
| ทดลอง compile object ด้วย GCC 14.2.1 ผ่าน | 54 / 54 |
| `.text` ที่มีข้อมูลจริงและตรงทุกไบต์ | 8 |
| object ที่มีเนื้อหาจริงและตรงทั้ง allocated sections + relocations + exported symbols | 9 |
| object ว่างที่ตรงกัน แต่ไม่นับเป็นหลักฐานโค้ด | 1 (`atoi.o`) |
| header ที่ Lua เก็บไว้ตรงกับ snapshot | 32 / 36 |

9 รายการที่มีเนื้อหาจริงและผ่าน strict comparison:
`clearerr.o`, `errlistu.o`, `errno_location.o`, `feof.o`, `ferror.o`,
`localeconv.o`, `strcpy.o`, `strerror.o`, `strlen.o`.

ผล "ตรง" ข้างต้นไม่ใช่ไฟล์ ELF ทั้งไฟล์ byte-identical: การทดลองเปรียบเทียบข้อมูลที่โหลดใช้งาน, relocation และ symbol ที่ export ไม่เปรียบเทียบ section metadata/attributes ที่ไม่ถูกโหลดทั้งหมด

### Config และข้อจำกัดของการเปรียบเทียบ

archive เดิมระบุ ARM7TDMI / ARMv4T, ARM mode, Thumb-1 interworking และ optimization for size ใช้ timestamp ใน archive เป็นเบาะแสเท่านั้น ไม่ใช่หลักฐานเลือก source revision ตัวชี้วัดของ object ที่ใช้ตรงกับวันที่ 2013-03-18 UTC

snapshot เปิด `WANT_FASTER_STRING_ROUTINES` แต่ `strlen` ของ archive เป็น small-string implementation เมื่อปิดตัวเลือกนี้ใน **header overlay แยกสำหรับการทดลอง** จะประกอบ `.text` ของ `strlen` ได้ตรงกันทุกไบต์ ไม่ได้แก้ snapshot ต้นฉบับหรือไฟล์ใน firmware/ การเลือกนี้เป็นข้อสันนิษฐานที่บันทึกไว้ ไม่ใช่ config ที่ได้รับการยืนยันจากผู้สร้าง archive

compiler ที่ใช้ทดลองรอบแรกคือ GCC 14.2.1 ปัจจุบัน ไม่ใช่ compiler เดิม ความต่างของ object อีก 44 รายการจึงไม่ได้พิสูจน์ว่ามี patches และไม่อาจใช้ยืนยันว่าไม่มี patches เช่นกัน ตัวอย่าง `errno.o` มี BSS padding ต่างกัน และ `errlist.o` มีขนาด rodata ต่างหนึ่งไบต์ การตรวจไม่ตัด padding หรือเปลี่ยนค่าที่คาดหวังเพื่อเรียกว่าผ่าน strict comparison ดูผลเครื่องมือรุ่นเก่าเพิ่มเติมด้านล่าง

4 header ที่ต่างคือ unistd.h, math.h, ctype.h และ sys/cdefs.h ส่วนของ math.h มี prototype จาก Newlib เพิ่ม และ sys/cdefs.h มีหมายเหตุการแก้โดย a1ex ข้อเปรียบเทียบนี้บอกความใกล้เคียงของสายซอร์ส ไม่ได้ยืนยันว่า headers ของ Lua ที่คัดลอกไว้เป็น headers ที่ใช้ build archive จริง

ดูรายละเอียดราย object และ flags ที่รันจริงใน
[DIETLIBC_COMPARISON.json](DIETLIBC_COMPARISON.json) และ metadata ใน
[DIETLIBC_SOURCE_EVIDENCE.json](DIETLIBC_SOURCE_EVIDENCE.json)

### ตรวจต่อด้วยเครื่องมือรุ่นเก่า

สร้าง GCC 4.7.3 จากซอร์สของ gcc-mirror และ GNU assembler 2.23.1 จาก RTEMS Sourceware mirror ในพื้นที่ audit แยก ระบุ commit และ hash ของ archive ที่ดาวน์โหลด ใช้ HTTPS พร้อมตรวจ certificate แต่ยังไม่ได้ตรวจ release signature ไม่ใช้ compiler เหล่านี้สร้างหรือแทนที่เฟิร์มแวร์ และไม่รัน ARM binary

| Compiler / assembler | Compile ผ่าน | object ที่มีเนื้อหาและตรงตาม strict comparison |
| --- | ---: | ---: |
| GCC 14.2.1 / GAS 2.44 — รอบแรก | 54 / 54 | 9 |
| GCC 14.2.1 / GAS 2.23.1 | 54 / 54 | 11 |
| GCC 4.7.3 / GAS 2.44 | 54 / 54 | 30 |
| GCC 4.7.3 / GAS 2.23.1 | 54 / 54 | 32 |
| GCC 4.6.2 / GAS 2.44 — รอบไม่สมบูรณ์ | 52 / 54 | 17 (ผลบางส่วน) |
| GCC 4.6.2 / GAS 2.23.1 — รอบไม่สมบูรณ์ | 52 / 54 | 19 (ผลบางส่วน) |

ทุกแถวใช้ candidate source, flags และ small-string overlay แบบเดียวกัน ไม่นับ `atoi.o` ที่ว่าง ผลของ GCC 4.7.3 มี `.text` ที่ไม่ว่างตรงกัน 29 รายการ

เมื่อเปลี่ยนเฉพาะ assembler จาก 2.44 เป็น 2.23.1 ทั้ง `errno.o` และ `errlist.o` ผ่าน strict comparison โดยไม่แก้ซอร์ส: `.bss` ของ errno มี padding เป็น 256 ไบต์ และ `.rodata` ของ errlist มี zero padding จนเป็น 3,536 ไบต์ตรง archive เดิม นี่เป็นหลักฐานทดลองว่าความต่างสองรายการนี้อธิบายได้ด้วย assembler โดยไม่ต้องสมมติ source patch แต่ยังไม่ยืนยันว่า archive เดิมใช้ assembler 2.23.1

รอบแรกของ wrapper GCC 4.7.3 เคยดึง generated headers ผ่าน `-B` และ compile `strtoull.c` ไม่ผ่าน ไม่นำผลนั้นมานับ ตารางนี้ใช้ wrapper ที่แยกไดเรกทอรีค้นหา `cc1` ออกจาก headers แล้ว ตรวจ `-E -H` ว่าใช้ `limits.h` และ `stddef.h` ของ candidate จริง ไม่มีการเพิ่ม define เพื่อกลบข้อผิดพลาด

การทดลองปิด `-ftree-ch`, `-freorder-blocks` และทั้งสองตัวพร้อมกันไม่ทำให้จำนวนตรงเพิ่มขึ้น ยังไม่มีหลักฐานว่า flags เหล่านี้เป็นของ build เดิม

ตรวจ GCC 4.6.2 ตามเบาะแสใน bootstrap script เก่าด้วย สร้าง compiler ได้หลังปรับ optimization ของ **host generator เท่านั้น** โดยไม่แก้ compiler source แต่เมื่อใช้ compile candidate พบ internal compiler error (segmentation fault) ใน `__v_printf.c` และ `strtoull.c` ทั้งสอง assembler การตรวจรอบนี้จึงไม่สมบูรณ์ ไม่ตีความว่าเป็น source patch หรือพิสูจน์ว่า compiler เดิมเป็น/ไม่เป็นรุ่นนี้ และไม่ใช้แทนผล GCC 4.7.3 ที่ compile ครบ ดูข้อจำกัดและ workaround ในบันทึกเครื่องมือ

รายละเอียดที่ทำซ้ำได้อยู่ใน [toolchain-audit/](toolchain-audit/README.md) พร้อมข้อมูลราย object แยกตามเครื่องมือ ผล 32 รายการที่ตรงช่วยลดข้อสงสัยเรื่อง toolchain แต่ยังเหลือ 21 รายการที่ต่างกัน และยังไม่ยืนยัน recipe/config/patches ของ archive ทั้งชุด

## 4. ทำซ้ำ

ตรวจ SHA256 และคลาย candidate source ในไดเรกทอรี audit แยก แล้วรัน:

```sh
python3 tools/audit_dietlibc_source.py \
  --source /workspace/source-audit/dietlibc-033/cvs-20130222 \
  --output /workspace/source-audit/dietlibc-033/new-comparison
```

output ต้องเป็นไดเรกทอรีใหม่และอยู่นอก source candidate และ firmware/ ใช้ `--cc` หาก compiler อยู่คนละพาธ ไม่ต้องรัน Makefile ของ source candidate; script นี้ compile เฉพาะ object โดยตรงและเก็บคำเตือนใน log ไม่รันผลลัพธ์ ARM

script ตรวจ hash archive v3r2 ก่อนเริ่ม และตรวจว่าไฟล์เดิมไม่ถูกเปลี่ยนเมื่อจบ ผล compile สำเร็จไม่ได้แปลว่า source/ABI ตรงหรือปลอดภัยสำหรับกล้อง

## 5. สิ่งที่ยังค้าง และทางเดินต่อ

เรามี source implementation และเส้นทางประวัติของ archive แล้ว แต่ยังไม่มี config/patches/build recipe ต้นฉบับที่ระบุได้ว่าซอร์สชุดใดสร้าง archive ทั้งหมด จึงยังไม่กล่าวว่า candidate นี้เป็น corresponding source ที่ยืนยันครบ และไม่เผยแพร่ Release ตามการตรวจนี้

คำถามถึงผู้สร้างเดิมสามารถแคบลงเป็น compiler, dietfeatures.h, build invocation และ patches ที่ใช้ แทนการถามว่าซอร์สอยู่ที่ไหนอย่างเดียว ไม่ได้ส่งคำถามติดตามอัตโนมัติ

หากหา recipe เดิมไม่ได้ อีกทางที่ตรวจสอบได้คือ build library จาก source ที่ระบุ commit/config แน่นอนสำหรับ **รุ่นถัดไป** แล้วทดสอบการ link, ABI, host และกล้องใหม่ทั้งหมด ทางนี้ยังไม่ได้ทำกับเฟิร์มแวร์ และไม่ควรนำ object ทดลองชุดนี้ไปแทนใน v3r2 ที่ผู้ใช้มีอยู่โดยไม่ผ่านงานพัฒนา/ทดสอบแยก
