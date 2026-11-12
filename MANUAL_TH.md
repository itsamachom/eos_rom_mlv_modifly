# คู่มือเมนูภาษาไทย — Thai-Menu v3r5

สำหรับ Canon EOS 600D / Canon firmware 1.0.2

## ใช้คู่มือนี้กับรุ่นใด

คู่มือสำหรับ FIRMWARE ADD-ON Thai-Menu v3r5 บน Canon EOS 600D / Rebel T3i / Kiss X5 และ Canon firmware 1.0.2 ชื่อเมนูอ้างอิงโค้ดรุ่นนี้ ไม่ใช่คู่มือเฟิร์มแวร์ Canon ทั้งระบบ

## ขอบเขต

อธิบาย 44 รายการใน Photo UI และตัวเลือกย่อยที่ผูกไว้กับเมนูเหล่านี้ ส่วน Modules, Preferences, Display และ Scripts เป็นทางเข้าหน้าระบบเดิม รายการภายในอาจต่างตามโมดูลและสถานะกล้อง จึงไม่ถือว่าเป็นรายการตายตัวครบทุกหน้า Classic

## การติดตั้ง

หากยังไม่ได้ติดตั้ง ให้อ่านคู่มือติดตั้งที่หน้าดาวน์โหลดและดูคลิปก่อน คู่มือนี้ใช้สำหรับทำความเข้าใจเมนู ไม่ใช้แทนขั้นตอนติดตั้ง

## สถานะรุ่น

รุ่นนี้เป็น Public Experimental คู่มืออธิบายพฤติกรรมตามโค้ด ไม่ใช่การยืนยันว่าทุกฟังก์ชันผ่านการทดสอบบนกล้องจริง ภาพเมนูที่ลิงก์ไว้เป็นภาพจำลองจากตัววาดเมนูบนคอมพิวเตอร์

## ปุ่มและการเลื่อนเมนู

- **ปุ่มถังขยะ:** เปิดเมนู Magic Lantern ตามการทำงานปกติของแพ็ก
- **ขึ้น/ลง หรือวงล้อ:** เลื่อนรายการในคอลัมน์ที่เลือก หากอยู่คอลัมน์รายการ เมื่อผ่านท้ายหมวดจะไปหมวดถัดไป เช่น S ไป F
- **ขวา / SET:** จากหมวดเข้าไปรายการ และจากรายการเข้าแผงตัวเลือกด้านขวา
- **SET ในแผงตัวเลือก:** แถวค่าที่แก้ได้: เข้าโหมดแก้ ใช้ซ้าย/ขวาปรับ แล้ว SET จบ; แถวคำสั่งแบบ Action: อาจต้อง SET ยืนยันอีกครั้ง อ่านคำถามบนจอก่อนรัน
- **ซ้าย:** ย้อนกลับหนึ่งคอลัมน์เมื่อไม่ได้แก้ค่า หากกำลังแก้ค่า ซ้ายใช้ลด/เปลี่ยนค่า จึงให้กด SET จบก่อนย้อนกลับ
- **Q / PLAY ในแผงตัวเลือก:** เปิดตัวเลือกหรือหน้าควบคุมเดิมของรายการนั้นเมื่อรองรับ บางหน้าจึงมีหน้าตาต่างจาก Photo UI
- **MENU:** จบการแก้หรือยกเลิกการยืนยันก่อน; เมื่อไม่ได้แก้/ยืนยัน ใช้ปิดเมนู
- **INFO:** เมื่อไม่ได้บันทึกวิดีโอ สลับ Photo UI กับ Classic หรือกลับจากตัวแก้ไขเดิม; ระหว่างบันทึก INFO ทำหน้าที่แบบ Q จึงไม่สลับหน้าแบบเดียวกัน
- **หน้าที่ 1/2 หรือ Options:** ยังมีรายการหรือตัวเลือกต่ออีกหน้า ใช้ขึ้น/ลงเลื่อนให้ครบ ไม่ได้หมายความว่าเมนูหาย
- **ค่าปัจจุบัน / ยังใช้งานไม่ได้:** ค่าปัจจุบันคือสถานะของรายการหลัก; ยังใช้งานไม่ได้อาจเกิดจากยังไม่โหลดโมดูล ไม่รองรับสถานะปัจจุบัน หรืออ่านข้อมูลไม่ได้ ไม่ได้แปลว่าเป็นเลขศูนย์หรือฟังก์ชันถูกลบ

## S · ถ่ายภาพ

### Time-lapse

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-item-01.png" width="220" alt="ภาพจำลองเมนู Time-lapse — หน้ารายการ"></a><br>หน้ารายการ | สั่งถ่ายภาพซ้ำเป็นช่วงเวลา เพื่อนำภาพไปเรียงเป็นวิดีโอ Timelapse หรือบันทึกการเปลี่ยนแปลงระยะยาว<br><br><strong>วิธีใช้:</strong> วางกล้องบนขาตั้ง ล็อกค่าแสงและโฟกัส ตั้งช่วงห่างและจำนวนภาพ แล้วเปิดใช้งานตามวิธีเริ่มที่เลือก |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-options-01.png" width="220" alt="ภาพจำลองเมนู Time-lapse — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ช่วงห่างแต่ละภาพ (Take a pic every)</strong><br>ช่วงเวลาระหว่างภาพ เลือกให้ยาวพอสำหรับเวลาเปิดรับแสงและเวลาบันทึกลงการ์ด หากกล้องยังไม่พร้อม ไม่ควรคาดว่าจะรักษาช่วงห่างได้ทุกภาพ<br><br><strong>เงื่อนไขเริ่มถ่าย (Start trigger)</strong><br>วิธีเริ่ม: Leave Menu เริ่มเมื่อออกจากเมนู; Half Shutter เริ่มเมื่อกดชัตเตอร์ครึ่งหนึ่ง; Take a Pic เริ่มหลังถ่ายภาพแรก<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-options-02.png" width="220" alt="ภาพจำลองเมนู Time-lapse — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>หน่วงก่อนเริ่ม (Start after)</strong><br>เวลารอก่อนเริ่มชุดถ่าย ใช้เมื่ออยากให้กล้องเริ่มหลังจัดวางเสร็จ<br><br><strong>หยุดหลังถ่ายครบ (Stop after)</strong><br>หยุดเมื่อครบจำนวนภาพที่กำหนด ค่า OFF ไม่กำหนดจำนวนหยุดจากตัวเลือกนี้<br><br> |

- ตัวอย่าง: ถ่ายทุก 5 วินาที จำนวน 120 ภาพ ใช้เวลาประมาณ 10 นาที; เวลาจริงขึ้นกับความพร้อมของกล้อง
- ตรวจจำนวนภาพต่อครั้งใน ตั้งค่าการถ่ายภาพ ด้วย หากต้องการหนึ่งภาพต่อรอบให้ใช้ 1 (OFF)

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ตั้งเวลาชัตเตอร์ B (Bulb Timer)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-02-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งเวลาชัตเตอร์ B — หน้ารายการ"></a><br>หน้ารายการ | กำหนดเวลาเปิดรับแสงแบบ Bulb สำหรับการถ่ายนานกว่าค่าชัตเตอร์ปกติ<br><br><strong>วิธีใช้:</strong> ใช้โหมด M/Bulb ตามการตั้งค่ากล้อง วางบนขาตั้ง กำหนดเวลา เปิดฟังก์ชัน แล้วเริ่มตามคำแนะนำบนจอ โดยต้นทางระบุการกดชัตเตอร์ครึ่งหนึ่งค้างประมาณ 1 วินาที |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-02-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-02-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งเวลาชัตเตอร์ B — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ระยะเวลาเปิดรับแสง (Exposure duration)</strong><br>ระยะเวลาเปิดหน้าชัตเตอร์ เช่น 60 วินาที ไม่ใช่เวลารอก่อนถ่าย<br><br><strong>หน้าจอขณะเปิดรับแสง (Display during exposure)</strong><br>การแสดงจอระหว่างเปิดรับแสง: ไม่เปลี่ยนสถานะเดิม ปิดจอ หรือแสดงภาพก่อนหน้า หากตัวเลือกนั้นพร้อมใช้<br><br> |

- การลดนอยส์จากการเปิดรับแสงนานของ Canon อาจทำให้ต้องรอเพิ่มหลังถ่าย ระยะห่างระหว่างภาพจึงอาจยาวกว่าระยะเปิดรับแสง

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ถ่ายคร่อม (Bracketing)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-item-01.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อม — หน้ารายการ"></a><br>หน้ารายการ | ถ่ายหลายภาพโดยเปลี่ยนค่าแสง แฟลช หรือระยะชัด เพื่อเลือกภาพหรือรวมภาพภายหลัง<br><br><strong>วิธีใช้:</strong> เลือกชนิดการคร่อม จำนวนภาพ และระยะ EV แล้วกดชัตเตอร์เพื่อเริ่มหนึ่งชุด |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-01.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อม — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>รูปแบบการคร่อมค่า (Bracket type)</strong><br>เลือกสิ่งที่เปลี่ยน: ค่าแสง (TV, AV), ค่าแสงแฟลช หรือ DOF (Aperture) ป้ายบนจอควรอ่านร่วมกับหมายเหตุด้านล่าง<br><br><strong>จำนวนภาพ (Frames)</strong><br>จำนวนภาพในหนึ่งชุด; Autodetect ให้โปรแกรมคำนวณตามเงื่อนไขที่รองรับ ส่วน 2–12 คือจำนวนภาพที่กำหนดเอง<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-02.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อม — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ระยะห่างค่าแสง EV (EV increment)</strong><br>ความต่างค่าแสงระหว่างภาพ หน่วย EV ยิ่งมาก ภาพติดกันยิ่งสว่างต่างกัน<br><br><strong>ลำดับการถ่าย (Sequence)</strong><br>ลำดับคร่อม: 0 - -- ถ่ายจากค่าตั้งต้นไปมืด; 0 - + -- ++ สลับมืด/สว่าง; 0 + ++ ไปทางสว่าง โดย 0 คือค่าตั้งต้น ไม่ใช่จำนวนภาพศูนย์<br><br><strong>หน่วงเวลา 2 วินาที (2-second delay)</strong><br>หน่วงก่อนเริ่มชุดที่สั่งด้วยชัตเตอร์ ตัวเลือก OFF/Auto ใช้ตามเงื่อนไขของโปรแกรม ไม่ใช่ตัวกำหนดจำนวนภาพ<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-03.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-options-03.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อม — ตัวเลือกหน้า 3"></a><br>ตัวเลือกหน้า 3 | <strong>เลื่อนค่า ISO (ISO shifting)</strong><br>เพิ่ม ISO เป็นตัวแปรคร่อม: OFF ไม่ใช้; Full พยายามใช้ ISO ก่อนแล้วจึงใช้ตัวแปรหลักเมื่อเกินช่วง; Half แบ่งผลระหว่าง ISO และตัวแปรหลัก<br><br> |

