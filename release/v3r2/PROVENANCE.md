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

The upstream and fork both contain prebuilt dietlibc/Newlib archives. The linked
dietlibc object members are referenced in firmware/platform/Makefile; Lua also
extracts stdio objects into lua.mo. The source bundle contains dietlibc headers,
but the corresponding implementation source for these linked archives has not
been found or verified in the inspected upstream tree. Newlib 1.20.0 is named by
firmware/src/libs/README.txt, but the full original source/notices and any patch
set used for those archive bytes have not been established either.

An exact match to upstream archive bytes establishes inheritance, not completeness
of corresponding source or a redistribution review. Do not silently substitute
modern toolchain sources or a guessed upstream tarball and call it verified.
Obtain the original library source, versions and build/patch information, retain
the required notices, and update the source supplement with evidence. The source
URL supplied by the user has been checked; this outstanding question concerns
the upstream's prebuilt libraries, not an unknown fork source URL.

The original installer is byte-identical to the compared upstream prebuilt FIR.
It has not been independently rebuilt. Its Makefile references CCF11102.FIR;
that Canon file is not shipped as an update by this fork. This limitation stays
in release notes, rather than claiming a fresh-install hardware test.

This is a technical distribution audit, not legal advice or a certification.
Unresolved evidence is reported as unresolved; no blanket license is assigned
to all inherited files based only on their names.
