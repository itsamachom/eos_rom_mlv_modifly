# Canon 600D.102 Photo UI v3r3 — Experimental

Camera update: **600D-102-PHOTO-UI-v3r3-FULL-EXPERIMENTAL.zip**. Download with GitHub's Download raw file button. Source ZIP is not the camera update.

- Up/Down and wheel in the middle pane continue across S → F → E → O → V → + → G, wrapping in both directions without editing settings or executing actions.
- Setup (+) contains Language, Modules, Preferences, Display, Version, Camera Info and Shutter Count. The seven requested obsolete shortcuts have been removed.
- เวอร์ชั่น displays Build v3r3, read-only, from the actual build_version string.
- Camera Info is on Setup page 1/2; Shutter Count is on page 2/2. Canon firmware and mechanical/Live View/combined counters remain read-only. Live View is an actuation count, not a direct photo-file count.
- Earlier Thai wording, 25px สำหรับ Timelapse/ถ่ายคร่อม and handheld-mode removal remain.

For future releases, update scripts/photo-ui-version.txt and follow PHOTO_UI_V3R3.md. The build and current packager use that version; the menu derives it from the compiled binary. Existing deliveries cannot be overwritten by the current packager.

For an already ML-enabled Canon EOS 600D with Canon firmware 1.0.2, back up the card and replace autoexec.bin and the entire ML/ directory. Do not run Firmware Update again for this UI update. Read INSTALL_TH.md and UPDATE_TH.md in the Full ZIP.

ARM build, ASan/UBSan Photo UI tests (cross-category buttons/wheel, seven Setup entries, read-only dynamic version, camera/counters), atlas regeneration, production MLU migration, Games registration, 39 linked bindings and packaged module imports passed. No camera or QEMU testing is claimed. The installer is unchanged. Inherited dietlibc corresponding source remains unverified; source-audit limitations and notices are included. Codex/LLM assistance is disclosed in AI_ASSISTANCE.md and UPDATE_TH.md.

Exact working-source ZIP and SHA256SUMS are included alongside this package. BUILD_INFO.json identifies the base commit and exact source ZIP hash; it does not claim that base commit alone contains the complete update. Verify with sha256sum -c SHA256SUMS from this directory.