- ป้ายไทย “ค่าแสง (TV, AV)” ตรงกับ Exposure (Tv,Ae) ในต้นทาง: โหมด M เปลี่ยนชัตเตอร์ โหมดอื่นเปลี่ยนค่าชดเชยแสง ไม่ได้หมายความว่าปรับรูรับแสงทุกโหมด การคร่อมรูรับแสงใช้ DOF (Aperture)
- ปิด Canon AEB ก่อนใช้การคร่อมชุดนี้ เพื่อไม่ให้การตั้งค่าซ้อนกัน

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ล็อคกระจกสะท้อน (Mirror Lockup)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-04-item-01.png" width="220" alt="ภาพจำลองเมนู ล็อคกระจกสะท้อน — หน้ารายการ"></a><br>หน้ารายการ | ยกกระจกสะท้อนล่วงหน้าเพื่อลดแรงสั่นก่อนเปิดรับแสง สำหรับการถ่ายภาพผ่านช่องมองภาพ<br><br><strong>วิธีใช้:</strong> เลือกวิธีล็อคกระจกตามรูปแบบถ่าย และตั้งเวลาหน่วงสำหรับชุด Timelapse/ถ่ายคร่อมเมื่อใช้ฟังก์ชันเหล่านั้น |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-04-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-04-options-01.png" width="220" alt="ภาพจำลองเมนู ล็อคกระจกสะท้อน — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>วิธีล็อคกระจก (MLU mode)</strong><br>Always ON ใช้รูปแบบล็อคกระจกของ Canon ซึ่งโดยปกติกดชัตเตอร์ครั้งแรกยกกระจกและครั้งต่อไปถ่าย; Self-Timer ผูกการล็อคกระจกกับโหมดตั้งเวลาถ่ายของ Canon<br><br><strong>สำหรับ Timelapse/ถ่ายคร่อม (Normal MLU Delay)</strong><br>ป้ายไทย “สำหรับ Timelapse/ถ่ายคร่อม” คือเวลารอหลังยกกระจกก่อนถ่ายเมื่อโปรแกรมเรียกใช้ MLU เช่น Timelapse หรือถ่ายคร่อม มี 0.5, 0.75, 1, 2, 3, 4 และ 5 วินาที<br><br> |

- ฟังก์ชันนี้ใช้ในโหมดภาพนิ่งนอก Live View และไม่มีตัวเลือกถือกล้องด้วยมือในบิลด์ 600D นี้
- เวลาหน่วงนี้ไม่ใช่เวลาห่างระหว่างภาพ และไม่ใช่ตัวตั้งเวลาถ่าย 2/10 วินาทีของ Canon

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ตั้งค่าแฟลช (Flash Tweaks)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-05-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าแฟลช — หน้ารายการ"></a><br>หน้ารายการ | รวมการชดเชยแสงแฟลชและตัวช่วยใช้งานแฟลชบางรูปแบบ<br><br><strong>วิธีใช้:</strong> ปรับเฉพาะตัวเลือกที่จำเป็นกับแฟลชที่ใช้อยู่ แล้วทดลองถ่ายและตรวจผลจริง |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-05-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-05-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าแฟลช — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ชดเชยแสงแฟลช (Flash expo comp.)</strong><br>ชดเชยความสว่างของแฟลช ช่วงตามโค้ดตั้งแต่ -10 EV ถึง +3 EV; เป็นค่าแสงแฟลช ไม่ใช่การชดเชยแสงฉากทั้งหมด<br><br><strong>สลับใช้แฟลช (Flash / No flash)</strong><br>สลับภาพที่ใช้แฟลชกับไม่ใช้แฟลช โดยภาพลำดับคี่ใช้แฟลชและภาพลำดับคู่ไม่ใช้<br><br><strong>แฟลชเสริมใน LV (3rd p. flash LV)</strong><br>วิธีช่วยให้แฟลชภายนอกบางชนิดยิงขณะใช้ Live View ปิดตัวเลือกนี้เมื่อไม่ได้ใช้ตามคำเตือนของต้นทาง<br><br> |

- ผลขึ้นกับรุ่นแฟลช โหมด และการเชื่อมต่อ ไม่ควรตีความว่าแฟลชทุกตัวรองรับ

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ตั้งค่าการถ่ายภาพ (Shoot Preferences)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าการถ่ายภาพ — หน้ารายการ"></a><br>หน้ารายการ | ตั้งค่าที่หลายฟังก์ชันถ่ายภาพใช้ร่วมกัน เช่น จำนวนภาพต่อการสั่งถ่ายหนึ่งครั้งและการใช้ AF<br><br><strong>วิธีใช้:</strong> ตรวจหน้านี้ก่อนทดสอบ Timelapse/ถ่ายคร่อม โดยเฉพาะเมื่อจำนวนภาพจริงต่างจากที่คาด |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าการถ่ายภาพ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>จำนวนภาพต่อชุด (Pics at once)</strong><br>จำนวนภาพต่อหนึ่งเหตุการณ์สั่งถ่าย มี 1 (OFF) ถึง 9; ถ้าต้องการหนึ่งภาพต่อรอบให้ตั้ง 1 (OFF)<br><br><strong>ใช้โฟกัสอัตโนมัติ (Use Autofocus)</strong><br>ให้ฟังก์ชันถ่ายอัตโนมัติที่รองรับเรียก AF ก่อนถ่าย หากหาโฟกัสไม่ได้อาจไม่ถ่าย เหมาะกับเลนส์และโหมดที่รองรับ AF<br><br><strong>สคริปต์หลังถ่าย (Post scripts)</strong><br>สร้างข้อมูล/สคริปต์ช่วยรวมภาพจากการคร่อมและคร่อมโฟกัส: OFF, Enfuse, Align+Enfuse หรือ File List ไม่ได้หมายความว่ากล้องรวมภาพเสร็จให้ทันที<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-options-02.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าการถ่ายภาพ — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>สคริปต์ถ่ายตามช่วงเวลา (Intervalometer Script)</strong><br>สร้างสคริปต์จัดเรียงชุดภาพ Timelapse บนคอมพิวเตอร์: OFF, Bash, MS-DOS หรือ File List<br><br><strong>จำลองการกดชัตเตอร์ (Snap Simulation)</strong><br>จำลองการถ่ายเพื่อทดสอบ โดยส่งสัญญาณไฟ/เสียงแทนการถ่ายจริง หากต้องการไฟล์ภาพจริงให้ใช้ OFF<br><br> |

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-01-06-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

## F · โฟกัส

### ถ่ายเมื่อเข้าโฟกัส (Trap Focus)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-01-item-01.png" width="220" alt="ภาพจำลองเมนู ถ่ายเมื่อเข้าโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | สั่งถ่ายเมื่อวัตถุเข้าระยะโฟกัส ใช้กับการตั้งเลนส์เป็น MF ตามเงื่อนไขของระบบ<br><br><strong>วิธีใช้:</strong> ตั้งระยะโฟกัสไว้ล่วงหน้า เลือก Hold AF button หรือ Continuous แล้วให้วัตถุเคลื่อนผ่านระนาบโฟกัส |

- OFF ปิดฟังก์ชัน; Hold AF button ทำงานขณะกดปุ่ม AF; Continuous ทำงานต่อเนื่องตามเงื่อนไขในโค้ด
- นอก Live View ต้องมีเลนส์ที่สื่อสารกับกล้องได้ การตรวจโฟกัสขึ้นกับเลนส์และแสง จึงต้องทดลองก่อนใช้งานจริง

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### ถ่ายคร่อมโฟกัส (Focus Stacking)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-item-01.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อมโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | ถ่ายหลายภาพโดยเลื่อนโฟกัส แล้วนำไปรวมเพิ่มระยะชัดบนคอมพิวเตอร์<br><br><strong>วิธีใช้:</strong> ใช้ Live View กับเลนส์ AF ที่สั่งขยับได้ วางขาตั้ง ตั้งจำนวนภาพหน้า/หลังและระยะขยับ แล้วเรียก Run focus stack |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-options-01.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อมโฟกัส — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>เริ่มถ่ายคร่อมโฟกัส (Run focus stack)</strong><br>เริ่มชุดถ่ายคร่อมโฟกัส กด MENU เพื่อขอหยุดตามคำแนะนำต้นทาง<br><br><strong>ภาพระยะชัดด้านหน้า (Num. pics in front)</strong><br>จำนวนภาพด้านหน้าของระยะโฟกัสปัจจุบัน ทิศจริงอาจกลับกันในเลนส์บางตัว<br><br><strong>ภาพระยะชัดด้านหลัง (Num. pics behind)</strong><br>จำนวนภาพด้านหลังของระยะโฟกัสปัจจุบัน ทิศจริงอาจกลับกันในเลนส์บางตัว<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-options-02.png" width="220" alt="ภาพจำลองเมนู ถ่ายคร่อมโฟกัส — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ระยะเลื่อนต่อภาพ (Focus steps / picture)</strong><br>จำนวนคำสั่งขยับโฟกัสระหว่างภาพ ยิ่งมากจุดโฟกัสยิ่งห่าง แต่ระยะจริงไม่ใช่มิลลิเมตรคงที่<br><br><strong>หน่วงรอแฟลช (Flash Delay)</strong><br>เวลารอระหว่างช่วงถ่ายเพื่อให้แฟลชชาร์จกลับ<br><br><strong>ใช้ช่วงย้ายโฟกัส (Copy rack focus range)</strong><br>คัดลอกช่วงโฟกัสที่ตั้งสำหรับ Rack Focus มาใช้กำหนดชุด Focus Stacking<br><br> |

