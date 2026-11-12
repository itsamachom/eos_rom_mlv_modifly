# Thai-Menu v3r5: source-based menu captures

Generated with `python3 tools/render_menu_catalog.py`.

- 188 PNGs: all 44 bound Photo UI items in Thai and English, plus all available source-defined immediate detail pages.
- Open `index.html` after extracting the ZIP. No server or internet required.
- Every PNG has a disclosure strip outside the unchanged 720×480 framebuffer.
- Production renderer and Thai blitter: `firmware/src/photo-menu-600d.h`, `photo-thai-600d.h`; committed PHOTO_TH.BIN and argnor RBF glyphs.
- Menu registry extracted from the real source with the 600D internals/features preprocessor configuration.
- Source commit: `e0ca30918cb571dbd8ab1fad8466319c9c6984a0`.

## ข้อจำกัด / Limitations

- Not a Canon hardware or QEMU screenshot.
- Palette is an illustrative host palette; actual camera colors may differ.
- Camera-dependent callbacks and all editable values are replaced by Unavailable, not inferred.
- Only real read-only project/build/camera-info callbacks run; model/Canon firmware are target fixtures, not camera readings.
- Modules and game scripts are not registered: their unavailable state is intentional, not evidence of a missing feature.
- Static 600D-enabled names/help/children are extracted with GCC preprocessing. Runtime row hiding/renaming/warnings are not emulated.
- Classic/native editors opened with Q/SET, module lists, and game screens are not captured.

ค่าจำนวนชัตเตอร์แสดงว่ายังใช้งานไม่ได้ ไม่ใส่จำนวนชัตเตอร์สมมุติ ภาพเป็นข้อมูลอ้างอิงโค้ด ไม่ใช่หลักฐานการทดสอบบนกล้องจริง

ภาพเมนูเกม/โมดูลที่ยังไม่ลงทะเบียนตรงกับสถานะยังไม่โหลด โดยไม่ได้รันเกมหรือ firmware updater

Developer: https://itsamachom.github.io/eos_rom_mlv_modifly/

Code and captures retain the firmware's GPL notices. Noto-derived Thai masks retain their OFL notices; see `assets/fonts/noto-sans-thai/OFL.txt` in the repository.
