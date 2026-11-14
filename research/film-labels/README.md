# Stock-specific label artwork data

HNGSeries/M-Film 0.2.1, commit 8118e9c7c072371bd53eda8920f44910e8a35baf, supplies the GPL-2.0-only label cues for all 72 preset identities. `CATALOG.json` records the original ramp/level colors, pattern, wording and source hashes. Runtime mapping to the existing Magic Lantern palette is approximate; the renderer changes foreground to black where a bright yellow band would hide white lettering.

`python tools/import_film_labels.py /path/to/pinned-upstream` safely parses the catalog's limited data expressions without executing upstream Python. Eight explicit labels are transcribed from fos_film.c. The generated compact header is indexed exactly like the immutable recipe catalog. Original ISO/WB/Picture Style recipes are not modified. The typed side names, compact glyphs, geometry and drawing code are independent work for this fork. No manufacturer photographs, upstream textures or third-party logo artwork are bundled. Brand words identify source presets.

Preserve the upstream GPL text in ../jpeg-tones/M-FILM-GPL-2.0.txt. Label data introduces GPL-2.0-only derived material; credit M-Film contributors.

External Google Images search was blocked at CONNECT with HTTP403, so this does not claim photographic verification of all actual retail wrappers. Some stock names refer to discontinued films, cross-process recipes or cinema print materials rather than purchasable 35mm cartridges. Those illustrations are documented as interpretations.

See [Thai gallery and prepared search links](GALLERY_TH.md) and `python tests/check_film_labels.py` for 72 independent label-only screen captures/side-name mapping checks. Host colors approximate the camera palette; hardware appearance and redraw speed need actual 600D testing.
