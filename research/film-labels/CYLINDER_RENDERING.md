# Cylinder rendering: source review and adaptation

Reviewed M-Film 0.2.1, commit `8118e9c7c072371bd53eda8920f44910e8a35baf`, [`ml-dev/filmos/fos_film.c`](https://github.com/HNGSeries/mfilm-canon-film-simulation/blob/8118e9c7c072371bd53eda8920f44910e8a35baf/ml-dev/filmos/fos_film.c).

The realistic appearance comes from geometry/lighting, not merely a flat product photograph:

- `build_profiles` computes `asin(x/r)` surface angle, diffuse softbox lighting, narrow specular lobes, separate steel and black-plastic profiles.
- A circumferential label texture is sampled column by column; the lettering compresses towards the silhouette. Top/bottom edges follow the viewing tilt.
- `can_col`, `draw_body` and related column runs combine label light, material reflection, antialiased silhouette coverage and dithering to palette ramps. `draw_leader` curves and tapers the perforated film tongue.

Our tone5 adaptation keeps the accepted 72 label identities/base palette colors. It builds a bounded 144×134 label plane with the shipped RBF fonts, reuses a single 19,296-byte heap buffer and wraps that plane with an independently generated 92-column angle/curvature/softbox profile. Float math runs offline in `tools/generate_film_cylinder.py`; the camera uses integer lookup tables. Caps/spool have separate steel/plastic highlights. A 4×4 ordered dither approximates colored shading using existing Magic Lantern colors; grayscale reflections use the built-in gray ramp.

This is an independent, smaller adaptation of the technique, not the entire upstream renderer or its custom palette system. Existing palette entries are not changed, and no upstream texture/font pack/RAW/LUT processing is loaded. Credit M-Film contributors for the label data and renderer approach. The pre-existing GPL-2.0-only label-data terms remain; independent renderer code is GPL-2.0-or-later. Preserve upstream GPL text in `../jpeg-tones/M-FILM-GPL-2.0.txt`.

The label plane is painted in the normal menu draw buffer; the existing menu double-buffering/presentation path is retained. Allocation is attempted once, with the tone4 flat renderer retained if memory is unavailable. The reusable buffer is intentionally kept for the session, not allocated per stock or redraw. It does not perform SD reads or photo processing. Hardware redraw speed/appearance remain to be measured on a 600D.

The lower-right framed panel distinguishes the active, read-back-verified tone from browsing. Merely browsing does not change the active name or camera settings. External Canon changes remove active marking. The selected name is previewed if no verified active recipe exists.