- ภาพยังต้องนำไปรวมด้วยซอฟต์แวร์ภายนอก โปรแกรมไม่ได้ทำภาพชัดลึกสำเร็จบนกล้อง

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### ย้ายระยะโฟกัส (Rack Focus)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-03-item-01.png" width="220" alt="ภาพจำลองเมนู ย้ายระยะโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | สั่งเลื่อนโฟกัสระหว่างตำแหน่งที่ตั้งไว้ เหมาะกับการเปลี่ยนจุดสนใจในวิดีโอ<br><br><strong>วิธีใช้:</strong> ตั้งจุดโฟกัสต้นทางและปลายทางใน Live View ก่อน แล้วเรียกคำสั่ง Rack Focus |

- ต้นทางระบุ SET สำหรับสั่งเลื่อน และ PLAY สำหรับเลื่อนพร้อมเริ่มบันทึกเมื่อเรียกผ่านตัวควบคุมเดิม การทำงานของปุ่มใน Photo UI ขึ้นกับแถวคำสั่งที่เลือก
- ใช้เลนส์ AF ที่กล้องสั่งโฟกัสได้ ความเร็วและความเรียบขึ้นกับเลนส์กับ Focus Settings

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### ควบคุมโฟกัส (Follow Focus)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-04-item-01.png" width="220" alt="ภาพจำลองเมนู ควบคุมโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | ใช้ปุ่มทิศทางสั่งขยับโฟกัสแทนการหมุนวงแหวนบนเลนส์<br><br><strong>วิธีใช้:</strong> เปิด Live View และใช้เลนส์ AF ที่รองรับ เปิดฟังก์ชันแล้วใช้ปุ่มตามคำแนะนำบนจอ |

- ขนาดและจังหวะขยับใช้ค่าจาก Focus Settings
- ข้อกำหนดต้นทางคือ Live View/AF และไม่ใช้ Continuous AF; ระหว่างบันทึก MENU มีหน้าที่เกี่ยวกับการเก็บจุดโฟกัสในระบบเดิม จึงควรอ่านคำใบ้บนหน้าที่กำลังใช้อยู่

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### จุดสิ้นสุดโฟกัส (Focus End Point)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-05-item-01.png" width="220" alt="ภาพจำลองเมนู จุดสิ้นสุดโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | กำหนดตำแหน่งปลายทางสำหรับ Rack Focus ไม่ใช่การตั้งขอบเขต AF ของ Canon<br><br><strong>วิธีใช้:</strong> เลื่อนเลนส์ไปยังระยะปลายทาง แล้วใช้ Q ในหน้าควบคุมเดิมเพื่อตั้งจุดตามคำแนะนำต้นทาง |

- คำใบ้เดิมระบุ Q ตั้งปลายทาง และ SET ร่วมกับซ้าย/ขวาสำหรับต้นทาง; Photo UI ใช้ Q เพื่อเปิดตัวแก้ไขเดิมก่อน
- ต้องใช้ Live View กับเลนส์ AF ที่รองรับคำสั่งขยับ

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### ตั้งค่าโฟกัส (Focus Settings)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | กำหนดวิธีส่งคำสั่งโฟกัสร่วมกันของ Follow Focus, Rack Focus และ Focus Stacking<br><br><strong>วิธีใช้:</strong> เริ่มด้วยจังหวะขยับที่เลนส์ตอบสนองได้ แล้วค่อยปรับความเร็วจากภาพที่เห็นจริง |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าโฟกัส — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ระยะเลื่อนโฟกัส (Step Size)</strong><br>ขนาดก้าวคำสั่งโฟกัส 1–3 เป็นระดับคำสั่งแบบ EOS Utility ไม่ใช่ระยะทางจริง<br><br><strong>หน่วงระหว่างเลื่อน (Step Delay)</strong><br>ช่วงรอระหว่างคำสั่งโฟกัสสองครั้ง เพิ่มค่านี้เมื่ออยากให้ส่งคำสั่งห่างขึ้น<br><br><strong>รอให้เลื่อนเสร็จ (Step Wait)</strong><br>รอสัญญาณยืนยันว่าเลนส์โฟกัสเสร็จก่อนส่งคำสั่งถัดไป<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-options-02.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าโฟกัส — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ทิศทางซ้าย/ขวา (Left/Right dir)</strong><br>สลับทิศใกล้/ไกลของปุ่มซ้ายและขวา<br><br><strong>ทิศทางขึ้น/ลง (Up/Down dir)</strong><br>สลับทิศใกล้/ไกลของปุ่มขึ้นและลง<br><br><strong>หน่วงก่อนเริ่ม (Start Delay)</strong><br>หน่วงเป็นวินาทีก่อนเริ่มการขยับโฟกัส<br><br> |

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-06-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

### ตั้งค่าระยะชัด (DOF Settings)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-07-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าระยะชัด — หน้ารายการ"></a><br>หน้ารายการ | ตั้งค่าการคำนวณและแสดงระยะชัด ไม่ได้เปลี่ยนคุณสมบัติทางกายภาพของเลนส์<br><br><strong>วิธีใช้:</strong> ใช้เพื่ออ่านข้อมูลประกอบการถ่าย โดยตรวจภาพขยายจริงร่วมด้วย |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-07-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-07-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าระยะชัด — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>วงกลมความคลาด (Circle of Confusion)</strong><br>เกณฑ์วงกลมความพร่าในการคำนวณระยะชัด ค่ายิ่งเข้มงวด ระยะที่ถือว่าชัดยิ่งแคบ ค่าต้นทางแนะนำ 19 สำหรับ APS-C<br><br><strong>สูตรคำนวณระยะชัด (DOF formula)</strong><br>Simple คิดจากความพร่าเพราะหลุดโฟกัส; Diffraction-aware พิจารณาผลเลี้ยวเบนของแสงร่วมด้วย<br><br><strong>ข้อมูลระยะชัดใน LV (DOF info in LiveView)</strong><br>เปิด/ปิดข้อมูลระยะชัดบริเวณข้อมูลระยะโฟกัสใน Live View<br><br> |

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-02-07-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/focus.c)

## E · ค่าแสง

### สมดุลแสงขาว (White Balance)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-item-01.png" width="220" alt="ภาพจำลองเมนู สมดุลแสงขาว — หน้ารายการ"></a><br>หน้ารายการ | ปรับสมดุลสีขาวและการชดเชยสีของภาพ<br><br><strong>วิธีใช้:</strong> เริ่มจาก Kelvin ให้สีโดยรวมเหมาะสม แล้วแก้เขียว/ม่วงหรือฟ้า/ส้มเมื่อจำเป็น |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-01.png" width="220" alt="ภาพจำลองเมนู สมดุลแสงขาว — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>สมดุลแสงขาว (White Balance)</strong><br>ปรับอุณหภูมิสี Kelvin ต่ำให้ภาพมีแนวโน้มเย็นลง สูงให้ภาพอุ่นขึ้นเมื่อใช้ชดเชยกับแสงเดิม<br><br><strong>ปรับสมดุลเขียว/ม่วง (WBShift G/M)</strong><br>ชดเชยไปทางเขียว (Green) หรือม่วงแดง (Magenta) ใช้แก้สีเพี้ยนจากแหล่งแสง<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-02.png" width="220" alt="ภาพจำลองเมนู สมดุลแสงขาว — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ปรับสมดุลน้ำเงิน/อำพัน (WBShift B/A)</strong><br>ชดเชยไปทางฟ้า (Blue) หรือส้มอำพัน (Amber)<br><br><strong>ตัวคูณสีแดง (R multiplier)</strong><br>ตัวคูณช่องสีแดงของ Custom White Balance เป็นการปรับขั้นสูง<br><br><strong>ตัวคูณสีเขียว (G multiplier)</strong><br>ตัวคูณช่องสีเขียวของ Custom White Balance<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-03.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-options-03.png" width="220" alt="ภาพจำลองเมนู สมดุลแสงขาว — ตัวเลือกหน้า 3"></a><br>ตัวเลือกหน้า 3 | <strong>ตัวคูณสีน้ำเงิน (B multiplier)</strong><br>ตัวคูณช่องสีน้ำเงินของ Custom White Balance<br><br><strong>เคลวิน + G/M ออโต้ (Auto adjust Kelvin + G/M)</strong><br>ปรับ Kelvin และ G/M อัตโนมัติหนึ่งครั้งจาก Live View ไม่ใช่การติดตามสีขาวต่อเนื่องทุกเฟรม<br><br> |

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ISO

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-item-01.png" width="220" alt="ภาพจำลองเมนู ISO — หน้ารายการ"></a><br>หน้ารายการ | ปรับความไวแสงและดูองค์ประกอบการขยายสัญญาณทั้งอนาล็อกและดิจิทัล<br><br><strong>วิธีใช้:</strong> เริ่มจาก ISO ปกติของ Canon ก่อนใช้ตัวปรับขั้นสูงที่แยกองค์ประกอบ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-options-01.png" width="220" alt="ภาพจำลองเมนู ISO — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ISO เทียบเท่า (Equivalent ISO)</strong><br>ค่า ISO เทียบเท่าที่รวมผลขององค์ประกอบอนาล็อกและดิจิทัล<br><br><strong>ISO แอนะล็อก Canon (Canon analog ISO)</strong><br>ส่วนการขยายสัญญาณอนาล็อกที่ใช้กับเซนเซอร์<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-options-02.png" width="220" alt="ภาพจำลองเมนู ISO — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ISO ดิจิทัล Canon (Canon digital ISO)</strong><br>ส่วนการขยายดิจิทัลของ Canon ต้นทางแนะนำค่า 0 สำหรับตัวชดเชยส่วนนี้<br><br><strong>ISO ดิจิทัล ML (ML digital ISO)</strong><br>ตัวชดเชยดิจิทัลของ Magic Lantern; ค่าลบเปลี่ยนลักษณะการเก็บไฮไลต์ แต่ไม่เท่ากับเพิ่มความสามารถรับแสงของเซนเซอร์<br><br> |

