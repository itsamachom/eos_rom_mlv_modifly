# Project website / เว็บไซต์ไทย–อังกฤษ

Branch: site/eos-600d-bilingual. Static HTML/CSS for GitHub Pages; no build dependencies, JavaScript, third-party embeds, tracking or payment forms. New website code is GPL-2.0-or-later; retain upstream notices in the firmware repository. Fonts use local system fallbacks, not remote font downloads. The hero and gallery use six real camera-menu photographs supplied by the project creator. EXIF/GPS metadata was removed without changing their decoded pixels or dimensions. The pictured build version is unspecified, and the captions do not claim full functional testing.

- Thai: index.html
- English: en/index.html
- Shared styles: assets/site.css
- Thai articles: articles/inspiration.html and articles/before-a-release.html
- English articles: en/articles/ with matching filenames
- Editorial tone: [CONTENT_STYLE.md](CONTENT_STYLE.md)

The owner reported activating GitHub Pages on 5 November 2026. Deployment has not been independently verified from this workspace because API access was blocked. With Pages configured to serve this branch, subsequent pushes update the website after a successful deployment. Website updates do not publish a firmware release. The owner has chosen not to accept money yet; do not add payment links, account details or QR codes without an explicit later request.

## Repository choice

Same repository: simplest start, one place for source/docs/site, project URL includes eos_rom_mlv_modifly. Site commits share the firmware history and repository permissions.

Separate website repository: cleaner website-specific name/history/access, easier to change independently. Requires managing a second repository and updating source/document links. These files can be moved unchanged; the language switch and stylesheet paths are relative.

## Publish on GitHub Pages

