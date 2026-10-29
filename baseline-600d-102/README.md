# Canon 600D / 1.0.2: unmodified development baseline

**Hardware-untested. This is not the redesigned UI release.** The original games, ML audio menus and modules remain. Build and checksum success do not establish camera safety.

Download `600D-102-baseline-test.zip` using the file page **Download raw file** button. Do not use **Code → Download ZIP** as a camera-ready package: that downloads the entire repository, including the source archive and documentation.

This package contains `autoexec.bin` and `ML/` only. The installer FIR was deliberately excluded. Use only with a Canon 600D running Canon firmware 1.0.2, with ML already installed and an already working ML-bootable card. Do not run a firmware update or change boot flags for this test.

## Preparation and rollback

1. Back up the entire working ML card to a computer and confirm the backup is readable.
2. With the card out of the powered-off camera, rename its existing `ML` directory to `ML_OLD` and `autoexec.bin` to `autoexec_OLD.bin`.
3. Extract the test package on a computer. Copy its `autoexec.bin` and `ML/` directly to the root of the card, not into DCIM or another enclosing directory. Do not merge old settings into the new ML directory. Do not format the card.
4. Eject properly, insert into the powered-off camera and use a fully charged battery. Check boot and the ML version page first. Do not enable extra modules or special shooting features initially.
5. Test a few ordinary stills, playback, Live View, focus peaking and histogram, then a short Canon video. Inspect saved photos/video/audio on a computer. Actual recorded-fps measurement has not been implemented.
6. If the camera hangs, try switching off; if unresponsive, remove the battery. Stop testing. On the computer, rename the test `ML` and `autoexec.bin` aside, then restore `ML_OLD` to `ML` and `autoexec_OLD.bin` to `autoexec.bin` before trying the old build again. Never boot the ML card with its autoexec.bin missing.

## Source and build information

The accompanying source ZIP is the complete uploaded source used for this baseline, with no original source-content changes. It has no Git metadata proving that it is the same commit as the 2025-06-20 reference build. See COPYING for the source license and BUILD_REPORT.md for the toolchain and known build warnings. Preserve upstream notices and licenses when redistributing. Build dates vary; this is not a claim of bit-for-bit reproducibility.

Build helper paths describe the prepared cloud environment: source under `/workspace/ml-source/magiclantern_simplified-dev`, helpers under `/workspace/ml-env`. They are reference instructions, not a Windows installer. No camera installation occurs automatically.
