# FIRMWARE ADD-ON Thai-Menu v3r4 — Public Experimental

Project website: https://itsamachom.github.io/eos_rom_mlv_modifly/

**Camera download: 600D-102-PHOTO-UI-v3r4-FULL-EXPERIMENTAL.zip**. Use GitHub's Download raw file button. The source ZIP and automatic GitHub Source code archive are not camera updates.

## What changed

The Version screen now shows FIRMWARE ADD-ON, Thai-Menu, the actual v3r4 version and project domain/path with the full project URL below. It no longer uses Build %.*s; version text is bounded before a simple %s conversion. Version, binary marker and package names share scripts/photo-ui-version.txt.

Continuous middle-pane category navigation, the seven-entry Setup menu and earlier wording fixes remain. Camera Info is on Setup page 1/2; Shutter Count is on page 2/2. Live View is an actuation count, not a direct photo-file count.

## Target and update

Canon EOS 600D with Canon firmware 1.0.2 only. For cameras already running ML, back up the card and replace autoexec.bin and the entire ML/ directory. Do not run Firmware Update again for this UI update. Read INSTALL_TH.md and UPDATE_TH.md in the Full ZIP. The inherited installer is unchanged and not independently rebuilt.

## Evidence and limitations

ARM build, ASan/UBSan host tests, restricted-format version regression (including the original failure), bounded/empty/future version strings, read-only identity/version/site in Thai and English, font regeneration, MLU/shutter-property/Games tests, 39 linked bindings, packaged imports, CRC/XOR checks and bilingual browser smoke checks passed. The included host layout proof is not a Canon camera capture or execution of the Canon ROM formatter.

Public Experimental, not Stable. No v3r4 camera or QEMU test is claimed. Inherited dietlibc corresponding implementation source/patches remain unverified; see included release/v3r2/PROVENANCE.md and READINESS.json. The Experimental label and inclusion of fork source do not resolve that audit. This independent Codex/LLM-assisted fork is not endorsed by Canon or Magic Lantern; preserve all original notices and credits.

Exact working source and checksums are provided. BUILD_INFO.json identifies the base commit and source ZIP hash; base alone is not necessarily the complete updated source. Verify with sha256sum -c SHA256SUMS from this directory.
