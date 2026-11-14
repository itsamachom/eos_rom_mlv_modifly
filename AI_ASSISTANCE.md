# AI / LLM assistance disclosure

This fork uses OpenAI Codex/LLM assistance. This includes substantial generated
or guided code; it is not being represented as solely human-written code.

Affected work includes:

- The 600D Photo UI implementation and later state/identity locking changes in
  firmware/src/photo-menu-600d.h and its integration in firmware/src/menu.c.
- Thai phrase rendering, translation data and font-generation tools/assets.
- Camera property availability handling, camera/shutter detail presentation,
  menu selection, Games registration correction and package module selection.
- Host tests, build/packaging/release helpers, documentation and translations.
- v3r3 cross-category item navigation, simplified Setup menu and build-derived version display.
- v3r4 Canon-compatible version formatting, FIRMWARE ADD-ON Thai-Menu identity, regression guards and bilingual public-package information.

The imported Magic Lantern source, original game scripts, original installer,
Noto font and inherited library archives are not claimed as original fork or
AI-authored work. Preserve their authorship and notices. Consult Git history,
release/v3r2/MODIFIED_FILES.json and THIRD_PARTY_NOTICES.md for boundaries.

Upstream firmware/LLM_POLICY.md requires disclosure and says that substantial
LLM-generated code will not be accepted as upstream contributions. Publishing
this independent fork does not claim upstream acceptance or waive that policy.
Do not submit these changes upstream as human-written work or describe this
fork's binary as an official Magic Lantern build. Any future upstream proposal
must follow the upstream policy and its maintainers' decisions.

AI assistance does not establish correctness, rights clearance, hardware safety
or completeness of corresponding source. See release readiness records.

- v3r5 Live View wording, separate first-install/update packaging, installation documentation, download navigation cleanup and developer links.

The v3r6-tone1 experiment uses Codex/LLM assistance for recipe provenance/deduplication, independent canister UI, Canon Picture Style/WB adapter, transaction/rollback engine, Thai strings, tests, preview captures and documentation. M-Film is credited for the source native preview recipes. Hardware JPEG appearance and latency remain unverified.

The v3r6-tone2 experiment also uses Codex/LLM assistance for original preset/ISO catalog extraction, read-readiness fixes, ISO backup/restore, cylindrical canister artwork, regression tests and experimental packaging. Original numerical recipes/ISO conversion and film identities remain credited to M-Film. v3r5 main release and website/manual scope remain unchanged.

The v3r6-tone3 update uses Codex/LLM assistance for requested display names, tab sizing, build verification and documentation. Three fictional THAI-MENU packaging concepts in design/film-concepts/v3r6-tone3 were made with OpenAI image generation. They are standalone design proposals, not runtime assets, and are not included in firmware source ZIPs. Native preset values are unchanged.
