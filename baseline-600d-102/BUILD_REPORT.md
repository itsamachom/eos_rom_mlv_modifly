# Canon 600D.102 baseline build

The uploaded source ZIP builds successfully without changing the contents of any of its 2,257 original files. The existing eos_rom_mlv_modifly Git checkout remains unchanged. ZIP executable permissions were restored from archive metadata for build scripts.

## Prepared workflow

- Source: /workspace/ml-source/magiclantern_simplified-dev
- Distributed reference: /workspace/ml-reference
- Isolated toolchain: /workspace/ml-env/toolchain/usr/bin
- GCC: Debian gcc-arm-none-eabi 15:14.2.rel1-1 (GCC 14.2.1)
- Binutils: Debian 2.44-3+23+b1; Newlib headers: 4.5.0.20241231-1
- Debian packages verified using signed APT repository metadata and package hashes; extracted without system installation.
- Python venv: /workspace/ml-env/venv; required build dependency docutils==0.21.2.
- Build: bash /workspace/ml-env/build-baseline.sh
- Full clean build: bash /workspace/ml-env/build-baseline.sh --clean
- Build uses four jobs, target 600D.102, CONFIG_QEMU=n and default compiler warning settings.

## Verification

Both incremental and full clean builds completed with exit status 0. Packaging checks verify ZIP integrity, embedded autoexec equality, required module/symbol presence and the autoexec XOR checksum. The executable is ELF32 ARM, EABI5 soft-float, entry point 0xc70100.

Reference autoexec.bin is 480,096 bytes; the clean-built file is 480,160 bytes (+64). Both packages contain 51 files and 17 .mo modules, with identical paths; 32 files have identical contents. Full per-file sizes and SHA-256 hashes are in comparison.json. Size similarity does not demonstrate equivalent behavior or camera safety. Source ZIP has no Git provenance proving it matches the distributed reference commit; timestamps and toolchain may also affect outputs.

Expected existing build messages: missing optional doc/cam files (copy explicitly ignored by Makefile; reference package has no files there either); grep broken pipe in the tcc_status pipeline where cmp -s can stop reading early; TCC memory TODO warning; Lua/EDMAC duplicate Makefile recipes; Lua stdio size warnings. No warning flags or verification were disabled. These messages did not prevent the required package build.

## Limits and next work

This is an unmodified development baseline, not a UI-modified release. Games, ML audio menus and original modules are still present. Camera boot, photography, Canon video recording, focus peaking and actual recorded-fps measurement have not been tested. Hardware testing remains required before calling a release usable. No camera installation is part of this validation.

fps_get_current_x1000() in src/fps-engio.c derives fps from hardware timing registers; it is not a count of frames successfully written to the video file. A measured-recording-fps implementation needs additional source investigation and hardware validation.

The source and toolchain live outside the Git checkout and must be retained in the published environment snapshot. Draft configuration saving alone does not publish or verify restoration in a new task. Use the existing isolated environment; do not create a Git worktree unless explicitly requested.
