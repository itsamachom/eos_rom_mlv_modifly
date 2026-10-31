# Building the v3r2 camera payload

Payload source commit: **5f543089565c1574606ea2436315e6ea5419ce70**.
Release documentation may have a later commit; that does not change which
source produced the existing payload. Do not call a new HEAD build byte-identical.

Use an isolated checkout of that commit if reproducing the payload. In Codex
cloud tasks use the existing task checkout; do not create a Git worktree unless
the user explicitly requests one. Paths below describe the prepared environment;
the repository itself can be elsewhere when equivalent tool paths are supplied.

## Tools used

- Debian gcc-arm-none-eabi 15:14.2.rel1-1: GCC 14.2.1 (20241119).
- Binutils-arm-none-eabi 2.44-3+23+b1; ARMv5TE / EABI / soft-float.
- libnewlib-dev 4.5.0.20241231-1 provides headers for the toolchain. This is
  distinct from the inherited Newlib 1.20.0 archives linked by the project.
- Python venv used for v3r2: docutils 0.23, pycparser 3.12, Pillow 12.3.0,
  fonttools 4.61.1. Thai shaping requires Pillow RAQM/HarfBuzz support.
- GNU make, native GCC for host tests, readelf, zip/unzip and Git.

The toolchain bootstrap downloads Debian packages through signed APT metadata
and extracts them under /workspace/ml-env/toolchain. Its repository tracks trixie,
so re-running it in the future does not pin identical package versions. Record
versions and artifact hashes; do not disable signatures or TLS verification.

```sh
bash baseline-600d-102/bootstrap-toolchain.sh
python3 -m venv /workspace/ml-env/venv
/workspace/ml-env/venv/bin/pip install \
  docutils==0.23 pycparser==3.12 Pillow==12.3.0 fonttools==4.61.1
bash tests/run-photo-menu-tests.sh
/workspace/ml-env/venv/bin/python tests/check_photo_ui_v3.py
python3 tests/check_game_registration.py
bash scripts/build-photo-ui.sh --clean
python3 tests/check_photo_menu_bindings.py
python3 tests/check_packaged_games.py
python3 tools/package_photo_ui_v3r2.py
```

The build uses four jobs, target 600D.102, CONFIG_QEMU=n and
VERSION=PHOTO-UI-v3r2.600D.102. Dates and Git metadata affect the output; bit-for-bit
reproducibility has not been established. The packager verifies the embedded
source commit/version, autoexec XOR, game/module inventory, source and atlas
identity, original installer hash, ZIP CRCs and SHA256 checksums.

## Installer and inherited libraries

The Full ZIP uses the unchanged prebuilt 600D.102 ML-SETUP.FIR. Its SHA256 is
7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3. It was not
independently rebuilt. Installer code is in firmware/installer and shared source;
the installer Makefile also references CCF11102.FIR. Canon firmware is not
redistributed by this fork as an installation prerequisite.

The firmware links selected members of inherited dietlibc/Newlib .a archives.
Those binaries being present is not proof their corresponding source and all
required notices have been verified. See PROVENANCE.md and READINESS.json before
publishing a binary release. Do not infer that modern libnewlib-dev is the source
of these older linked archive bytes.

Existing TCC memory TODO, duplicate Makefile recipe and Lua stdio-size warnings
are recorded in the previous build reports. No tests on real camera hardware or
QEMU are implied by a successful host build.
