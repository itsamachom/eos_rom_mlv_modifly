# ดาวน์โหลด / Downloads — FIRMWARE ADD-ON Thai-Menu v3r4

**Canon EOS 600D / Canon firmware 1.0.2 · Public Experimental**
[หน้าเว็บดาวน์โหลดภาษาไทย](https://itsamachom.github.io/eos_rom_mlv_modifly/download.html) · [English download page](https://itsamachom.github.io/eos_rom_mlv_modifly/en/download.html)

## 1. ไฟล์สำหรับอัปเดตกล้อง / Camera update

### [ดาวน์โหลด 600D-102-Thai-Menu-v3r4-UPDATE.zip](https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/site/eos-600d-bilingual/downloads/v3r4/camera/600D-102-Thai-Menu-v3r4-UPDATE.zip)

**2.06 MB** — สำหรับกล้องที่ติดตั้ง ML แล้ว มี autoexec.bin และ ML/ ไม่มี Source ZIP หรือตัวติดตั้ง FIR ไม่ใช่แพ็กเกจสำหรับติดตั้ง ML ครั้งแรก

Back up the card; replace autoexec.bin and the entire ML/ directory at the card root. Do not run Firmware Update again for this UI update. Read INSTALL_TH.md / INSTALL_EN.md inside the ZIP.

SHA256: `4ca725b055f087fc5eb93232baf12a6e477d2da7c72f59e2ebc1f8f7f4217373`

## 2. Source code สำหรับผู้พัฒนา / Developer source

### [ดาวน์โหลด 600D-PHOTO-UI-v3r4-source.zip](https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/v3r4/deliveries/photo-ui-v3r4-full/600D-PHOTO-UI-v3r4-source.zip)

**27.36 MB** — ซอร์ส fork ที่ตรงกับไบนารี ใช้ศึกษา/พัฒนา **ไม่ใช่ไฟล์ลงกล้อง** ไม่ใช้ Code → Download ZIP หรือ Source code ที่ GitHub สร้างอัตโนมัติแทน camera update

Source is pinned to tag [v3r4](https://github.com/itsamachom/eos_rom_mlv_modifly/tree/v3r4). Inherited dietlibc corresponding source remains unverified; including fork source does not close that audit.

SHA256: `77564f9ebc11e5a5f219bd4dd511bd83a39c9a6bb250446724d910612397022d`

## 3. Checksum และข้อมูลรุ่น

- [ดาวน์โหลด SHA256SUMS](https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/site/eos-600d-bilingual/downloads/v3r4/SHA256SUMS) — ตรวจไฟล์ที่เลือก หรือวางทั้งสอง ZIP ไว้ด้วยกันแล้วรัน `sha256sum -c SHA256SUMS`
- [ข้อมูลแพ็กเกจ](https://raw.githubusercontent.com/itsamachom/eos_rom_mlv_modifly/site/eos-600d-bilingual/downloads/v3r4/DOWNLOAD_INFO.json)
- [รายละเอียด v3r4 และข้อจำกัด](https://github.com/itsamachom/eos_rom_mlv_modifly/blob/v3r4/PHOTO_UI_V3R4.md)

ไฟล์สำหรับกล้องใช้ runtime bytes เดียวกับ Full v3r4 เดิมทุกไบต์ เป็นการแยกแพ็กเกจโดยไม่ rebuild เฟิร์มแวร์ รุ่นนี้ยังไม่ได้ทดสอบบนกล้องจริง/QEMU และไม่ใช่ Stable ไม่ใช่บิลด์ที่ Canon/Magic Lantern รับรอง เครดิตและใบอนุญาตต้นทางยังคงอยู่ในแพ็กเกจ

The older Full ZIP bundles camera files and source together. It remains unchanged for archival use; the camera-only UPDATE ZIP above is the recommended download for an existing ML installation.
