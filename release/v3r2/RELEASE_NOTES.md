# Photo UI v3r2 — Canon 600D / Canon firmware 1.0.2 (Experimental fork)

Prepared release notes; publication readiness is recorded separately in
READINESS.json. Intended classification: **prerelease**, not stable/latest.

This is a release of itsamachom/eos_rom_mlv_modifly, an independent fork based on
Magic Lantern. It is not an official Magic Lantern release and is not endorsed
by Magic Lantern or Canon. Significant fork code, tests and documentation were
created or guided with Codex/LLM assistance; see AI_ASSISTANCE.md.

## Changes

- Thai/English Photo UI with original 23/28/32 font sizes retained.
- Rename the menu to Focus Peaking; retain Histogram, Waveform, Time-lapse,
  bracketing, zebra settings and Movie → Bitrate (CBR).
- Fix the 600D core rule that discarded Games registration despite Arkanoid
  being loaded. Pong/Sokoban remain Lua scripts using lua.mo; instructions are
  included, and Autorun is not enabled automatically.
- Model/Canon firmware details and read-only mechanical/Live View/combined
  shutter counts use available camera properties. Unknown values are not invented.
- No Picture Style work; Silent Picture is excluded from this package.

## Downloads and installation

Use **600D-102-PHOTO-UI-v3r2-FULL-EXPERIMENTAL.zip** as the camera package, not
GitHub's automatically generated Source code ZIP. The Full ZIP contains matching
source under SOURCE/, the original installer, GPL and Thai installation/game
instructions. The separate source ZIP is also distributed alongside the binary.
Check SHA256SUMS before use. The release documentation/license supplement is
additional material and is not a camera payload.

Supported target: **Canon EOS 600D / Rebel T3i / Kiss X5 with Canon 1.0.2 only**.
For an existing ML installation back up the card, then replace autoexec.bin and
ML/ as a matched set; do not run Firmware Update again merely to update this UI.
Read the included instructions for first installation. No Canon firmware updater
or real Canon ROM dump is distributed as an installation prerequisite.

## Evidence and limitations

The existing payload was built from
5f543089565c1574606ea2436315e6ea5419ce70. Recorded checks: clean ARM build,
28 ASan/UBSan groups, 38 menu/module/script bindings, actual Games registry and
Arkanoid init/start host test, packaged Lua helpers/imports, ZIP/source/atlas
integrity, XOR and SHA256. Host fixtures are not camera measurements.

**v3r2 camera operation, gameplay and first installation have not been tested on
hardware. QEMU was not run.** Previous-version user reports do not establish
v3r2 readiness. ML-SETUP.FIR is unchanged from upstream and was not independently
rebuilt. Keep upstream warranty disclaimers and original credits/licenses.

A new public binary Release must wait for the outstanding dependency source/
notice audit in PROVENANCE.md. Publishing this document does not mark that audit
complete. Do not label the release GPL/source-audited until its gates are resolved.
