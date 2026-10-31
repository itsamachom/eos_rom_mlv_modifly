# Canon 600D Photo UI — Magic Lantern fork

Photo UI ภาษาไทยสำหรับ **Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น** พัฒนาต่อยอดจาก [Magic Lantern](https://www.magiclantern.fm/) และ [reticulatedpines/magiclantern_simplified](https://github.com/reticulatedpines/magiclantern_simplified)

นี่คือ release ของ fork `itsamachom/eos_rom_mlv_modifly` ไม่ใช่บิลด์ทางการหรือบิลด์ที่ทีม Magic Lantern หรือ Canon รับรอง โค้ด UI, tests, คำแปลและเอกสารของ fork ใช้ Codex/LLM ช่วย ดู [การเปิดเผยการใช้ AI](AI_ASSISTANCE.md)

## v3r2 — Experimental

- UI หมวดถ่ายภาพ/โฟกัส/ค่าแสง/ตัวช่วยแสดงภาพ/วิดีโอ/ตั้งค่า/เกม พร้อมภาษาไทยและอังกฤษ
- Focus Peaking, Histogram, Waveform, Time-lapse, ถ่ายคร่อม, zebra settings และ Movie → Bitrate (CBR)
- แก้การบล็อกการลงทะเบียนแท็บ Games บน 600D; Arkanoid ใช้โมดูล arkanoid, Pong/Sokoban ใช้ lua
- ข้อมูลรุ่นกล้อง/เฟิร์มแวร์และชัตเตอร์กลไก/Live View/ผลรวมจาก property ที่อ่านได้จริง
- ไม่ทำ Picture Style; นำ Silent Picture ออกจากชุดนี้

**สถานะ:** build และ host checks ผ่าน แต่ v3r2 ยังไม่ได้ทดสอบการทำงานบนกล้องจริง การเล่นเกม หรือการติดตั้งครั้งแรก ไม่ควรเรียกว่า stable จากผล host tests

[ไฟล์ทดสอบที่มีอยู่](deliveries/photo-ui-v3r2-full/) · [คู่มือติดตั้ง](PHOTO_UI_V3R2_INSTALL_TH.md) · [เปิดเกม](GAMES_V3R2_TH.md) · [รายละเอียด v3r2](PHOTO_UI_V3R2.md) · [สถานะการเตรียม Release](release/v3r2/README.md)

ไฟล์สำหรับกล้องคือ `600D-102-PHOTO-UI-v3r2-FULL-EXPERIMENTAL.zip` **ไม่ใช่** Source code (zip) / Code → Download ZIP ของ GitHub ตรวจ SHA256SUMS ก่อนใช้ ผู้ที่ติดตั้ง ML แล้วให้อัปเดต autoexec.bin และ ML/ ทั้งชุดหลังสำรองข้อมูล ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดต UI

## ซอร์สและการ build

ซอร์สที่ใช้ build v3r2 คือ commit `5f543089565c1574606ea2436315e6ea5419ce70` และ source ZIP ที่แจกคู่กับไบนารี แหล่งที่มาของโค้ดต้นทางและไลบรารีต้องแยกจาก source commit ของ fork ดู [Provenance](release/v3r2/PROVENANCE.md), [วิธี build](release/v3r2/BUILDING.md) และ [ข้อจำกัดที่ยังเปิดอยู่](release/v3r2/READINESS.json)

## ลิขสิทธิ์และการมีส่วนร่วม

เก็บลิขสิทธิ์และใบอนุญาตต้นทางตามแต่ละไฟล์ ส่วนหลักของ Magic Lantern ใช้ GPL; ข้อความ GPL v2 อยู่ใน [LICENSE](LICENSE) และ [firmware/COPYING](firmware/COPYING) ส่วนที่มีเงื่อนไขต่างกัน เช่น TCC, Lua และ Noto ใช้ใบอนุญาตเดิม ดู [Third-party notices](THIRD_PARTY_NOTICES.md) และ [เครดิตต้นทาง](firmware/doc/CREDITS.txt)

[Contributing](CONTRIBUTING.md) · [นโยบาย LLM ของต้นทาง](firmware/LLM_POLICY.md)