- ค่าที่แสดงและการปรับได้ขึ้นกับโหมดภาพนิ่ง/วิดีโอและข้อจำกัดของ Canon

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### ความเร็วชัตเตอร์ (Shutter)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-03-item-01.png" width="220" alt="ภาพจำลองเมนู ความเร็วชัตเตอร์ — หน้ารายการ"></a><br>หน้ารายการ | ปรับความเร็วชัตเตอร์และดูค่าที่เกี่ยวข้อง เช่น APEX Tv หรือมุมชัตเตอร์เทียบเท่า<br><br><strong>วิธีใช้:</strong> เลือกเวลารับแสงให้เหมาะกับการเคลื่อนไหวและอัตราเฟรม สำหรับวิดีโอควรตรวจการกะพริบจากแหล่งแสงด้วย |

- เวลารับแสงนานขึ้นทำให้ภาพสว่างขึ้นและเบลอจากการเคลื่อนไหวมากขึ้น
- ตัวแก้ไขค่าละเอียดอาจเปิดผ่าน Q และยังเป็นหน้าควบคุมเดิม

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### รูรับแสง (Aperture)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-04-item-01.png" width="220" alt="ภาพจำลองเมนู รูรับแสง — หน้ารายการ"></a><br>หน้ารายการ | ปรับรูรับแสงและแสดงค่า APEX Av ที่เกี่ยวข้อง<br><br><strong>วิธีใช้:</strong> เลือก f-number ให้เหมาะกับแสงและระยะชัด แล้วตรวจภาพจริง |

- f-number ต่ำคือรูรับแสงกว้างและมักได้ระยะชัดตื้น; f-number สูงคือรูแคบและมักได้ระยะชัดมากขึ้น
- ต้องใช้เลนส์ที่กล้องควบคุมรูรับแสงได้ เลนส์มือหมุนอาจต้องปรับที่เลนส์

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/shoot.c)

### รูปแบบภาพ (Picture Style)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-item-01.png" width="220" alt="ภาพจำลองเมนู รูปแบบภาพ — หน้ารายการ"></a><br>หน้ารายการ | เลือกสไตล์ภาพและค่าการประมวลผล เช่น ความคม คอนทราสต์ และสี<br><br><strong>วิธีใช้:</strong> เลือกสไตล์หลักก่อน แล้วปรับค่ารายละเอียดตามงานที่ต้องการ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-01.png" width="220" alt="ภาพจำลองเมนู รูปแบบภาพ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>รูปแบบที่ใช้อยู่ (Active style)</strong><br>Picture Style ที่ใช้อยู่ขณะนี้<br><br><strong>ความคมชัด (Sharpness)</strong><br>ระดับการเน้นความคมของขอบภาพ<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-02.png" width="220" alt="ภาพจำลองเมนู รูปแบบภาพ — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ความเปรียบต่าง (Contrast)</strong><br>ความต่างส่วนสว่างและส่วนมืด<br><br><strong>ความอิ่มตัวของสี (Saturation)</strong><br>ความอิ่มสี<br><br><strong>โทนสี (Color Tone)</strong><br>การเลื่อนโทนสีตามการปรับของ Picture Style<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-03.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-options-03.png" width="220" alt="ภาพจำลองเมนู รูปแบบภาพ — ตัวเลือกหน้า 3"></a><br>ตัวเลือกหน้า 3 | <strong>บังคับรูปแบบขณะบันทึก (Force style for REC)</strong><br>บังคับใช้ Picture Style ที่ระบุขณะบันทึกวิดีโอ<br><br><strong>รูปแบบภาพขณะบันทึก (Style for recording)</strong><br>สไตล์ที่จะใช้เมื่อเปิด Force style for REC<br><br> |

- Picture Style มีผลกับ JPEG และภาพวิดีโอที่ประมวลผลแล้ว สำหรับ RAW ค่าบางส่วนเป็นข้อมูลประกอบการแสดง/แปลง ไม่ใช่การเปลี่ยนข้อมูลเซนเซอร์แบบเดียวกับ JPEG

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/picstyle.c)

### Dual ISO

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" width="220" alt="ภาพจำลองเมนู Dual ISO — หน้ารายการ"></a><br>หน้ารายการ | ใช้ ISO สองระดับสลับเป็นกลุ่มแถวเซนเซอร์ เพื่อช่วยเพิ่มช่วงรับแสงหลังประมวลผลไฟล์<br><br><strong>วิธีใช้:</strong> ต้องโหลด dual_iso.mo ที่ตรงกับบิลด์ อ่านข้อจำกัดของโมดูล และเตรียมขั้นตอนแปลงไฟล์ด้วยเครื่องมือ Dual ISO เช่น cr2hdr ก่อนใช้จริง |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" width="220" alt="ภาพจำลองเมนู Dual ISO — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>ISO กู้รายละเอียด (Recovery ISO)</strong><br>ISO สำหรับแถวอีกชุดหนึ่ง เลือกเป็น ISO ตายตัวหรือความต่าง EV เทียบกับ ISO หลักได้ตามตัวเลือกที่โมดูลเปิดให้<br><br><strong>ช่วงแสงที่เพิ่มขึ้น (Dynamic range gained)</strong><br>ค่าประมาณขอบเขตสูงสุดของช่วงรับแสงที่เพิ่มขึ้น เป็นค่าอ่านอย่างเดียว ไม่ใช่ผลวัดภาพจริงทุกฉาก<br><br><strong>ช่วงทับซ้อนโทนกลาง (Midtone overlapping)</strong><br>ช่วงซ้อนทับของโทนกลางที่ได้ความละเอียดดีกว่า ส่วนไฮไลต์/เงามีข้อแลกเปลี่ยนด้านความละเอียดและ aliasing/moire<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png" width="220" alt="ภาพจำลองเมนู Dual ISO — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>สลับทุกภาพ (Every other frame)</strong><br>สลับถ่ายภาพที่เปิด Dual ISO กับภาพที่ไม่เปิด<br><br><strong>คำนำหน้าชื่อไฟล์ (Custom file prefix)</strong><br>เปลี่ยนคำนำหน้าชื่อไฟล์เป็น DUAL เมื่อรองรับ ต้นทางระบุว่าไม่น่าเชื่อถือเมื่อถ่ายต่อเนื่องหรือเร็วมาก<br><br> |

- ไม่ใช่การถ่ายคร่อมสองภาพตามปกติ และไม่ใช่ฟังก์ชันที่เปิดแล้วได้ JPEG HDR สำเร็จทันที
- เมนูจะยังใช้งานไม่ได้เมื่อโมดูลไม่ได้ลงทะเบียน การมีชื่อ Dual ISO ใน Photo UI ไม่ยืนยันว่าเปิดใช้งานบนกล้องสำเร็จแล้ว

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-06-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/modules/dual_iso/dual_iso.c)

### ETTR อัตโนมัติ (Auto ETTR)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" width="220" alt="ภาพจำลองเมนู ETTR อัตโนมัติ — หน้ารายการ"></a><br>หน้ารายการ | ปรับค่าแสงเพื่อให้ข้อมูล RAW อยู่ทางขวาของฮิสโตแกรมโดยรักษาไฮไลต์ตามเป้าหมายที่ตั้ง<br><br><strong>วิธีใช้:</strong> ต้องโหลด ettr.mo เลือกวิธีเรียกทำงาน กำหนดชัตเตอร์ช้าที่สุดและเผื่อไฮไลต์ แล้วตรวจไฟล์ RAW |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" width="220" alt="ภาพจำลองเมนู ETTR อัตโนมัติ — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>เงื่อนไขเริ่มทำงาน (Trigger mode)</strong><br>Always ON ปรับตามจังหวะที่รองรับ; Auto Snap อาจสั่งภาพเพิ่มหลังวัด; Press SET และ HalfS DblClick เรียกจากปุ่มเมื่อฮาร์ดแวร์/โหมดรองรับ ไม่ใช่ทุกตัวเลือกจะใช้ได้ใน Live View ทุกกล้อง<br><br><strong>ชัตเตอร์ช้าที่สุด (Slowest shutter)</strong><br>ชัตเตอร์ช้าที่สุดที่ยอมให้ระบบเลือก ป้องกันการลากเวลารับแสงเกินความต้องการ<br><br><strong>ค่าแสงเป้าหมาย (Exposure target)</strong><br>เป้าหมายไฮไลต์ ต้นทางแนะนำเผื่อประมาณ -0.5 หรือ -1 EV จากจุดอ้างอิงของระบบ<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" width="220" alt="ภาพจำลองเมนู ETTR อัตโนมัติ — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>สัดส่วนแสงจ้าที่ยอมข้าม (Highlight ignore)</strong><br>สัดส่วนพิกเซลสว่างที่ยอมให้เกินเป้าหมาย เช่น จุดสะท้อนเล็ก ๆ<br><br><strong>ยอมให้แสงล้น (Allow clipping)</strong><br>กำหนดว่าจะยอมให้ช่องสีใดล้นค่าได้: ไม่ยอม, ช่องเขียว หรือช่องใดก็ได้<br><br><strong>SNR โทนกลาง (Midtone SNR limit)</strong><br>จำกัดการลดแสงเมื่อสัญญาณต่อสัญญาณรบกวนของพื้นที่โทนกลางต่ำกว่าเกณฑ์ อาจแลกกับไฮไลต์ล้นมากขึ้น<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" width="220" alt="ภาพจำลองเมนู ETTR อัตโนมัติ — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>เกณฑ์สัญญาณส่วนมืด (Shadow SNR limit)</strong><br>เกณฑ์ลักษณะเดียวกันสำหรับบริเวณเงา<br><br><strong>เชื่อมชัตเตอร์ Canon (Link to Canon shutter)</strong><br>เชื่อมการกำหนดชัตเตอร์ช้าที่สุดกับการปรับชัตเตอร์จาก Canon ตามการรองรับของโมดูล<br><br><strong>เชื่อมกับ Dual ISO (Link to Dual ISO)</strong><br>ยอมให้ ETTR ปรับหรือปิด Dual ISO เมื่อไม่จำเป็น เพื่อให้ได้เกณฑ์โทนกลางและเงาที่ตั้งไว้<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png" width="220" alt="ภาพจำลองเมนู ETTR อัตโนมัติ — สถานะก่อนโหลดโมดูล"></a><br>สถานะก่อนโหลดโมดูล | ภาพแสดงสถานะก่อนโหลดโมดูล; คำอธิบายต่อไปนี้อ้างอิงโค้ดเมื่อโหลดแล้ว<br><br><strong>แสดงบริเวณวัดแสง (Show metered areas)</strong><br>แสดงพื้นที่ที่ใช้วัดส่วนสว่าง โทนกลาง และเงา<br><br><strong>อนุญาตเสียงเตือน (Allow beeps)</strong><br>สัญญาณเสียงสถานะ: 1 ครั้งสำเร็จ, 2 ครั้งต้องการภาพเพิ่ม, 3 ครั้งผิดพลาด ตามต้นทาง<br><br><strong>แสดงข้อมูลตรวจสอบ (Show debug info)</strong><br>ข้อมูลวินิจฉัยของโมดูลสำหรับตรวจการทำงาน<br><br> |

