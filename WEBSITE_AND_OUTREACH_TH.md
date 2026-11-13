# หน้าแรก GitHub และการค้นหาโครงการ

หน้าแรกของ repository ใช้ branch เริ่มต้น `main` งานปัจจุบันคือ **FIRMWARE ADD-ON Thai-Menu v3r5** สำหรับ Canon EOS 600D / Rebel T3i / Kiss X5 และ Canon firmware 1.0.2 เว็บไซต์อยู่ที่ https://itsamachom.github.io/eos_rom_mlv_modifly/

README บน main เป็นจุดเริ่มสำหรับผู้ใช้ มีเว็บ ดาวน์โหลดแยก FIRST-INSTALL / UPDATE / SOURCE, คู่มือติดตั้ง คู่มือเมนูพร้อมภาพ วิดีโอ และช่องทางแจ้งปัญหา branch `site/eos-600d-bilingual` ยังใช้เผยแพร่เว็บตามการตั้งค่า Pages เดิม เมื่อแก้งานให้คงข้อมูลสอง branch นี้สอดคล้องกัน

## ตั้ง About และ Topics ให้ค้นหาเจอง่าย

ค่าที่เตรียมไว้ดู [.github/repository-metadata.json](.github/repository-metadata.json) **GitHub ไม่อ่านไฟล์นี้ไปตั้ง About/topics อัตโนมัติ** เป็นข้อมูลสำหรับบันทึกผ่านหน้าเว็บหรือ API เท่านั้น

