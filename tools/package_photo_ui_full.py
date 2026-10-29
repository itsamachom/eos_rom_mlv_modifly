"""Combine the unchanged v2 payload and original 600D.102 installer offline.

No firmware rebuild, installer patch, boot flag operation or hardware action.
"""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
v2 = root / "deliveries/photo-ui-v2"
out = root / "deliveries/photo-ui-v2-full"
out.mkdir(parents=True, exist_ok=True)
for line in (v2 / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split("  ", 1)
    assert hashlib.sha256((v2 / name).read_bytes()).hexdigest() == digest, name
fir = (root / "firmware/platform/600D.102/ML-SETUP.FIR").read_bytes()
fir_hash = "7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3"
assert len(fir) == 65852 and hashlib.sha256(fir).hexdigest() == fir_hash
dest = out / "600D-102-PHOTO-UI-v2-FULL-EXPERIMENTAL.zip"
source_info = json.loads((v2 / "BUILD_INFO.json").read_text())
source_note = f'''Photo UI v2 source commit: {source_info['source_commit']}
Source tree: https://github.com/itsamachom/eos_rom_mlv_modifly/tree/{source_info['source_commit']}/firmware
Matching source archive: deliveries/photo-ui-v2/600D-PHOTO-UI-v2-source.zip
Source archive is distributed in this repository alongside the firmware package.
Package guide: PHOTO_UI_V2_INSTALL_TH.md
License: COPYING (GPL); preserve original notices.
UI, tests and guides are Codex/LLM-assisted fork changes, not upstream-endorsed.

ML-SETUP.FIR is the original prebuilt 600D.102 installer (unchanged, not independently rebuilt).
Its hash matches both the uploaded 2025-06-20 distributed ZIP and the source bundle's prebuilt file.
Installer SHA256: {fir_hash}
The source archive includes upstream installer source and the original prebuilt installer.
First-time camera installation of this combined package has NOT been hardware-tested.
'''
with zipfile.ZipFile(v2 / "600D-102-PHOTO-UI-v2-TEST.zip") as z:
    assert z.testzip() is None
    payload = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in payload.items():
        z.writestr(name, data)
    z.writestr("ML-SETUP.FIR", fir)
    z.write(root / "PHOTO_UI_V2_INSTALL_TH.md", "INSTALL_TH.md")
    z.write(root / "PHOTO_UI_V2.md", "PHOTO_UI_V2.md")
    z.write(root / "firmware/doc/INSTALL.txt", "INSTALL_UPSTREAM.txt")
    z.write(root / "firmware/COPYING", "COPYING")
    z.writestr("SOURCE.txt", source_note)
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for name, data in payload.items():
        assert z.read(name) == data, name
    assert z.read("ML-SETUP.FIR") == fir
    assert all(n in z.namelist() for n in ("autoexec.bin", "ML-SETUP.FIR", "ML/fonts/argnor23.rbf", "COPYING", "INSTALL_TH.md", "SOURCE.txt"))
    assert not any("ROM" in n.upper() and n.upper().endswith(".BIN") for n in z.namelist())
info = {
    "version": source_info["version"], "target": "600D.102",
    "source_commit": source_info["source_commit"],
    "payload_identical_to_v2": True,
    "user_reported_v2_working_on_already_installed_camera": True,
    "first_install_hardware_tested": False,
    "installer_rebuilt_or_modified": False,
    "installer_sha256": fir_hash,
    "zip_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
    "zip_bytes": dest.stat().st_size,
}
(out / "PACKAGE_INFO.json").write_text(json.dumps(info, indent=2) + "\n")
(out / "SHA256SUMS").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n"
                                       for p in (dest, out / "PACKAGE_INFO.json")))
print(json.dumps(info, indent=2))