- ตัวเลือกขั้นสูงบางรายการถูกซ่อนตามโหมด/การรองรับ และบางตัวเลือกปรากฏเมื่อเปิดโมดูลที่เกี่ยวข้องเท่านั้น

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-03-07-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/modules/ettr/ettr.c)

## O · ตัวช่วยแสดงภาพ

### zebra settings

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-item-01.png" width="220" alt="ภาพจำลองเมนู zebra settings — หน้ารายการ"></a><br>หน้ารายการ | แสดงแถบลายบนพื้นที่สว่างหรือมืดเกินเกณฑ์ เพื่อช่วยประเมินค่าแสง<br><br><strong>วิธีใช้:</strong> เปิดตัวช่วยแสดงภาพก่อน แล้วเลือกชนิดการวัดและเกณฑ์ที่ต้องการ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-01.png" width="220" alt="ภาพจำลองเมนู zebra settings — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ระบบสี (Color Space)</strong><br>Luma วัดความสว่างรวม, RGB แยกตามช่องสี; Luma Fast เป็นวิธีเร็วเมื่อมีให้เลือก<br><br><strong>เตือนส่วนมืด (Underexposure)</strong><br>เกณฑ์พื้นที่ที่ถือว่ามืดเกิน<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-02.png" width="220" alt="ภาพจำลองเมนู zebra settings — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>เตือนส่วนสว่าง (Overexposure)</strong><br>เกณฑ์พื้นที่ที่ถือว่าสว่างเกิน<br><br><strong>ขณะบันทึกวิดีโอ (When recording)</strong><br>ซ่อนหรือแสดงลาย Zebra ระหว่างบันทึกวิดีโอ<br><br><strong>ใช้ RAW เตือนแสง (Use RAW zebras)</strong><br>เลือกใช้ข้อมูล RAW เมื่อมี: OFF, Always หรือ Photo only การรองรับขึ้นกับโหมด<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-03.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-options-03.png" width="220" alt="ภาพจำลองเมนู zebra settings — ตัวเลือกหน้า 3"></a><br>ตัวเลือกหน้า 3 | <strong>เตือนส่วนมืดจาก RAW (Raw zebra underexposure)</strong><br>เกณฑ์ด้านมืดของ RAW Zebra แยกจากเกณฑ์แบบภาพแสดงผล<br><br> |

- ลายบนจอเป็นตัวช่วย ไม่ได้เขียนทับเป็นลายลงในไฟล์ภาพตามปกติ ควรแยกเกณฑ์ RAW ออกจาก JPEG/Live View

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### Focus Peaking

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-item-01.png" width="220" alt="ภาพจำลองเมนู Focus Peaking — หน้ารายการ"></a><br>หน้ารายการ | ทำเครื่องหมายบริเวณที่ระบบเห็นว่ามีรายละเอียดคม เพื่อช่วยหมุนโฟกัส<br><br><strong>วิธีใช้:</strong> เปิดตัวช่วยแสดงภาพ แล้วปรับความไวให้เห็นรายละเอียดสำคัญโดยไม่ขึ้นเครื่องหมายทั่วจอ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-options-01.png" width="220" alt="ภาพจำลองเมนู Focus Peaking — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ลักษณะขอบที่ตรวจจับ (Filter bias)</strong><br>เลือกเน้นขอบแรง สมดุล หรือรายละเอียดเล็ก ในการตรวจความคม<br><br><strong>เกณฑ์จุดชัด (Threshold)</strong><br>สัดส่วนพิกเซลที่ระบบนับว่าอยู่ในโฟกัส เป็นความไวของตัวช่วย ไม่ใช่ค่าความคมไฟล์<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-options-02.png" width="220" alt="ภาพจำลองเมนู Focus Peaking — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>สี (Color)</strong><br>สีคงที่หรือการไล่สีตาม Global Focus/Local Focus<br><br><strong>แสดงภาพขาวดำ (Grayscale image)</strong><br>แสดงภาพ Live View เป็นขาวดำเพื่อให้สี Peaking เห็นง่าย<br><br> |

- Peaking เป็นตัวช่วยประเมิน ไม่ใช่การรับรองว่าโฟกัสตรงทุกครั้ง ตรวจภาพขยายร่วมด้วย

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### ขยายช่วยโฟกัส (Magic Zoom)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-item-01.png" width="220" alt="ภาพจำลองเมนู ขยายช่วยโฟกัส — หน้ารายการ"></a><br>หน้ารายการ | แสดงกรอบภาพขยายเพื่อช่วยตรวจโฟกัส รวมถึงขณะบันทึกเมื่อรองรับ<br><br><strong>วิธีใช้:</strong> เลือกจังหวะเปิด ขนาด และตำแหน่งกรอบให้ไม่บังส่วนสำคัญ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-options-01.png" width="220" alt="ภาพจำลองเมนู ขยายช่วยโฟกัส — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>เงื่อนไขเริ่มทำงาน (Trigger mode)</strong><br>กำหนดจังหวะเปิดจากการบันทึก วงแหวนโฟกัส ปุ่มซูม หรือเปิดตลอด ตามชื่อโหมดที่แสดง<br><br><strong>ขนาด (Size)</strong><br>ขนาดกรอบ: เล็ก กลาง ใหญ่ หรือเต็มจอ<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-options-02.png" width="220" alt="ภาพจำลองเมนู ขยายช่วยโฟกัส — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ตำแหน่ง (Position)</strong><br>ผูกกับกรอบโฟกัสหรือวางค้างที่มุมจอที่เลือก<br><br><strong>อัตราขยาย (Magnification)</strong><br>อัตราขยายกรอบ 1:1, 2:1, 3:1 หรือ 4:1; 1:1 ใช้พิกเซลตามคำอธิบายต้นทาง ไม่ใช่การซูมเลนส์<br><br><strong>ยืนยันโฟกัส (Focus confirm)</strong><br>วิธียืนยันความคมด้วยแถบเขียวหรือภาพแยก SplitScreen ตามตัวเลือก<br><br> |

- เป็นกรอบช่วยดู ไม่ใช่การเพิ่มระยะซูมจริงให้ไฟล์บันทึก

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### Histogram

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-item-01.png" width="220" alt="ภาพจำลองเมนู Histogram — หน้ารายการ"></a><br>หน้ารายการ | แสดงการกระจายส่วนมืดและส่วนสว่างของภาพ เพื่อช่วยตรวจเงาจมและไฮไลต์ล้น<br><br><strong>วิธีใช้:</strong> อ่านกราฟร่วมกับภาพและ Zebra โดยเลือกฐานการวัดให้ตรงกับงาน |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-options-01.png" width="220" alt="ภาพจำลองเมนู Histogram — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>รูปแบบฮิสโตแกรม (Histogram type)</strong><br>เลือกฐานข้อมูล YUV/Luma, YUV/RGB, RAW RGB หรือ RAW HistoBar ตามที่เปิดให้ใช้<br><br><strong>แสดง EV จาก RAW (RAW EV indicator)</strong><br>แสดงข้อมูล Dynamic Range หรือคำแนะนำ ETTR บนฮิสโตแกรม RAW หรือปิด<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-options-02.png" width="220" alt="ภาพจำลองเมนู Histogram — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>สเกลกราฟ (Scaling)</strong><br>Linear แสดงสเกลเชิงเส้น; Log ขยายการเห็นส่วนที่มีพิกเซลน้อย<br><br><strong>เตือนส่วนแสงล้น (Clip warning)</strong><br>แสดงจุดเตือนเมื่อช่องสีหนึ่งล้นเกณฑ์<br><br> |

