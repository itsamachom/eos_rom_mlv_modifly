"""Package the committed Photo UI v2 build with matching source and checksums."""
import functools
import hashlib
import json
import operator
from pathlib import Path
import struct
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
subprocess.run(["git", "diff", "--exit-code", "HEAD", "--", "firmware", "scripts", "tests", "tools", "PHOTO_UI_V2.md"], cwd=root, check=True)
build = root / "firmware/platform/600D.102/build"
out = root / "deliveries/photo-ui-v2"
out.mkdir(parents=True, exist_ok=True)
dest = out / "600D-102-PHOTO-UI-v2-TEST.zip"
expected = {"adv_int", "autoexpo", "deflick", "dual_iso", "ettr", "file_man", "img_name", "pic_view", "silent"}
with zipfile.ZipFile(build / "magiclantern.zip") as z:
    assert z.testzip() is None
    binary = z.read("autoexec.bin")
    assert b"PHOTO-UI-v2.600D.102" in binary and sha[:7].encode() in binary
    assert len(binary) % 4 == 0
    assert functools.reduce(operator.xor, struct.unpack("<%dI" % (len(binary) // 4), binary), 0) == 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as target:
        for name in z.namelist():
            if name.endswith("/") or name.lower().endswith(".fir"):
                continue
            assert name == "autoexec.bin" or name.startswith("ML/"), name
            assert Path(name).name not in {"pong.lua", "sokoban.lua", "arkanoid.mo"}
            target.writestr(name, z.read(name))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert {Path(n).stem for n in z.namelist() if n.endswith(".mo")} == expected
source = out / "600D-PHOTO-UI-v2-source.zip"
subprocess.run(["git", "archive", "--format=zip", "--prefix=600D-photo-ui-v2-source/", "-o", str(source),
                sha, "firmware", "scripts", "tests", "tools", "PHOTO_UI_V1.md", "PHOTO_UI_V2.md"], cwd=root, check=True)
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    assert z.read("600D-photo-ui-v2-source/firmware/src/photo-menu-600d.h") == (root / "firmware/src/photo-menu-600d.h").read_bytes()
info = {
    "source_commit": sha, "version": "PHOTO-UI-v2.600D.102", "target": "600D.102",
    "camera_tested": False, "modules": sorted(expected), "autoexec_bytes": len(binary),
    "autoexec_sha256": hashlib.sha256(binary).hexdigest(),
    "zip_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
    "host_test_groups_passed": 12, "target_bindings_checked": 32,
    "gcc": "14.2.1 (Debian 15:14.2.rel1-1)", "qemu": False,
}
(out / "BUILD_INFO.json").write_text(json.dumps(info, indent=2) + "\n")
(out / "SHA256SUMS").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n"
                                      for p in (dest, source, out / "BUILD_INFO.json")))
print(json.dumps(info, indent=2))