The owner authorized public website publication on 5 November 2026. The site is prepared in this repository. Open [GitHub Pages settings](https://github.com/itsamachom/eos_rom_mlv_modifly/settings/pages), then choose Build and deployment → Source: Deploy from a branch → Branch: `site/eos-600d-bilingual` → Folder: `/docs` → Save. Labels may vary with the GitHub UI. The `.nojekyll` file serves the existing HTML/CSS directly. No Actions workflow or token needs to be added. Website publication is separate from publishing the firmware release.

The workspace attempt to read/configure Pages through `api.github.com` returned `Forbidden` from the network. Pages settings and remote deployment status could not be verified. Website files have been pushed; this does not establish that Pages is active. The owner subsequently reported that the browser setup succeeded. That is an owner-reported status, not an automated deployment check.

The expected project-site address, if Pages is activated here, is:
https://itsamachom.github.io/eos_rom_mlv_modifly/

This is the expected URL for the configuration the owner reported enabling. Use the deployment status/link shown in GitHub Pages as the authority.

## Local review

Serve the repository root and open /docs/ (Thai) or /docs/en/ (English). Check both languages, keyboard navigation, mobile widths and the FAQ disclosures. Both pages work without JavaScript. Do not open an HTML file's GitHub source viewer and mistake it for a live site.

## Updating status

Before changing hardware-test claims, record exact camera/firmware/package checksum, tested behavior, date and observed failures. Keep first-install testing distinct from updating an already ML-enabled camera. Do not replace experimental wording with stable merely because host checks pass.

If financial contributions open later, name the recipient and purpose, use an appropriate external provider, disclose fees/affiliate links and preserve GPL rights. Update both languages and the privacy explanation when adding any external embeds or services.

## Editing website content

For a Thai beginner's guide to editing text through GitHub, see [EDITING_TH.md](EDITING_TH.md). The inspiration story is marked `CONTENT: story` in both language files. Ordinary text changes do not require a firmware build or release. If Pages is later activated from this branch, committed site changes become visible after a successful Pages deployment; the owner has now reported that hosting is configured.

Articles use `CONTENT: article-body`; homepage article cards use `CONTENT: journal`.
Language switches on an article open its translation, rather than the homepage.
The latest source-review links point to the pinned audit record at `31b1022`;
this does not change the firmware source or incorporate the audit branch here.

## Creator channels and photo assets

The homepage creator section links to the exact YouTube, Facebook and Blogger addresses supplied by the owner. These are plain links, without social embeds or tracking scripts. Article footers link back to the creator section.

The six camera-menu photos were received in `Picture.zip` and integrated into both homepages. Their source-to-asset mapping, privacy processing checks and hashes are recorded in `website-content/menu-photos.json` outside the published tree. The gallery groups shooting, focus and setup images in Thai/English pairs with non-clickable photos constrained to 520px wide (about 330px high) and scaled down on smaller screens. Actual remote deployment is confirmed only by GitHub Pages; a push alone is not an independent live-site check.

Photo display widths are constrained by both CSS and inline HTML fallbacks so a stale stylesheet cannot make them fill the page at their native dimensions. All six pages reference a content-versioned stylesheet URL. After changing CSS, refresh its `?v=` value in every HTML page to prevent mixed cached styles. The original JPEG pixels and metadata-removal checks remain unchanged.

## First installation, update and source downloads

The Thai download page is download.html; English is en/download.html. DOWNLOAD.md is the GitHub guide. There are three separate downloads: FIRST-INSTALL includes the original verified ML-SETUP.FIR plus the current runtime, UPDATE has the same runtime without FIR, and matching source is separate. First-install instructions follow firmware/doc/INSTALL.txt and the original installer countdown behavior; hardware first-install testing is still unverified.

Current release preparation: update scripts/photo-ui-version.txt; add current notes/guides; build/test; stage source; run package_photo_ui_current.py, package_camera_download.py and render_download_pages.py; update homepage current-version/status; commit/tag/publish atomically. Source URLs reference the immutable release tag. Do not overwrite prior tags or published ZIPs. Obsolete distribution files are removed only from the current branch; keep Git history and required provenance/license evidence.

Developer profile links are present in every HTML footer and the GitHub download guide. Keep the three owner-provided URLs unchanged. Run node tools/check_download_pages.cjs, node tools/check_website.cjs and node tools/check_video_pages.cjs from a temporary copy containing docs, tools, scripts, downloads, previews and website-content. Download tests use actual package bytes as browser fixtures; verify public GitHub transport after publishing. A Git push does not prove Pages deployed.

Creator profile links use target="_blank" with rel="noopener noreferrer" across all pages. Keep these attributes in the download-page renderer as well. For guide-only corrections use tools/revise_download_docs.py: it produces new -docN ZIPs, preserves firmware/FIR bytes and prior downloads, then refresh pages with render_download_pages.py. Do not overwrite the published firmware tag for editorial changes.

## Video guides

Thai: videos.html. English: en/videos.html. The homepage has a featured lesson, and downloads links to the installation lesson before the written first-install steps. Video and playlist links open YouTube in a new tab, without an iframe, remote thumbnail, script, or initial third-party request. The poster is an original illustrated lesson cover, not a frame captured from the video. No donation/Sponsors button was added.

Catalog: website-content/videos.json. To add a video, append an entry with a unique id, 11-character youtube_id, localized title/summary, category, added_at, version_in_video (null if unknown) and a local poster. Keep the actual version shown separate from the latest release; a tutorial does not prove hardware testing for that release. Set featured to choose the installation lesson. Run python3 tools/render_download_pages.py then python3 tools/render_video_pages.py, and refresh the shared CSS token after style changes. Add videos to the YouTube playlist itself to keep the external playlist current; the website catalog is edited explicitly and does not auto-sync.

## Source-based menu captures

`menu-previews/v3r5/index.html` is a separate reference gallery, generated by `python3 tools/render_menu_catalog.py`. It runs the production Photo UI renderer with the shipped Thai atlas/RBF glyphs, a static registry extracted using the real 600D feature flags, and explicit unavailable values for camera-dependent callbacks. It covers 44 front-end items and immediate detail pages in both languages. This is not a camera/QEMU capture or evidence of hardware testing. Every PNG carries a disclosure outside the framebuffer; colors are an illustrative host palette. Classic editors, runtime-dependent hiding/warnings, loaded module internals and game screens are outside the capture scope. The gallery, manifest, licenses and PNGs are also bundled into a ZIP for offline inspection. Run `node tools/check_menu_catalog.cjs` after regenerating the gallery. No firmware or published installation package is rebuilt.

## Thai user manual

The reviewed explanations live in `website-content/manual-th.json`. Run `python3 tools/render_manual_th.py` to produce `docs/manual-th.html` and `MANUAL_TH.md`, then `python3 tools/check_manual_th.py` to audit all 44 front-end entries and 116 immediate controls against the 600D-enabled source, including optional Dual ISO/ETTR declarations. Run `node tools/build_manual_pdf.cjs` to check responsive layout/navigation and export the searchable, font-embedded A4 PDF under `docs/manual/`. The local Noto font and original OFL/source notices live in `docs/assets/manual/`. The manual clearly distinguishes Tv/Ae behavior from the existing TV/AV label, Canon firmware from Thai-Menu version, and Live View actuations from image-file counts. For a future firmware release, review the explanations/source revision and bump the manual release before regenerating. Native menus are documented as gateways, not a claim to cover every dynamic Classic menu.
