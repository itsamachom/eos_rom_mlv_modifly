/* Native JPEG recipes derived from HNGSeries/M-Film 0.2.1, commit
 * 8118e9c7c072371bd53eda8920f44910e8a35baf, fos_film.c and genfilms.py.
 * Copyright M-Film contributors; adaptation, grouping and UI by this fork.
 * GPL-2.0-only for this derived recipe table; preserve upstream LICENSE.
 * These are native Picture Style/WB approximations, NOT the 72 developed LUT looks.
 * Deliberately no ISO, exposure, file-quality or shutter controls. */
#ifndef PHOTO_TONE_RECIPES_600D_H
#define PHOTO_TONE_RECIPES_600D_H
struct photo_tone_recipe {
    const char *name;
    int group, style, contrast, sharpness, saturation, color_tone, kelvin, gm, ba;
};
static const char *const photo_tone_groups[] = {"Warm Tones","Vivid Tones","Cinema Tones","Mono Tones"};
static const struct photo_tone_recipe photo_tone_recipes[] = {
    {"Soft Skin",      0,0x81,-1,2,-1, 1,5500,0,1},
    {"Golden Warm",    0,0x81, 1,2, 1, 2,5600,0,2},
    {"Fresh Green",    0,0x81, 1,2, 1, 0,5200,1,0},
    {"Natural Color",  0,0x81, 0,2, 0, 0,5200,0,0},
    {"Vivid Color",    1,0x83, 1,3, 2, 0,5200,0,0},
    {"Slide Vivid",    1,0x83, 3,3, 4, 0,5200,0,0},
    {"Slide Rich",     1,0x83, 2,2, 2, 0,5200,0,0},
    {"Cross Color",    1,0x83, 3,2, 3, 0,5200,0,0},
    {"Night Cool",     2,0x81, 1,2, 1,-1,3200,0,0},
    {"Cinema Cool",    2,0x81, 1,2, 1,-1,5200,0,0},
    {"Cinema Muted",   2,0x81, 1,2,-1, 0,5200,0,0},
    {"Mono Soft",      3,0x86, 1,2, 0, 0,5200,0,0},
    {"Mono Contrast",  3,0x86, 3,2, 0, 0,5200,0,0},
};
#define PHOTO_TONE_COUNT ((int)(sizeof(photo_tone_recipes)/sizeof(photo_tone_recipes[0])))
#endif
