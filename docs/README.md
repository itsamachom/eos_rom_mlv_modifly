# Website draft / ร่างเว็บไซต์ไทย–อังกฤษ

Branch: site/eos-600d-bilingual. Static HTML/CSS for GitHub Pages; no build dependencies, JavaScript, third-party embeds, tracking or payment forms. New website code is GPL-2.0-or-later; retain upstream notices in the firmware repository. Fonts use local system fallbacks, not remote font downloads. The menu illustration is original HTML/CSS and is labeled as an illustration, not a hardware screenshot.

- Thai: index.html
- English: en/index.html
- Shared styles: assets/site.css

This branch is a reviewable draft. Pushing it does not activate Pages or publish a firmware release. The owner has chosen not to accept money yet; do not add payment links, account details or QR codes without an explicit later request.

## Repository choice

Same repository: simplest start, one place for source/docs/site, project URL includes eos_rom_mlv_modifly. Site commits share the firmware history and repository permissions.

Separate website repository: cleaner website-specific name/history/access, easier to change independently. Requires managing a second repository and updating source/document links. These files can be moved unchanged; the language switch and stylesheet paths are relative.

## Activate only after choosing where to host

If retaining this repository, GitHub → repository Settings → Pages → Build and deployment → Deploy from a branch → branch site/eos-600d-bilingual → folder /docs → Save. Labels may vary with GitHub UI. No workflow, release upload token or Codex network-setting change is required for this branch-based Pages route. This will publish the website publicly; choose it only after reviewing the site. Firmware release/source verification is a separate process.

The expected project-site address, if Pages is activated here, is:
https://itsamachom.github.io/eos_rom_mlv_modifly/

This address is not claimed to be live by this draft. Use the deployment status/link shown in GitHub Pages as the authority.

## Local review

Serve the repository root and open /docs/ (Thai) or /docs/en/ (English). Check both languages, keyboard navigation, mobile widths and the FAQ disclosures. Both pages work without JavaScript. Do not open an HTML file's GitHub source viewer and mistake it for a live site.

## Updating status

Before changing hardware-test claims, record exact camera/firmware/package checksum, tested behavior, date and observed failures. Keep first-install testing distinct from updating an already ML-enabled camera. Do not replace experimental wording with stable merely because host checks pass.

If financial contributions open later, name the recipient and purpose, use an appropriate external provider, disclose fees/affiliate links and preserve GPL rights. Update both languages and the privacy explanation when adding any external embeds or services.
