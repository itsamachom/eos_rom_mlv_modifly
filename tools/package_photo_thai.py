"""Verify and package a committed TH2 build, font license and matching source."""
import functools
import hashlib
import json
import operator
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib

root = Path(__file__).resolve().parents[1]
sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
paths = ["firmware", "scripts", "tests", "tools", "assets", "translations", "previews", "PHOTO_UI_THAI.md", "INSTALL_PHOTO_THAI_TH.md", "PHOTO_UI_TH2.md"]
subprocess.run(["git", "diff", "--exit-code", "HEAD", "--", *paths], cwd=root, check=True)
out = root / "deliveries/photo-ui-th2"
out.mkdir(parents=True, exist_ok=True)
build = root / "firmware/platform/600D.102/build"
atlas = (root / "firmware/data/photo_thai/PHOTO_TH.BIN").read_bytes()
manifest = json.loads((root / "firmware/data/photo_thai/manifest.json").read_text())
assert hashlib.sha256(atlas).hexdigest() == manifest["atlas_sha256"]
assert "%08x" % zlib.crc32(atlas) == manifest["atlas_crc32"]
expected_modules = {"adv_int", "autoexpo", "deflick", "dual_iso", "ettr", "file_man", "img_name", "pic_view", "silent"}
with zipfile.ZipFile(build / "magiclantern.zip") as z:
    assert z.testzip() is None
    payload = {n: z.read(n) for n in z.namelist() if not n.endswith("/") and not n.lower().endswith(".fir")}
binary = payload["autoexec.bin"]
assert b"PHOTO-UI-TH2.600D.102" in binary and sha[:7].encode() in binary
assert len(binary) % 4 == 0 and functools.reduce(operator.xor, struct.unpack("<%dI" % (len(binary)//4), binary), 0) == 0
assert payload["ML/data/PHOTO_TH.BIN"] == atlas
assert payload["ML/fonts/NOTO_THAI_OFL.txt"] == (root / "assets/fonts/noto-sans-thai/OFL.txt").read_bytes()
assert {Path(n).stem for n in payload if n.endswith(".mo")} == expected_modules
assert not any(Path(n).name in {"arkanoid.mo", "pong.lua", "sokoban.lua"} for n in payload)
fir = (root / "firmware/platform/600D.102/ML-SETUP.FIR").read_bytes()
assert hashlib.sha256(fir).hexdigest() == "7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3"
source_note = f'''Photo UI TH2 source commit: {sha}
Source: https://github.com/itsamachom/eos_rom_mlv_modifly/tree/{sha}
Matching source archive: 600D-PHOTO-UI-TH2-source.zip (distributed alongside the camera ZIPs).
GPL notices: COPYING. Font-derived masks: SIL OFL, see ML/fonts/NOTO_THAI_OFL.txt.
Font source/provenance/license: assets/fonts/noto-sans-thai in the source archive.
English fallback is intentional for strings not included in the Thai lexicon.
TH2 has not been hardware-tested. Any included FIR is original, unchanged and not independently rebuilt.
This is a Codex/LLM-assisted fork, not an upstream-endorsed release.
'''
archives = []
for full in (False, True):
    name = "600D-102-PHOTO-UI-TH2-" + ("FULL-EXPERIMENTAL" if full else "TEST") + ".zip"
    dest = out / name
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in payload.items():
            assert n == "autoexec.bin" or n.startswith("ML/"), n
            z.writestr(n, data)
        if full:
            z.writestr("ML-SETUP.FIR", fir)
        for src, dst in (("firmware/COPYING", "COPYING"), ("firmware/doc/INSTALL.txt", "INSTALL_UPSTREAM.txt"),
                         ("PHOTO_UI_TH2.md", "PHOTO_UI_TH2.md")):
            z.write(root / src, dst)
        # Keep the historical TH1 source guides intact; name this build correctly inside its ZIP.
        z.writestr("PHOTO_UI_THAI.md", (root / "PHOTO_UI_THAI.md").read_text().replace("TH1", "TH2"))
        z.writestr("INSTALL_TH.md", (root / "INSTALL_PHOTO_THAI_TH.md").read_text().replace("TH1", "TH2"))
        z.writestr("SOURCE.txt", source_note)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for n, data in payload.items():
            assert z.read(n) == data
        assert ("ML-SETUP.FIR" in z.namelist()) == full
        assert not any("ROM" in n.upper() and n.upper().endswith(".BIN") for n in z.namelist())
    archives.append(dest)
source = out / "600D-PHOTO-UI-TH2-source.zip"
subprocess.run(["git", "archive", "--format=zip", "--prefix=600D-photo-ui-th2-source/", "-o", str(source), sha,
                *paths, "PHOTO_UI_V2.md"], cwd=root, check=True)
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    assert z.read("600D-photo-ui-th2-source/firmware/data/photo_thai/PHOTO_TH.BIN") == atlas
archives.append(source)
info = {"source_commit": sha, "version": "PHOTO-UI-TH2.600D.102", "camera_tested": False,
        "first_install_hardware_tested": False, "host_test_groups_passed": 23, "target_bindings_checked": 33,
        "autoexec_bytes": len(binary), "autoexec_sha256": hashlib.sha256(binary).hexdigest(),
        "font": manifest, "modules": sorted(expected_modules), "installer_unmodified": True}
(out / "BUILD_INFO.json").write_text(json.dumps(info, indent=2) + "\n")
archives.append(out / "BUILD_INFO.json")
(out / "SHA256SUMS").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n" for p in archives))
print(json.dumps(info, indent=2))
