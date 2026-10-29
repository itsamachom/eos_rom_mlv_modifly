# Photo UI v2 — full installation package (experimental)

**Canon 600D / Canon firmware 1.0.2 only.** The full ZIP combines the unchanged Photo UI v2 camera payload with the original ML-SETUP.FIR and installation/license/source information. No separate ML download or second overlay installation is required.

อ่าน [คู่มือติดตั้งภาษาไทย](../../PHOTO_UI_V2_INSTALL_TH.md) ก่อนใช้ ไฟล์สำหรับการ์ดคือ **600D-102-PHOTO-UI-v2-FULL-EXPERIMENTAL.zip** ดาวน์โหลดด้วย Download raw file ไม่ใช่ Code > Download ZIP

- กล้องที่ยังไม่เคยมี ML: ยังต้องทำขั้นตอน Firmware Update เพื่อเปิดการบูต ML ครั้งแรกตามคู่มือ โดยใช้ไฟล์ทั้งหมดจาก ZIP เดียวกัน ตัวแพ็กเกจไม่ได้รวม Canon firmware 1.0.2
- กล้องและการ์ดที่ใช้ ML อยู่แล้ว: เปลี่ยนเฉพาะ autoexec.bin และ ML/ หลังสำรองข้อมูล ไม่ต้องเรียก FIR อีก
- ผู้ที่ใช้ Photo UI v2 อยู่แล้ว: ไม่ต้องติดตั้งใหม่ Payload นี้เหมือนรุ่นที่ทดสอบแล้วทุกไบต์

**First-time installation has not been hardware-tested.** User confirmation applies to Photo UI v2 running on a camera with ML already installed; it does not verify a fresh install. The FIR is unchanged and matches the user-supplied 2025-06-20 developer distribution and the source bundle's prebuilt installer; it was not independently rebuilt.

PACKAGE_INFO.json records the original installer hash and payload provenance. SHA256SUMS verifies the complete ZIP. The matching UI source archive remains in [the v2 delivery directory](../photo-ui-v2/600D-PHOTO-UI-v2-source.zip); upstream installer source and its prebuilt FIR are included there. Preserve GPL notices and original attribution when sharing. This fork is Codex/LLM-assisted and is not an upstream-endorsed release.