- กราฟจากภาพแสดงผลไม่จำเป็นต้องตรงกับขอบเขต RAW ทั้งหมด

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### วัดความสว่างจุด (Spotmeter)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-05-item-01.png" width="220" alt="ภาพจำลองเมนู วัดความสว่างจุด — หน้ารายการ"></a><br>หน้ารายการ | วัดค่าความสว่างจากบริเวณเล็ก ๆ บนจอ<br><br><strong>วิธีใช้:</strong> เลื่อนหรือจัดจุดวัดไปบริเวณที่ต้องการ เช่น ใบหน้าหรือส่วนสว่าง แล้วอ่านค่าตามหน่วยที่เลือก |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-05-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-05-options-01.png" width="220" alt="ภาพจำลองเมนู วัดความสว่างจุด — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>หน่วยความสว่าง (Spotmeter Unit)</strong><br>หน่วยวัด เช่น เปอร์เซ็นต์, 0–255, RGB แบบรหัสสี, RAW EV หรือ RGB เปอร์เซ็นต์<br><br><strong>ตำแหน่งวัด (Spot Position)</strong><br>เลือกจุดกลางจอหรือผูกกับกรอบโฟกัส<br><br> |

- ค่า RAW EV ใช้ได้เมื่อมีข้อมูล RAW ที่ระบบรองรับ ไม่ใช่การวัดแสงสะท้อนภายนอกกล้อง

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### เส้นกรอบภาพ (Cropmarks)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-item-01.png" width="220" alt="ภาพจำลองเมนู เส้นกรอบภาพ — หน้ารายการ"></a><br>หน้ารายการ | วางกรอบอัตราส่วนหรือเส้นองค์ประกอบทับภาพบนจอ<br><br><strong>วิธีใช้:</strong> เลือกไฟล์กรอบที่มากับแพ็กหรือที่เตรียมไว้ แล้วเลือกว่าจะใช้ในโหมดใด |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-options-01.png" width="220" alt="ภาพจำลองเมนู เส้นกรอบภาพ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ไฟล์เส้นกรอบภาพ (Bitmap)</strong><br>เลือกไฟล์กรอบหรือเส้นจัดภาพ สามารถทำไฟล์เองตามรูปแบบที่ Magic Lantern รองรับ<br><br><strong>แสดงในโหมดภาพนิ่ง (Show in photo mode)</strong><br>เปิด/ปิดกรอบในโหมดภาพนิ่ง<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-options-02.png" width="220" alt="ภาพจำลองเมนู เส้นกรอบภาพ — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>แสดงขณะดูภาพ (Show in PLAY mode)</strong><br>เปิด/ปิดกรอบขณะดูภาพย้อนหลัง<br><br> |

- กรอบช่วยจัดองค์ประกอบ ไม่ได้ตัดขอบไฟล์ภาพให้จริงโดยอัตโนมัติ

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-06-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/cropmarks.c)

### Waveform

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-07-item-01.png" width="220" alt="ภาพจำลองเมนู Waveform — หน้ารายการ"></a><br>หน้ารายการ | แสดงความสว่างตามตำแหน่งแนวนอนของภาพ ช่วยดูว่าแสงส่วนใดสูงหรือต่ำ<br><br><strong>วิธีใช้:</strong> ใช้ตรวจภาพรวมของแสง เช่น ฉากที่มีหน้าต่างสว่างอยู่ด้านหนึ่งของเฟรม |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-07-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-07-options-01.png" width="220" alt="ภาพจำลองเมนู Waveform — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ขนาดกราฟเวฟฟอร์ม (Waveform Size)</strong><br>เลือกขนาดเล็ก ใหญ่ หรือเต็มจอ<br><br> |

- Waveform เป็นตัวช่วยแสดงผลบนจอ และอาจใช้ทรัพยากรประมวลผลเพิ่ม

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-07-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

### เปิดตัวช่วยแสดงภาพ (Global Draw)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-08-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-08-item-01.png" width="220" alt="ภาพจำลองเมนู เปิดตัวช่วยแสดงภาพ — หน้ารายการ"></a><br>หน้ารายการ | สวิตช์หลักของกราฟิกช่วยดูภาพ เช่น Zebra, Peaking และกรอบภาพ<br><br><strong>วิธีใช้:</strong> ถ้าเปิดตัวช่วยย่อยแล้วไม่เห็น ให้ตรวจเมนูนี้และสถานะ Live View/Quick Review ก่อน |

- ตัวเลือกอาจแยก OFF, LiveView, QuickReview และ ON, all modes ตามที่แสดงในโหมดปัจจุบัน
- ตัวช่วยบางอย่างยังขึ้นกับเงื่อนไขเฉพาะของตัวเอง แม้เปิดสวิตช์หลักแล้ว

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-04-08-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/zebra.c)

## V · วิดีโอ

### Bitrate (CBR)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-item-01.png" width="220" alt="ภาพจำลองเมนู Bitrate (CBR) — หน้ารายการ"></a><br>หน้ารายการ | ปรับวิธีควบคุมอัตราข้อมูลวิดีโอ H.264<br><br><strong>วิธีใช้:</strong> เริ่มจาก FW default ก่อน หากปรับ CBR ให้ทดสอบบันทึกด้วยการ์ดและฉากที่จะใช้งานจริง |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-options-01.png" width="220" alt="ภาพจำลองเมนู Bitrate (CBR) — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>Mode</strong><br>FW default ใช้ค่าปกติ; CBR ปรับด้วยตัวคูณ; VBR (QScale) เป็นโหมดขั้นสูงที่ต้นทางระบุว่ามีความเสี่ยงต่อการหยุดบันทึกมากกว่า<br><br><strong>CBR factor</strong><br>ตัวคูณเทียบค่าปกติของ Canon เช่น 1.0× เท่าปกติ ค่าสูงขึ้นต้องการอัตราเขียนการ์ดมากขึ้น ไม่รับประกันคุณภาพเพิ่มตามสัดส่วน<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-options-02.png" width="220" alt="ภาพจำลองเมนู Bitrate (CBR) — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>QScale</strong><br>ตัวกำหนดคุณภาพของโหมด VBR ต้นทางระบุ -16 เป็นฝั่งคุณภาพสูงและแนะนำหลีกเลี่ยงหากไม่จำเป็น<br><br><strong>Bitrate Info</strong><br>ข้อมูลอัตราข้อมูลที่จะแสดง: A คือเฉลี่ย, B คือขณะนั้น, Q คือ QScale ขณะนั้น<br><br><strong>BuffWarnLevel</strong><br>เกณฑ์บัฟเฟอร์ที่โปรแกรมจะลดงานกราฟิกหนักเพื่อช่วยการบันทึก<br><br> |

- ไม่ได้ปลดข้อจำกัดเวลาหรือขนาดไฟล์ทุกอย่างของ Canon และบิตเรตสูงเกินไปอาจทำให้บันทึกหยุด

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/bitrate.c)

### เวลาในการบันทึก (Time Indicator)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-02-item-01.png" width="220" alt="ภาพจำลองเมนู เวลาในการบันทึก — หน้ารายการ"></a><br>หน้ารายการ | เลือกรูปแบบเวลาที่แสดงระหว่างบันทึกวิดีโอ<br><br><strong>วิธีใช้:</strong> เลือก OFF, Elapsed, Remain.Card หรือ Remain.4GB ตามข้อมูลที่ต้องการดู |

- Elapsed คือเวลาที่บันทึกไปแล้ว; Remain.Card คือเวลาที่ประเมินจากพื้นที่การ์ด; Remain.4GB คือเวลาที่ประเมินก่อนถึงขนาดไฟล์ 4 GB
- ค่าเวลาคงเหลือเป็นการประมาณและขึ้นกับบิตเรต ไม่ใช่การรับรองว่าจะบันทึกได้เท่านั้นแน่นอน

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/bitrate.c)

### ปุ่มบันทึกวิดีโอ (REC key)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-03-item-01.png" width="220" alt="ภาพจำลองเมนู ปุ่มบันทึกวิดีโอ — หน้ารายการ"></a><br>หน้ารายการ | ใช้การกดชัตเตอร์ครึ่งหนึ่งหรือรีโมตสายที่เข้ากันได้เพื่อเริ่ม/หยุดวิดีโอ<br><br><strong>วิธีใช้:</strong> เปิด HalfShutter แล้วเลือกว่าจะยอมให้ปุ่มสั่งเริ่ม หยุด หรือทั้งสองแบบ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-03-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-03-options-01.png" width="220" alt="ภาพจำลองเมนู ปุ่มบันทึกวิดีโอ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ต้องกดค้าง (Require long press)</strong><br>OFF ใช้ตามจังหวะปกติ; ON (1s) ต้องกดครึ่งหนึ่งค้างประมาณ 1 วินาที<br><br><strong>คำสั่งที่อนุญาต (Allowed actions)</strong><br>Start/Stop ใช้ทั้งเริ่มและหยุด; Start only เริ่มอย่างเดียว; Stop only หยุดอย่างเดียว<br><br> |

- เมนูนี้เปลี่ยนหน้าที่ปุ่มระหว่างโหมดวิดีโอ จึงควรทดลองก่อนถ่ายงานจริง

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/movtweaks.c)

### ตั้งค่าวิดีโอ (Movie Tweaks)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-item-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าวิดีโอ — หน้ารายการ"></a><br>หน้ารายการ | รวมตัวเลือกเสริมระหว่างถ่ายวิดีโอ<br><br><strong>วิธีใช้:</strong> เปิดเฉพาะตัวเลือกที่ต้องใช้ เพื่อให้คาดเดาพฤติกรรมปุ่มและ Live View ได้ง่าย |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-options-01.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าวิดีโอ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>เริ่มบันทึกใหม่อัตโนมัติ (Movie Restart)</strong><br>พยายามเริ่มบันทึกใหม่เมื่อวิดีโอหยุด ไม่รับประกันความต่อเนื่องและอาจมีช่วงภาพขาดระหว่างไฟล์<br><br><strong>แสดงสถานะบันทึก/รอ (REC/STBY notify)</strong><br>แจ้งสถานะบันทึก/พร้อมด้วยเครื่องหมาย ข้อความ หรือเสียงตามตัวเลือก<br><br><strong>เปิด LiveView ค้าง (Force LiveView)</strong><br>กำหนดให้พยายามเปิด/คง Live View ในสถานการณ์ที่รองรับ เช่น เปลี่ยนเลนส์หรือใช้เลนส์มือหมุน<br><br> |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-options-02.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-options-02.png" width="220" alt="ภาพจำลองเมนู ตั้งค่าวิดีโอ — ตัวเลือกหน้า 2"></a><br>ตัวเลือกหน้า 2 | <strong>ล็อกค่าชัตเตอร์ (Shutter Lock)</strong><br>ล็อกการเปลี่ยนชัตเตอร์ในโหมดวิดีโอ โดยให้เปลี่ยนผ่านเมนูค่าแสงของ Magic Lantern แทน<br><br> |

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-05-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/movtweaks.c)

