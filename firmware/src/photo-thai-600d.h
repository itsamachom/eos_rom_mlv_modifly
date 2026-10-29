/* Photo UI phrase rendering: GPL-2.0-or-later. Noto-derived mask data is OFL.
 * Include within menu.c after normal bitmap/font declarations.
 */
#include "photo-thai-data.h"

static unsigned char * photo_thai_atlas;
static int photo_thai_attempted;

static int photo_thai_prepare(void)
{
    if (!photo_thai_enabled) return 0;
    if (photo_thai_attempted) return photo_thai_atlas != NULL;
    photo_thai_attempted = 1;
    uint32_t size = 0;
    if (FIO_GetFileSize("ML/data/PHOTO_TH.BIN", &size) || size != PHOTO_TH_BYTES || size > 512 * 1024)
        return 0;
    unsigned char * data = fio_malloc(size);
    if (!data) return 0;
    FILE * file = FIO_OpenFile("ML/data/PHOTO_TH.BIN", O_RDONLY | O_SYNC);
    if (!file) { fio_free(data); return 0; }
    int read = FIO_ReadFile(file, data, size);
    FIO_CloseFile(file);
    unsigned crc = ~0u;
    if (read == (int)size)
    {
        for (unsigned i = 0; i < size; i++)
        {
            crc ^= data[i];
            for (int bit = 0; bit < 8; bit++)
                crc = (crc >> 1) ^ ((crc & 1) ? 0xedb88320u : 0);
        }
    }
    if (read != (int)size || ~crc != PHOTO_TH_CRC)
    {
        fio_free(data);
        return 0; /* Missing/mismatched/corrupt resources retain English. */
    }
    photo_thai_atlas = data;
    return 1;
}

static int photo_thai_active(void)
{
    return photo_thai_enabled && photo_thai_atlas != NULL;
}

static const struct photo_thai_mask * photo_thai_find(int font, const char * key)
{
    int id = FONT_ID(font);
    int style = id == 2 ? 0 : id == 3 ? 1 : id == 4 ? 2 : -1;
    if (style < 0 || !key) return NULL;
    for (unsigned i = 0; i < COUNT(photo_thai_phrases); i++)
        if (streq(key, photo_thai_phrases[i].key)) return &photo_thai_phrases[i].masks[style];
    return NULL;
}

static int photo_thai_blit(int font, int x, int y, int width, const struct photo_thai_mask * mask)
{
    if (!mask || mask->width > width || mask->offset > PHOTO_TH_BYTES ||
        mask->encoded_size > PHOTO_TH_BYTES - mask->offset) return 0;
    unsigned stride = (mask->width + 7) / 8;
    unsigned bytes = stride * mask->height;
    unsigned end = mask->offset + mask->encoded_size;
    unsigned pos = mask->offset;
    unsigned out = 0;
    uint8_t * vram = bmp_vram();
    while (pos < end && out < bytes)
    {
        unsigned tag = photo_thai_atlas[pos++];
        unsigned run = (tag & 127) + 1;
        if (run > bytes - out || (!(tag & 128) && run > end - pos)) return 0;
        if (tag & 128) { out += run; continue; }
        for (unsigned n = 0; n < run; n++, out++)
        {
            unsigned bits = photo_thai_atlas[pos++];
            if (!bits) continue;
            int px = x + (int)((out % stride) * 8);
            int py = y + (int)(out / stride);
            if (py < 0 || py >= 480) continue;
            for (unsigned bit = 0; bit < 8; bit++)
                if ((bits & (128 >> bit)) && (out % stride) * 8 + bit < mask->width &&
                    px + (int)bit >= 0 && px + (int)bit < 720)
                    bmp_putpixel_fast(vram, px + bit, py, FONT_FG(font));
        }
    }
    return out == bytes && pos == end;
}

static int photo_thai_text(int font, int x, int y, int width, const char * text)
{
    if (!photo_thai_active() || !text) return 0;
    char key[MENU_MAX_HELP_LEN];
    snprintf(key, sizeof(key), "%s", text);
    char * newline = strchr(key, '\n');
    if (newline) *newline = 0;
    int len = strlen(key);
    while (len && key[len - 1] == ' ') key[--len] = 0;
    const struct photo_thai_mask * mask = photo_thai_find(font, key);
    if (mask) return photo_thai_blit(font, x, y, width, mask);

    /* Keep measured numbers/symbols unchanged when translating compound ON/OFF values. */
    int prefix = strncmp(key, "ON,", 3) == 0 ? 2 : strncmp(key, "OFF,", 4) == 0 ? 3 : 0;
    if (prefix)
    {
        char state[4];
        memcpy(state, key, prefix); state[prefix] = 0;
        mask = photo_thai_find(font, state);
        int tail_width = bmp_string_width(font, key + prefix);
        if (mask && mask->width + tail_width <= width && photo_thai_blit(font, x, y, width, mask))
        {
            bmp_printf(font, x + mask->width, y + 4, "%s", key + prefix);
            return 1;
        }
    }
    /* No guessed translations: retain original strings when not in the lexicon. */
    return 0;
}
