# Native JPEG recipes: source scope

Upstream: HNGSeries/M-Film 0.2.1, commit `8118e9c7c072371bd53eda8920f44910e8a35baf`.

- Eight explicit native preview recipes are in `ml-dev/filmos/fos_film.c`.
- `ml-dev/filmos/tools/genfilms.py` supplies native preview settings by kind for the other 64 profiles (63 Film-Luts entries plus cinestill400t).
- Ignoring ISO and deduplicating the actual Picture Style, contrast, sharpness, saturation, tone, Kelvin, GM and BA tuples leaves **13 distinct native recipes**.
- The 72 developed looks rely on separate RAW/LUT processing. Their names are not evidence of 72 distinct direct-JPEG looks.
- `UPSTREAM_NATIVE_RECIPES.json` records all 72 input mappings, source hashes and the audited commit. The derived table has new names and grouping in `firmware/src/photo-tone-recipes-600d.h`.
- Native preview recipes are GPL-2.0-only; preserve the verbatim upstream GPL text and attribution. No `.cube`, film LUT, RAW decoder, Darkrooms code, sample photo or film-canister graphics were copied into this feature.

The independent picker uses its own rectangle/shading/film-leader renderer. Host screenshots show its production code and shipped font masks with simulated camera properties, not real JPEG appearance or measured camera timings.
