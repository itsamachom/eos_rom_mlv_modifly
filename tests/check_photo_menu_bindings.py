"""Check Photo UI bindings against menu arrays in the actual ARM ELF.

This validates linked-in names and original menu ownership, not camera behavior.
ELF32 and menu_entry layout are specific to this ARM 600D build.
"""
import pathlib
import re
import struct
import sys

root = pathlib.Path(__file__).resolve().parents[1]
path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "firmware/platform/600D.102/build/magiclantern"
data = path.read_bytes()
assert data[:6] == b"\x7fELF\x01\x01", "Expected little-endian ELF32"
eh = struct.unpack_from("<16sHHIIIIIHHHHHH", data)
sections = [struct.unpack_from("<10I", data, eh[6] + i * eh[11]) for i in range(eh[12])]


def memory(addr, size):
    for s in sections:
        if s[1] != 8 and s[3] <= addr and addr + size <= s[3] + s[5]:
            pos = s[4] + addr - s[3]
            return data[pos:pos + size]
    raise AssertionError(f"Unmapped ARM address {addr:x}")


def cstring(addr):
    # Read one byte at a time so strings at section ends remain valid.
    b = bytearray()
    while memory(addr + len(b), 1) != b"\0":
        b.extend(memory(addr + len(b), 1))
        assert len(b) < 1024
    return b.decode("utf-8", errors="replace")


arrays = {
    "customize_menu": "Prefs", "debug_menus": "Debug", "photo_camera_info_menu": "Help", "shoot_menus": "Shoot", "expo_menus": "Expo",
    "picstyle_features_menu": "Expo", "trap_focus_menu": "Focus",
    "focus_menu": "Focus", "zebra_menus": "Overlay", "cropmarks_menu": "Overlay",
    "mov_menus": "Movie", "movie_tweaks_menus": "Movie", "mov_tweak_menus": "Movie Tweaks",
}
registered = set()
for s in sections:
    if s[1] != 2:
        continue
    names = sections[s[6]]
    strtab = data[names[4]:names[4] + names[5]]
    for pos in range(s[4], s[4] + s[5], s[9]):
        name_off, addr, size, *_ = struct.unpack_from("<IIIBBH", data, pos)
        name = strtab[name_off:].split(b"\0", 1)[0].decode()
        if name not in arrays:
            continue
        assert size % 88 == 0, f"Unexpected ARM menu_entry layout: {name}"
        for offset in range(0, size, 88):
            ptr = struct.unpack("<I", memory(addr + offset + 20, 4))[0]
            if ptr:
                registered.add((arrays[name], cstring(ptr)))

header = (root / "firmware/src/photo-menu-600d.h").read_text()
bindings = re.findall(r'\{"[^"]+", "([^"]+)", "([^"]+)"\}', header)
module_bindings = {("Shoot", "Silent Picture"), ("Expo", "Dual ISO"), ("Expo", "Auto ETTR"), ("Games", "Arkanoid")}
for menu, entry in bindings:
    if (menu, entry) in module_bindings:
        # Modules are resolved dynamically on the camera. Check packaged strings.
        mod = {"Silent Picture": "silent", "Dual ISO": "dual_iso", "Auto ETTR": "ettr", "Arkanoid": "arkanoid"}[entry]
        blob = (path.parent / "zip/ML/modules" / (mod + ".mo")).read_bytes()
        assert entry.encode() + b"\0" in blob, (menu, entry)
    elif menu == "Scripts":
        script = {"Pong Game": "pong.lua", "Sokoban Game": "sokoban.lua"}[entry]
        text = (path.parent / "zip/ML/scripts" / script).read_text()
        assert text.split("--[[", 1)[1].strip().splitlines()[0].strip() == entry
        assert (path.parent / "zip/ML/modules/lua.mo").is_file()
    else:
        assert (menu, entry) in registered, f"Unresolved Photo UI binding: {menu} / {entry}"
print(f"PASS {len(bindings)} Photo UI bindings match linked ARM menus or packaged modules")
