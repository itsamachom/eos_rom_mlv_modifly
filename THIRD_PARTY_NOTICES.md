# Third-party notices and source scope

This file is an attribution index, not a replacement for individual licenses or
an assertion that a legal/source audit is complete. Preserve all original file
headers, notices, license texts and attribution when redistributing.

| Component | Attribution / terms | Source or notice in this repository |
| --- | --- | --- |
| Magic Lantern core and modules | Magic Lantern contributors; GPL, with version/upgrade terms in individual files | firmware/COPYING, firmware/README.md, firmware/doc/CREDITS.txt, source headers |
| TinyCC / runtime module linker | Fabrice Bellard and contributors; original LGPL notices retained | firmware/tcc, firmware/tcc/COPYING, firmware/modules/tcc |
| Lua | Copyright (C) 1994–2015 Lua.org, PUC-Rio; MIT notice | firmware/modules/lua/lua/lua.h, release/v3r2/licenses/LUA-MIT.txt |
| UMM allocator | Copyright (c) 2015 Ralph Hempel; MIT | firmware/modules/lua/umm_malloc/LICENSE |
| Noto Sans Thai and derived Thai phrase masks | 2022 The Noto Project Authors; SIL OFL 1.1 | assets/fonts/noto-sans-thai/OFL.txt, SOURCE.md, release/v3r2/licenses/NOTO-SANS-THAI-OFL-1.1.txt |
| Arkanoid | Original module credits include pravdomil.cz; original GPL notices retained | firmware/modules/arkanoid/README.rst and arkanoid.c |
| Pong / Sokoban scripts | Original source comments and attribution retained byte-for-byte | firmware/scripts/pong.lua, firmware/scripts/sokoban.lua |
| Inherited dietlibc 0.33 archive | Exact upstream binary inheritance verified; GPL notice recovered from PR #321; corresponding archive source remains unverified | firmware/src/libs/dietlib-0.33-none-eabi-Os/dietlibc.a; see release/v3r2/PROVENANCE.md |
| Inherited Newlib 1.20.0 archives | Newlib 1.20.0 source URL/build notes and COPYING.NEWLIB recovered from PR #321; original per-file terms still apply | firmware/src/libs/README.txt, arm-none-eabi-O3 archives and release/v3r2/licenses/NEWLIB-NOTICES.txt |
| GCC runtime | Toolchain-provided libgcc linked into the payload; keep applicable GCC runtime licensing/exception information | Toolchain documentation and release source audit; not a claim that the compiler itself is part of this fork |
| Original ML-SETUP.FIR | Unchanged prebuilt installer distributed by the identified upstream; not a Canon firmware updater | firmware/platform/600D.102/ML-SETUP.FIR; shared installer sources in firmware/installer and firmware/src |

## Identity and provenance

The user identified reticulatedpines/magiclantern_simplified as the source.
Comparison with upstream commit 142472e95054d73640f50789ac0fd66325499d82 found
all **2,257 imported file blobs identical** to the initial imported firmware tree
in commit 359f828. This verifies an exact content match. It does not prove the
original upload's Git history or complete source of prebuilt dependencies.

This fork does not claim authorship of upstream code or fonts, and does not
claim approval, support or endorsement by Magic Lantern, its developers, Canon,
Google, the Noto Project or the third-party authors.

No actual Canon ROM dump was found in the named ROM test fixtures: the two
small files under firmware/tools/ghidra/detect_rom_test_files are textual test
fixtures (63 and 58 bytes). Do not replace these with real camera dumps or
publish installer-generated ML/LOGS/ROM*.BIN files.

See AI_ASSISTANCE.md for fork modifications and LLM disclosure. Before marking a
binary release ready, resolve the source/notices questions in
release/v3r2/READINESS.json rather than treating inherited binaries as proof of
complete corresponding source.

## Follow-up license evidence

Upstream PR #321, inspected at d727e1e148e48a2a63c1cf1742e71a361ca61361,
adds GPL/Newlib license texts. Verbatim copies and hashes are preserved in
release/v3r2/licenses and UPSTREAM_PR_EVIDENCE.json. The proposed README supplies
the Newlib 1.20.0 source URL, but explicitly says dietlibc source/build notes are
not in the repository. This does not resolve the dietlibc corresponding-source
gate. PR #290 is a Lua header compatibility fix; no build fixes were applied to
the camera payload in this documentation update.

## Native JPEG tone recipes (v3r6-tone1 experiment)

The 13 distinct native Picture Style/WB recipes derive from the preview settings in HNGSeries/M-Film 0.2.1 (`8118e9c7c072371bd53eda8920f44910e8a35baf`), `ml-dev/filmos/fos_film.c` and `ml-dev/filmos/tools/genfilms.py`. Credit HNGSeries/M-Film contributors; the derived recipe table retains GPL-2.0-only terms. See `research/jpeg-tones/UPSTREAM_NATIVE_RECIPES.json` and the verbatim GPL text beside it. Recipe names/grouping, transaction adapter and canister menu were implemented for this fork. No Film-Luts tables, M-Film RAW decoder, Darkrooms desktop code or third-party sample photos are included in this feature. These native JPEG approximations do not claim the full developed film looks.

### tone2 original catalog

v3r6-tone2 retains all 72 original preset names, native JPEG preview numbers and ISO conversion from `ml-dev/fork/src/filmroll.c` at the same upstream commit, rather than tone1's 13 deduplicated names. The auditable catalog/source hashes are `research/jpeg-tones/UPSTREAM_ORIGINAL_CATALOG.json`. Preserve the same GPL-2.0-only recipe terms and M-Film contributor attribution. Film names identify source presets and do not imply endorsement or exact photographic reproduction. The independent canister artwork contains no copied upstream textures/logos.

### Stock-specific canister labels (tone4)

The compact label table additionally derives from M-Film's `ml-dev/filmos/tools/catalog.py` and the eight built-in label cues in `ml-dev/filmos/fos_film.c`, pinned to the same 8118e9c commit. Credit HNGSeries/M-Film contributors; preserve GPL-2.0-only terms and the verbatim GPL text in research/jpeg-tones. Source hashes, original ramp/level data and scope are in research/film-labels/CATALOG.json. The independent renderer and compact letterforms are fork changes. No manufacturer photograph, third-party logo artwork, upstream raster label texture or RAW/LUT code is bundled by this change. Brand words identify presets and do not imply endorsement. Actual packaging varies; cross-process/cinema-print illustrations do not claim a retail cartridge existed. External retail-photo verification remains incomplete.

### tone5 cylinder technique review

M-Film's `fos_film.c` at the same pinned 8118e9c commit was reviewed for cylinder-angle texture projection, diffuse/specular/material profiles and palette dithering. Credit M-Film contributors for this approach. The fork implements an independent small integer column-profile adaptation and uses the already shipped RBF fonts, without importing the upstream texture/font engine or custom palette. See research/film-labels/CYLINDER_RENDERING.md and tools/generate_film_cylinder.py. Existing GPL label-data terms and notices remain.