1. เข้า [หน้า repository](https://github.com/itsamachom/eos_rom_mlv_modifly) ด้วยบัญชีเจ้าของหรือผู้มีสิทธิ์ดูแล
2. ที่แถบขวา **About** กดรูปเฟือง
3. ใส่ Description ด้านล่าง และ Website เป็น `https://itsamachom.github.io/eos_rom_mlv_modifly/`
4. เพิ่ม Topics จากรายการด้านล่าง แล้วกด **Save changes**

Description ที่แนะนำ:

> Thai/English Magic Lantern add-on for Canon EOS 600D / Rebel T3i / Kiss X5 (firmware 1.0.2). Downloads, illustrated Thai manual and video guides. Independent experimental project.

Topics ที่แนะนำ:

`magic-lantern` · `canon` · `canon-600d` · `eos-600d` · `rebel-t3i` · `kiss-x5` · `firmware-addon` · `camera-firmware` · `thai-menu` · `thai-language` · `photography` · `timelapse` · `open-source`

About คือคำอธิบายสั้น/เว็บไซต์ของ repository; Topics คือคำค้นจัดหมวด ไม่ใช่เลขรุ่น ส่วน **Git tag** เช่น [v3r5](https://github.com/itsamachom/eos_rom_mlv_modifly/tree/v3r5) ระบุจุดในประวัติโค้ด ไม่ควรเปลี่ยน tag เดิมให้ชี้ไปงานใหม่ การแก้คู่มือหรือหน้าเว็บไม่จำเป็นต้องเพิ่มเลขเฟิร์มแวร์

เมื่อใช้ API ได้ ผู้มีสิทธิ์สามารถนำ description/homepage ไป PATCH repository และ topics ไป PUT endpoint `/repos/itsamachom/eos_rom_mlv_modifly/topics` ตามเอกสาร GitHub ไม่ใส่ token ในไฟล์นี้หรือในแชต การเรียก API จากเครื่องคลาวด์ครั้งล่าสุดได้ `Forbidden` จึงยังไม่ได้บันทึก About/topics ผ่าน API

## ป้าย GPL-2.0 ใช้ได้หรือไม่

ไม่ต้องสมัครหรือผ่านเกณฑ์ยอดผู้ติดตามเพื่อมี About, Topics หรือป้ายใบอนุญาต GitHub ตรวจข้อความ LICENSE ใน branch เริ่มต้นและแสดงป้ายที่รู้จักให้ โครงการมี [LICENSE](LICENSE) เป็น GNU GPL version 2 อยู่แล้ว จึงนำไฟล์เดิมมาขึ้น main พร้อมงานได้ โดยไม่เปลี่ยนใบอนุญาตต้นทาง

ป้ายที่แสดง **ไม่ใช่การตรวจรับรองว่าการแจกไบนารีผ่านเงื่อนไขครบแล้ว**:

- เก็บเครดิต copyright และเงื่อนไข GPL/การอัปเกรดตามแต่ละไฟล์
- เก็บใบอนุญาตส่วนประกอบอื่น เช่น Lua/MIT, TinyCC/LGPL, Noto/OFL ตาม [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- การแจกไบนารีต้องพิจารณา corresponding source ที่ตรงกับส่วนประกอบนั้นด้วย [ข้อค้าง inherited dietlibc](release/v3r2/PROVENANCE.md) ยังไม่ถือว่าแก้แล้วเพียงเพราะมี LICENSE หรือ Source ZIP
- ไม่อ้างว่าเป็นโครงการที่ Canon หรือทีม Magic Lantern รับรอง และไม่คัดลอกข้อความ/ภาพของ repository ตัวอย่างมาเป็นของเรา

## ทำให้คนพบโครงการมากขึ้น

| ลำดับ | สิ่งที่ทำ | เหตุผล |
| --- | --- | --- |
| 1 | About + Website + Topics ให้ครบ | คนเห็นรุ่นกล้องและสิ่งที่โครงการทำตั้งแต่หน้า repository และค้นตามหมวดได้ |
| 2 | ใช้ชื่อ Canon EOS 600D / Rebel T3i / Kiss X5, Magic Lantern และ Thai Menu ในชื่อ/คำอธิบายวิดีโออย่างเป็นธรรมชาติ | คนในแต่ละประเทศเรียกกล้องคนละชื่อ และอาจค้นภาษาอังกฤษ |
| 3 | ใส่ลิงก์หน้าเว็บกลางในคำอธิบายคลิปและโพสต์ที่ผู้ดูแลเผยแพร่เอง | ผู้ใช้ไปยังไฟล์/คู่มือล่าสุดได้จากจุดเดียว ลด ZIP ที่กระจายหลายสำเนา |
| 4 | ทำคลิปสั้นแยกเรื่อง เช่น ติดตั้งครั้งแรก อัปเดต ตั้ง Timelapse หรือแก้ปัญหาโมดูล | คนค้นตามงานที่ต้องการทำได้ง่ายกว่าคลิปยาวเรื่องเดียว |
| 5 | เมื่อออกรุ่นจริง ใช้ GitHub Releases พร้อมสรุปสิ่งที่เปลี่ยน ไฟล์ติดตั้ง/ซอร์สแยกกัน และผลทดสอบตามจริง | ผู้ติดตาม Watch → Releases ได้รับข่าวที่ชัด ไม่สับสนกับการแก้หน้าเว็บ |
| 6 | แชร์ในชุมชน Canon/Magic Lantern/ถ่ายภาพที่อนุญาต พร้อมบอกว่าเป็น fork อิสระและสถานะทดลอง | เข้าถึงผู้ใช้ตรงกลุ่มโดยรักษากติกาชุมชนและเครดิตต้นทาง |
| 7 | ตั้ง Social preview ของ repository เป็นภาพโครงการของเรา และ pin repository บนโปรไฟล์ผู้พัฒนา | ลิงก์ที่แชร์มีภาพ/ตัวตนชัด และผู้เข้าหน้าโปรไฟล์เจองานได้ง่าย |

ไม่รับรองอันดับค้นหาหรือยอดผู้ใช้ การเพิ่มคำค้นควรตรงกับกล้องและคุณสมบัติที่รองรับจริง ไม่เพิ่มชื่อกล้องที่ยังไม่ได้รองรับเพื่อเรียกคนเข้า และไม่อ้างการทดสอบหรือการรับรองที่ไม่มี

## ช่องทางสนับสนุน

เจ้าของกำลังสมัครช่องทางสนับสนุน ยังไม่ได้เพิ่มปุ่ม GitHub Sponsors หรือระบบรับเงิน เมื่อสมัครเสร็จจึงเชื่อมบัญชีที่เจ้าของยืนยัน รายได้จาก YouTube ใช้ต่อได้ตามสิทธิ์ช่อง โดยเนื้อหาและลิงก์ดาวน์โหลดไม่จำเป็นต้องล็อกไว้หลังการชำระเงิน

เว็บไซต์: https://itsamachom.github.io/eos_rom_mlv_modifly/

ผู้พัฒนา: [YouTube Online2easy](https://www.youtube.com/@Online2easy) · [Facebook Online2easy](https://www.facebook.com/online2easy) · [Online2hobby Blog](https://online2hobby.blogspot.com/)
