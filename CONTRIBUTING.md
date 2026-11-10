# Contributing to this fork

This repository is an independent Magic Lantern fork. Keep upstream credits,
copyright statements, per-file licenses and notices when modifying or sharing.
Use a compatible license for new work and identify copied/derived material and
its source. Do not replace third-party licenses with the repository's GPL text.

Describe the camera model and exact Canon firmware. Keep changes for different
ports separate. Include the reason for the change, observed behavior and the
checks actually run; distinguish host tests from camera tests. Report module
status (OK/OFF/Err/???) when relevant. Never attach Canon ROM dumps, private
photographs, credentials or personal serial-number data to an issue or PR.

Disclose AI/LLM involvement, affected portions and extent in every contribution.
Read AI_ASSISTANCE.md and firmware/LLM_POLICY.md. A contribution to this fork is
not a submission to, or acceptance by, the Magic Lantern upstream project.

Useful existing checks:

```sh
bash tests/run-photo-menu-tests.sh
/workspace/ml-env/venv/bin/python tests/check_photo_ui_v3.py
python3 tests/check_game_registration.py
bash scripts/build-photo-ui.sh --clean
python3 tests/check_photo_menu_bindings.py
python3 tests/check_packaged_games.py
```

Do not publish camera binaries until the release's source, provenance, licenses,
checksums and exact target have been reviewed. Use experimental/prerelease status
until the hardware behavior claimed in the release notes has been tested.

For every Photo UI release, update scripts/photo-ui-version.txt first. The build
script, read-only Version menu and tools/package_photo_ui_current.py share that
version. Add PHOTO_UI_<VERSION>.md notes, stage any new source files, and follow
PHOTO_UI_V3R5.md. Never hardcode the next release label in the menu.

Canon's ROM formatter is not the host libc formatter. Version/identity values
use literal strings, %s or %d; do not reintroduce dynamic precision (%.*s).
The Photo UI tests enforce this subset for camera-info/version callbacks.
