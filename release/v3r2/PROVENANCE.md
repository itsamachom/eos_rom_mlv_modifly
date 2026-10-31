# v3r2 provenance and open source questions

## Verified

- Source identified by the maintainer: https://github.com/reticulatedpines/magiclantern_simplified
- Upstream comparison revision: **142472e95054d73640f50789ac0fd66325499d82**.
- Initial fork import: **359f828**. All 2,257 imported firmware file blobs match
  the compared upstream revision, including the prebuilt libraries and FIR.
- Actual v3r2 payload source: **5f543089565c1574606ea2436315e6ea5419ce70**.
- Payload delivery commit: **ea38a62**. Later documentation does not imply a
  firmware rebuild or change the source identifier inside BUILD_INFO.json.
- Exact file comparison and inherited artifact SHA256 values are recorded in
  UPSTREAM_COMPARISON.json. Per-file fork changes are in MODIFIED_FILES.json.
- Noto font provenance, license and hash are recorded under
  assets/fonts/noto-sans-thai; Lua/TCC/UMM notices remain in their source trees.

## Unresolved before a new public binary Release

The inherited dietlibc 0.33 archive is GPL-licensed, and the corresponding
implementation source and any patches remain unverified. Lua also extracts
stdio objects from it. PR #321's updated README explicitly states "no build notes
or source in this repository" for dietlibc. Matching the archive bytes to upstream
establishes inheritance, not completeness of corresponding source.

Follow-up evidence: [upstream PR #321](https://github.com/reticulatedpines/magiclantern_simplified/pull/321),
inspected at d727e1e148e48a2a63c1cf1742e71a361ca61361, adds COPYING.DIETLIBC and
COPYING.NEWLIB. Those texts have been retained verbatim in licenses/ with hashes
and paths in UPSTREAM_PR_EVIDENCE.json. The PR identifies
https://sourceware.org/pub/newlib/newlib-1.20.0.tar.gz and documents the historical
Newlib configuration. This resolves the missing-notice/source-reference question
for Newlib at the documentation level; no claim is made that its tarball was
downloaded or that the inherited archives were independently rebuilt.

PR #290 addresses mixed system/dietlibc headers in Lua, not the source of the
historical archive. Neither PR's proposed build/header changes are incorporated
into this fork's existing v3r2 camera payload by this release-documentation work.
Do not change tested ABI/header assumptions merely to prepare a release.

The outstanding maintainer question is narrowed to dietlibc's original source,
version/patch set and available build information. Do not substitute a guessed
tarball or mark the source gate passed solely because a GPL license text is now
present. See SOURCE_PROVENANCE_QUESTION.md for the prepared, unsent follow-up.

The original installer is byte-identical to the compared upstream prebuilt FIR.
It has not been independently rebuilt. Its Makefile references CCF11102.FIR;
that Canon file is not shipped as an update by this fork. This limitation stays
in release notes, rather than claiming a fresh-install hardware test.

This is a technical distribution audit, not legal advice or a certification.
Unresolved evidence is reported as unresolved; no blanket license is assigned
to all inherited files based only on their names.