## + · ตั้งค่า

### ภาษา / Language (Language)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-01-item-01.png" width="220" alt="ภาพจำลองเมนู ภาษา / Language — หน้ารายการ"></a><br>หน้ารายการ | เปลี่ยนภาษา Photo UI ระหว่างไทยและอังกฤษ<br><br><strong>วิธีใช้:</strong> เลือกภาษาที่ต้องการแล้วกลับมาดูหน้าหลักเพื่อยืนยันผล |

- ไม่ได้เปลี่ยนภาษาเมนู Canon หรือแปลทุกหน้า Classic/ทุกโมดูล
- หากฟอนต์ PHOTO_TH.BIN ไม่ครบหรือไม่ตรงรุ่น ระบบอาจกลับไปใช้ภาษาอังกฤษ

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/menu.c)

### โมดูลเสริม (Modules)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-02-item-01.png" width="220" alt="ภาพจำลองเมนู โมดูลเสริม — หน้ารายการ"></a><br>หน้ารายการ | เปิดหน้ารายการโมดูลเสริมของ Magic Lantern เพื่อเลือกโหลดความสามารถเพิ่มเติม<br><br><strong>วิธีใช้:</strong> เลือกเฉพาะโมดูลที่ต้องใช้ แล้วออกจากเมนู ปิดกล้องตามปกติ รอไฟการ์ดดับ และเปิดใหม่ จากนั้นตรวจสถานะ OK |

- ใช้ไฟล์ .mo และ 600D_102.sym จากแพ็กเดียวกับ autoexec.bin
- OFF คือยังไม่เปิด; ???/Err/FileErr ไม่ใช่สถานะสำเร็จ ให้เก็บข้อความปัญหาเพื่อตรวจต่อ
- รายชื่อจริงขึ้นกับไฟล์ใน ML/modules/ คู่มือนี้ไม่ได้สมมุติว่าโมดูลทุกตัวถูกโหลดแล้ว

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/module.c)

### การตั้งค่า (Preferences)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-03-item-01.png" width="220" alt="ภาพจำลองเมนู การตั้งค่า — หน้ารายการ"></a><br>หน้ารายการ | เปิดเมนูตั้งค่าระบบเดิมของ Magic Lantern<br><br><strong>วิธีใช้:</strong> เข้าเมนูนี้เพื่อปรับความชอบและพฤติกรรมระบบที่ไม่ได้อยู่ในหน้าถ่ายภาพใหม่ |

- นี่เป็นทางเข้าเมนู Classic ไม่ใช่เมนูย่อยตายตัวชุดเดียว รายการขึ้นกับฟีเจอร์และโมดูลที่ลงทะเบียน
- ใช้ INFO กลับมาที่ Photo UI เมื่อไม่ได้บันทึกวิดีโอ อ่านคำใบ้ของหน้าระบบเดิมก่อนเปลี่ยนค่า

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/menu.c)

### การแสดงผล (Display)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-04-item-01.png" width="220" alt="ภาพจำลองเมนู การแสดงผล — หน้ารายการ"></a><br>หน้ารายการ | เปิดเมนูการแสดงผลเดิมของ Magic Lantern<br><br><strong>วิธีใช้:</strong> ใช้ตั้งค่าจอ/ข้อมูลแสดงผลเพิ่มเติมตามรายการที่มีบนกล้อง |

- รายการภายในขึ้นกับการตั้งค่าและฟีเจอร์ ไม่ได้เปลี่ยนความละเอียดไฟล์ภาพเพียงเพราะปรับการแสดงผล
- ออกด้วยปุ่มตามคำใบ้ของหน้าที่ใช้อยู่ หรือ INFO กลับ Photo UI เมื่อไม่ได้บันทึก

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/tweaks.c)

### เวอร์ชั่น (Version)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-05-item-01.png" width="220" alt="ภาพจำลองเมนู เวอร์ชั่น — หน้ารายการ"></a><br>หน้ารายการ | ตรวจชื่อโครงการ รุ่น Thai-Menu และที่มาของบิลด์ที่กำลังรัน<br><br><strong>วิธีใช้:</strong> เปิด + → เวอร์ชั่น แล้วอ่านแถว Thai-Menu ให้ตรงกับไฟล์ที่ดาวน์โหลด |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-05-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-05-options-01.png" width="220" alt="ภาพจำลองเมนู เวอร์ชั่น — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ชื่อโครงการ (Project)</strong><br>ชื่อโครงการ FIRMWARE ADD-ON<br><br><strong>Thai-Menu</strong><br>รุ่นของโครงการนี้ เช่น v3r5 อ่านจาก build string ของโปรแกรม ไม่ใช่ Canon firmware<br><br><strong>เว็บไซต์โครงการ (Website)</strong><br>เว็บไซต์ itsamachom.github.io/eos_rom_mlv_modifly/ เป็นที่มาของโครงการ<br><br> |

- ชื่อไฟล์เอกสารลงท้าย -doc1 หมายถึงแก้เอกสารในแพ็ก ไม่ได้หมายความว่ารุ่นเฟิร์มแวร์เปลี่ยนจาก v3r5

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/photo-camera-info-600d.h)

### ข้อมูลกล้อง (Camera Info)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-06-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-06-item-01.png" width="220" alt="ภาพจำลองเมนู ข้อมูลกล้อง — หน้ารายการ"></a><br>หน้ารายการ | แสดงรุ่นกล้องและ Canon firmware ที่กล้องรายงาน<br><br><strong>วิธีใช้:</strong> เปิด + → ข้อมูลกล้อง เพื่อตรวจว่าตรงกับกล้องและเป้าหมายที่แพ็กรองรับ |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-06-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-06-options-01.png" width="220" alt="ภาพจำลองเมนู ข้อมูลกล้อง — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>รุ่นกล้อง (Camera Model)</strong><br>ชื่อรุ่นที่ Canon รายงาน เช่น Canon EOS 600D<br><br><strong>เฟิร์มแวร์ Canon (Canon Firmware)</strong><br>รุ่นเฟิร์มแวร์เดิมของ Canon เช่น 1.0.2 ไม่ใช่รุ่น Thai-Menu<br><br> |

- ข้อมูลหน้านี้อ่านอย่างเดียว แก้รุ่นกล้องหรือ Canon firmware จากหน้านี้ไม่ได้

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-06-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/photo-camera-info-600d.h)

### จำนวนชัตเตอร์ (Shutter Count)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-07-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-07-item-01.png" width="220" alt="ภาพจำลองเมนู จำนวนชัตเตอร์ — หน้ารายการ"></a><br>หน้ารายการ | แสดงตัวนับการทำงานชัตเตอร์และ Live View ที่ระบบอ่านจาก Canon<br><br><strong>วิธีใช้:</strong> เปิด + → จำนวนชัตเตอร์ แล้วอ่านแต่ละแถวแยกกัน ไม่ใช้เลขเดียวแทนทุกความหมาย |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-07-options-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-07-options-01.png" width="220" alt="ภาพจำลองเมนู จำนวนชัตเตอร์ — ตัวเลือกหน้า 1"></a><br>ตัวเลือกหน้า 1 | <strong>ชัตเตอร์กลไก (Mechanical Shutter)</strong><br>ตัวนับชัตเตอร์เชิงกลที่ Canon รายงาน<br><br><strong>โหมด Live View (Live View Actuations)</strong><br>ป้ายไทย “โหมด Live View” คำนวณจากตัวนับรวมลบตัวนับชัตเตอร์เชิงกล เป็นจำนวนการทำงานที่เกี่ยวข้อง ไม่ใช่จำนวนไฟล์ภาพที่ถ่ายใน Live View โดยตรง<br><br><strong>รวมการทำงาน (Combined Actuations)</strong><br>ตัวนับรวมการทำงานเชิงกลและ Live View ที่ Canon รายงาน<br><br> |

- หากอ่านตัวนับไม่ได้จะแสดงว่ายังใช้งานไม่ได้ ไม่ใช่แสดงว่าถ่ายไปแล้วศูนย์ภาพ
- ภาพจำลองในแกลเลอรีไม่ใช่ตัวนับจริงจากกล้องของคุณ

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-06-07-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/photo-camera-info-600d.h)

## G · เกมและสคริปต์

### Arkanoid

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-01-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-01-item-01.png" width="220" alt="ภาพจำลองเมนู Arkanoid — หน้ารายการ"></a><br>หน้ารายการ | เปิดเกมตีอิฐที่มาจากโมดูล arkanoid<br><br><strong>วิธีใช้:</strong> เปิด arkanoid ใน Modules แล้วรีสตาร์ตตามปกติ ตรวจ OK จากนั้น G → Arkanoid → เริ่มเกม และยืนยันตามหน้าจอ |

- ต้องมี ML/modules/arkanoid.mo ไม่ใช่สคริปต์ Lua
- หน้าเริ่มเกมใช้ซ้าย/ขวาผ่านหน้าเริ่มและเริ่มลูกบอล ซ้าย/ขวาขยับไม้ SET หยุด/เล่นต่อ Q กลับหน้าเริ่ม ตามเกมเดิม
- ออกโดยปิดเมนู Magic Lantern เช่น ปุ่มถังขยะหรือชัตเตอร์ครึ่งหนึ่งตามหน้าควบคุมเดิม

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-01-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/modules/arkanoid/arkanoid.c)

