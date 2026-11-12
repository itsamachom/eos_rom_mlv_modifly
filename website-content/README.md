# Camera-photo source record

The owner supplied six camera-screen photographs in `Picture.zip` and authorized
publishing them on the project website. `menu-photos.json` maps source filenames
to the public assets, captions and hashes. The originals are kept outside the
repository, because their metadata includes location and device information.
No private metadata values are recorded here.

Both homepages use a real shooting-menu photograph as the hero image. A gallery
presents shooting, focus and setup as three Thai/English pairs, with captions in the page's language. The photos stay on the page and do not
open larger copies when clicked. JPEG metadata was removed without
re-encoding: all six public images were verified to have identical decoded
pixels and dimensions, and no remaining EXIF metadata. No photograph was
reconstructed, recolored or cropped.

The pictured build version is unspecified. Preserve that distinction and the
existing v3r2 release/testing status. Photographs establish the visible menu
rendering, not complete functional or first-install testing. Credit the project
creator, Online2easy; see the asset README for the photo-use statement.

Display frames are at most 520px wide (approximately 330px high), with responsive scaling on smaller screens. This changes presentation only; source JPEG pixels remain intact.

## Video catalog

Add future lessons in videos.json and run tools/render_video_pages.py. The supplied installation video is Ii1Uv8L9Nf8; the supplied playlist is PLUY4HsSfA1IU. Video/playlist live availability could not be checked from the cloud proxy, so no title, duration, recording date or tested firmware version was inferred from YouTube. version_in_video is null until confirmed. Keep the playlist URL exactly as supplied unless the owner provides a replacement.

## Thai user manual

`manual-th.json` contains one Thai explanation per unique Photo UI item (43 unique keys; Modules appears in two categories, so there are 44 entries on screen). Each includes a purpose, usage, exact English control keys and Thai explanations. `tools/render_manual_th.py` takes displayed labels from the current translation dictionary and orders entries from the actual front-end arrays. Do not edit the generated HTML/Markdown/PDF as the source of truth. Verify source behavior as well as labels, especially controls whose short Thai label differs from the upstream English variable.
