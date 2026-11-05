# 600D.102 v3r2 Menu Update — Experimental

Camera update: **600D-102-PHOTO-UI-v3r2-MENU-UPDATE-EXPERIMENTAL.zip**.
Download this file using GitHub's **Download raw file** button. Do not use the source ZIP as a camera update.

Changes: Thai TV/AV and mirror-lock wording; renamed delay to หน่วงเมื่อถ่าย Time-lapse/ถ่ายคร่อม; removed handheld MLU and its settings on 600D; migrates saved handheld mode to self-timer. The long delay label uses a 20px font to fit in its column.

For an already ML-enabled Canon 600D with Canon firmware 1.0.2, back up the card and replace autoexec.bin plus the complete ML/ directory. Do not run Firmware Update again to apply this UI update. Read INSTALL_TH.md inside the Full ZIP.

Host tests, ARM build, 38 bindings, game-module import checks, ZIP CRC and SHA256 checks passed. This update has not been tested on camera hardware or QEMU. The user confirmed that the previously reported multiple self-timer shots were the configured shot count; no shutter-count fix was applied.

The source ZIP contains the exact working source used for this build, based on 06961d8ee000652948188e98f5a1e70fa8c880c2 plus the included changes. BUILD_INFO.json identifies the base and exact source ZIP hash; the base alone is not the complete updated source. Source and licenses/provenance documents are also included in the Full ZIP. Inherited dietlibc corresponding source remains unverified; see the included release/v3r2/PROVENANCE.md and READINESS.json. This experimental package does not resolve that audit or establish official upstream endorsement. Codex/LLM assistance is disclosed in AI_ASSISTANCE.md and MENU_UPDATE.md.

Verify locally from this folder:

```sh
sha256sum -c SHA256SUMS
```
