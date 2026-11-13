# Native JPEG recipes: source scope

Upstream: HNGSeries/M-Film 0.2.1, commit `8118e9c7c072371bd53eda8920f44910e8a35baf`.

- Eight explicit native preview recipes are in `ml-dev/filmos/fos_film.c`.
- `ml-dev/filmos/tools/genfilms.py` supplies native preview settings by kind for the other 64 profiles (63 Film-Luts entries plus cinestill400t).
- Ignoring ISO and deduplicating the actual Picture Style, contrast, sharpness, saturation, tone, Kelvin, GM and BA tuples leaves **13 distinct native recipes**.
- The 72 developed looks rely on separate RAW/LUT processing. Their names are not evidence of 72 distinct direct-JPEG looks.
- `UPSTREAM_NATIVE_RECIPES.json` records all 72 input mappings, source hashes and the audited commit. The tone1 derived table used new names; that historical analysis excludes ISO. The current tone2 table preserves all original names and values in `firmware/src/photo-tone-recipes-600d.h`.
- Native preview recipes are GPL-2.0-only; preserve the verbatim upstream GPL text and attribution. No `.cube`, film LUT, RAW decoder, Darkrooms code, sample photo or film-canister graphics were copied into this feature.

The independent picker uses its own rectangle/shading/film-leader renderer. Host screenshots show its production code and shipped font masks with simulated camera properties, not real JPEG appearance or measured camera timings.

## tone2: original catalog including ISO

`UPSTREAM_ORIGINAL_CATALOG.json` records all 72 original names, brands, box ISO, camera ISO, native style/WB settings and source hashes. The eight built-ins retain their exact values; all other entries use the original `genfilms.py` defaults by kind. Nothing is deduplicated. The source `filmroll.c` whole-stop `iso_to_raw` behavior is preserved: declared ISO125/160 requests raw80 (ISO200); low box-speed films use camera ISO100. The actual effective camera ISO is shown separately from the box label.

To audit/regenerate against the pinned upstream checkout: `python tools/import_original_jpeg_tones.py /path/to/upstream`. It parses source data without executing upstream code, verifies the commit, and emits the catalog/header. `python tests/check_original_jpeg_recipes.py` checks the shipped header against the audit. Group positions map upstream Colour/Slide/B&W/Cine to this picker's Colour/Slide/Cine/Mono order; recipe values stay unchanged. Monochrome preserves the owner's filter/toning, as the original `apply_film` does.

Including ISO/WB does not turn native previews into the full developed looks. No LUT, grain, halation or RAW-development stage is included. v3r5 remains the public main release and website/manual target; tone2 is an isolated experiment.
