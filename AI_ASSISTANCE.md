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
