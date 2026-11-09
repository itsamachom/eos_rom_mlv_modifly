# Canon 600D.102 — v3r2-menu-update2 Experimental

Camera update: **600D-102-PHOTO-UI-v3r2-MENU-UPDATE2-EXPERIMENTAL.zip**. Use GitHub's Download raw file button. The separate source ZIP is not a camera update.

- Thai delay label: สำหรับ Timelapse/ถ่ายคร่อม, increased from 20px to 25px.
- Camera details are still in Setup (+), page 2/3: ข้อมูลกล้อง and จำนวนชัตเตอร์. Scroll down past ตรวจสอบระบบ.
- Live View is the reported combined-minus-mechanical actuation count, not a direct photo-file count.
- Previous mirror-lock wording and handheld-mode removal are retained.

For an already ML-enabled Canon 600D with Canon firmware 1.0.2, back up the card and replace autoexec.bin and the complete ML/ directory. Do not run Firmware Update again for this UI update. See INSTALL_TH.md and MENU_UPDATE.md in the Full ZIP.

ARM build and host tests passed, including keyboard navigation to Camera Info on page 2/3 in Thai and English, model/firmware/counter rows, atlas regeneration/width, MLU migration, 38 bindings and packaged module imports. No camera or QEMU testing is claimed. Existing installer is unchanged.

Exact working source and inherited licenses/provenance records are included. The source state is the base commit plus changes, identified by the source ZIP hash in BUILD_INFO.json. Inherited dietlibc corresponding source remains unverified; see included release/v3r2/PROVENANCE.md and READINESS.json. Codex/LLM assistance is disclosed in MENU_UPDATE.md and AI_ASSISTANCE.md.

Verify this directory using sha256sum -c SHA256SUMS.
