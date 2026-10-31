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