### Pong

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-02-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-02-item-01.png" width="220" alt="ภาพจำลองเมนู Pong — หน้ารายการ"></a><br>หน้ารายการ | เปิดเกมตีลูกปิงปองจากสคริปต์ Lua<br><br><strong>วิธีใช้:</strong> โหลด lua แล้วรีสตาร์ต ตรวจ OK และรอการสแกนสคริปต์ เข้า G → Pong → Run Script แล้วยืนยัน |

- ใช้ ML/scripts/pong.lua กับ lua.mo ไม่มีโมดูล pong.mo แยกต่างหาก
- ขึ้น/ลงหรือวงล้อเลื่อนไม้ MENU หยุด/เล่นต่อ ปิดเมนู Magic Lantern เพื่อออก
- ไม่ต้องเปิด Autorun เพื่อเล่นครั้งเดียว

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-02-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/scripts/pong.lua)

### Sokoban

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-03-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-03-item-01.png" width="220" alt="ภาพจำลองเมนู Sokoban — หน้ารายการ"></a><br>หน้ารายการ | เปิดเกมดันกล่องจากสคริปต์ Lua<br><br><strong>วิธีใช้:</strong> โหลด lua แล้วรีสตาร์ต เข้า G → Sokoban → Run Script แล้วยืนยัน |

- ใช้ ML/scripts/sokoban.lua กับ lua.mo ไม่มีโมดูล sokoban.mo
- ปุ่มทิศทางขยับตัวละคร/ดันกล่อง Q, MENU หรือถังขยะออกตามหน้าควบคุมเกม
- เก็บโฟลเดอร์ ML/scripts/lib/ จากแพ็กไว้ครบ เพราะเกมใช้ helper ร่วมกัน

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-03-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/scripts/sokoban.lua)

### โมดูลเสริม (Modules)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-04-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-04-item-01.png" width="220" alt="ภาพจำลองเมนู โมดูลเสริม — หน้ารายการ"></a><br>หน้ารายการ | เปิดหน้ารายการโมดูลเสริมของ Magic Lantern เพื่อเลือกโหลดความสามารถเพิ่มเติม<br><br><strong>วิธีใช้:</strong> เลือกเฉพาะโมดูลที่ต้องใช้ แล้วออกจากเมนู ปิดกล้องตามปกติ รอไฟการ์ดดับ และเปิดใหม่ จากนั้นตรวจสถานะ OK |

- ใช้ไฟล์ .mo และ 600D_102.sym จากแพ็กเดียวกับ autoexec.bin
- OFF คือยังไม่เปิด; ???/Err/FileErr ไม่ใช่สถานะสำเร็จ ให้เก็บข้อความปัญหาเพื่อตรวจต่อ
- รายชื่อจริงขึ้นกับไฟล์ใน ML/modules/ คู่มือนี้ไม่ได้สมมุติว่าโมดูลทุกตัวถูกโหลดแล้ว

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-04-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/src/module.c)

### สคริปต์ (Scripts)

| ภาพเมนู — คลิกเพื่อขยาย | หน้าที่และวิธีใช้ |
| --- | --- |
| <a href="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-05-item-01.png" target="_blank" rel="noopener noreferrer"><img src="https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-05-item-01.png" width="220" alt="ภาพจำลองเมนู สคริปต์ — หน้ารายการ"></a><br>หน้ารายการ | เปิดเมนูสคริปต์ที่โมดูล Lua ลงทะเบียนไว้<br><br><strong>วิธีใช้:</strong> โหลด lua ตรวจสถานะ OK แล้วเข้ารายการสคริปต์ที่ต้องการ เลือก Run Script เพื่อรันครั้งเดียว |

- Autorun ใช้ให้สคริปต์เริ่มตอนบูต จึงไม่จำเป็นสำหรับการเปิดเกมชั่วคราว
- รายการที่เห็นขึ้นกับไฟล์ใน ML/scripts/ และผลการโหลด Lua

[ภาพเมนูจำลอง](https://itsamachom.github.io/eos_rom_mlv_modifly/menu-previews/v3r5/th/th-07-05-item-01.png) · [อ้างอิงโค้ด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/b835d83/firmware/modules/lua/lua.c)

## ตัวอย่างการตั้งค่า

### Timelapse ครั้งแรก

1. ตั้งกล้องบนขาตั้ง ล็อกค่าแสง/โฟกัสให้เหมาะสม
2. S → ตั้งค่าการถ่ายภาพ → จำนวนภาพต่อครั้ง ใช้ 1 (OFF) และปิด Snap Simulation
3. S → Time-lapse ตั้งทุก 5 วินาที หยุดหลัง 120 ภาพ แล้วเลือกวิธีเริ่มที่สะดวก
4. ตรวจภาพช่วงสั้นก่อนปล่อยถ่ายยาว และเว้นช่วงให้กล้องเปิดรับแสง/บันทึกทัน

### ถ่ายคร่อมค่าแสง

1. ปิด Canon AEB ก่อน
2. S → ถ่ายคร่อม เลือกชนิดคร่อมค่าแสง จำนวน 3 ภาพ และความต่าง 1 EV เป็นจุดเริ่มทดลอง
3. เลือก Sequence ที่ต้องการ เช่น 0 - + -- ++; จำนวนภาพยังขึ้นกับ Frames
4. ถ่ายหนึ่งชุดแล้วตรวจภาพทั้งสามบนคอมพิวเตอร์ ก่อนเพิ่มระยะ EV หรือจำนวนภาพ

### ใช้ตัวช่วยโฟกัสมือหมุน

1. เปิด Live View และ O → เปิดตัวช่วยแสดงภาพ
2. เปิด Focus Peaking เพื่อเห็นบริเวณคม แล้วใช้ Magic Zoom ตรวจซ้ำ
3. ภาพที่เห็นบนจอเป็นตัวช่วย ไม่ได้เพิ่มรายละเอียดหรือซูมเลนส์ในไฟล์ภาพ

## เมื่อผลไม่เป็นอย่างที่คาด

### ถ่ายหลายภาพทั้งที่กดครั้งเดียว

ตรวจจำนวนภาพต่อครั้งใน Shoot Preferences, Frames ในถ่ายคร่อม และจำนวนภาพของโหมดตั้งเวลาถ่าย Canon ตัวนับ 2/10 วินาทีบอกเวลาเริ่ม ไม่ใช่จำนวนภาพเสมอไป

### เปิด Zebra/Peaking แล้วไม่เห็น

ตรวจ Global Draw, สถานะ Live View, ตัวเลือกซ่อนระหว่างบันทึก และเงื่อนไขของตัวช่วยนั้น

### Dual ISO / Auto ETTR / เกมยังใช้งานไม่ได้

ตรวจไฟล์โมดูล เปิดใน Modules แล้วรีสตาร์ตตามปกติ ต้องเห็น OK ก่อน สำหรับ Pong/Sokoban ใช้ lua ไม่ใช่โมดูลชื่อเกม

### จำนวนชัตเตอร์ไม่ขึ้น

เป็นข้อมูลอ่านอย่างเดียว หากระบบอ่านจาก Canon ไม่สำเร็จจะไม่สร้างตัวเลขขึ้นมา เก็บภาพอาการและรุ่นที่ใช้เพื่อแจ้งปัญหา

### เมนูเป็นอังกฤษบางส่วน

ภาษาไทยใช้กับ Photo UI และวลีที่มีในชุดฟอนต์ หน้า Classic คำเตือนจากโมดูล หรือข้อความที่ยังไม่มีคำแปลอาจยังเป็นอังกฤษ

## คำศัพท์

- **Tv:** ค่า APEX ที่เกี่ยวกับเวลารับแสง/ชัตเตอร์
- **Av:** ค่า APEX ที่เกี่ยวกับรูรับแสง
- **Ae / AE compensation:** การชดเชยแสงอัตโนมัติ ไม่ใช่คำเดียวกับ Av
- **EV:** หน่วยความต่างค่าแสง 1 EV ต่างประมาณหนึ่งสต็อป
- **MLU:** Mirror Lock-Up: ยกและล็อคกระจกสะท้อนก่อนถ่าย
- **DOF:** Depth of Field: ระยะชัด
- **ETTR:** Expose To The Right: จัดค่าแสงให้ข้อมูล RAW เข้าใกล้ด้านสว่างโดยคุมไฮไลต์
- **CBR / VBR:** วิธีควบคุมอัตราข้อมูลวิดีโอ; CBR ของเมนูนี้ใช้ตัวคูณเทียบค่าปกติ ส่วน VBR ใช้ QScale
- **SNR:** อัตราส่วนสัญญาณต่อสัญญาณรบกวน
- **Live View:** การแสดงภาพจากเซนเซอร์บนจอแทนการมองผ่านช่องมองภาพ

## แหล่งที่มาและผู้พัฒนา

อ้างอิงโค้ด `b835d83`; เนื้อหาคู่มือ: website-content/manual-th.json

[คู่มือบนเว็บ](https://itsamachom.github.io/eos_rom_mlv_modifly/manual-th.html) · [คู่มือติดตั้ง](https://itsamachom.github.io/eos_rom_mlv_modifly/download.html#first-install-steps) · [วิดีโอ](https://itsamachom.github.io/eos_rom_mlv_modifly/videos.html)

[YouTube Online2easy](https://www.youtube.com/@Online2easy) · [Facebook Online2easy](https://www.facebook.com/online2easy) · [Online2hobby Blog](https://online2hobby.blogspot.com/)

โครงการอิสระบน Magic Lantern มี Codex/LLM ช่วยพัฒนาและเรียบเรียงคู่มือ เก็บเครดิต/ใบอนุญาตต้นทาง คู่มือไม่ใช่ผลยืนยันการทดสอบบนกล้องจริง
