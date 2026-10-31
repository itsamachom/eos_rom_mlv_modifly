# v3r2 release preparation

**ผู้ดูแลแจ้งว่าสร้าง Draft Release v3r2 ผ่านหน้าเว็บแล้ว แต่ยังไม่ Publish และไม่ประกาศเป็น stable** เอกสารนี้เป็นชุดเตรียมเผยแพร่ของ fork เอง ไม่ใช่การส่ง contribution หรือ release ให้ Magic Lantern upstream

เตรียมไว้แล้ว:

- README, LICENSE, THIRD_PARTY_NOTICES, เครดิตต้นทางและการเปิดเผย AI
- release notes ที่ระบุ target/firmware, experimental status และข้อจำกัดจริง
- source commit ที่ตรงกับ payload และผลเทียบ 2,257 ไฟล์กับ upstream ที่ผู้ใช้ระบุ
- รายการไฟล์ที่ fork แก้ไข, วิธี build, คู่มือเกม/ติดตั้ง และการตรวจ checksum
- เครื่องมือจัด staging โดยรักษาไบนารีเดิม และเครื่องมือเผยแพร่ที่ปฏิเสธการ publish เมื่อ gate ยังไม่ผ่าน

ยังติด:

1. การยืนยันซอร์ส/patches/build information ของ dietlibc archive ที่ upstream และ fork นำมาเป็นไบนารี (พบใบอนุญาตทั้งสองไลบรารีและแหล่ง Newlib แล้วจาก PR #321) ดู PROVENANCE.md และ READINESS.json การตรงกับ archive ต้นทางไม่ได้ยืนยันว่ามี corresponding source ครบ
2. การเผยแพร่แบบอัตโนมัติผ่าน API ยังติด proxy (คำขอครั้งล่าสุดตอบ CONNECT 403) แต่ไม่จำเป็นต้องแก้เครือข่ายเพื่อใช้ Draft บน GitHub ผ่านหน้าเว็บ เมื่อยืนยันซอร์ส dietlibc แล้วสามารถแนบไฟล์และ Publish ผ่านเว็บได้ ไม่มีการขอให้ส่ง token ในแชต

Agent ไม่เปลี่ยนความเป็นส่วนตัวของ repository, ไม่ merge main และไม่สร้าง tag ที่อ้างว่า release สำเร็จ และไม่ส่งข้อความไปหา upstream ในงานนี้

```sh
python3 tools/prepare_v3r2_release.py
python3 tools/publish_v3r2_release.py --check
# หลังแก้ gate และตรวจหลักฐานแล้วเท่านั้น:
python3 tools/publish_v3r2_release.py --publish
```

Staging อยู่ /workspace/release-staging/v3r2 โดยค่าเริ่มต้น ชุดนี้ยังไม่ใช่ release-ready ตราบที่ READINESS.json ยังมี blocker การบันทึก network draft ไม่ใช่การเปิดสิทธิ์ runtime หรือการ publish GitHub Release

หลักฐานเพิ่มเติมจากผลค้นหาของผู้ใช้: [PR #321](https://github.com/reticulatedpines/magiclantern_simplified/pull/321) และ UPSTREAM_PR_EVIDENCE.json คำถามถึงต้นทางปรับให้เหลือ dietlibc แล้ว
