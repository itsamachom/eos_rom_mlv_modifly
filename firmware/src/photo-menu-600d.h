/* Canon 600D Photo menu front end, GPL-2.0-or-later.
 * Included by menu.c: reuse its locking, values and editing paths.
 * No camera addresses or exposure/recording algorithms are changed here.
 */
#ifdef CONFIG_600D

#define PHOTO_ROWS 7
struct photo_item {
    const char * label;
    const char * menu;
    const char * entry; /* NULL opens the original system menu */
};
struct photo_page {
    const char * name;
    const char * badge;
    const struct photo_item * items;
    int count;
};

static const struct photo_item photo_shoot[] = {
    {"Intervalometer", "Shoot", "Intervalometer"},
    {"Bulb Timer", "Shoot", "Bulb Timer"},
    {"Advanced Bracket", "Shoot", "Advanced Bracket"},
    {"Silent Picture", "Shoot", "Silent Picture"},
    {"Mirror Lockup", "Shoot", "Mirror Lockup"},
    {"Flash Tweaks", "Shoot", "Flash Tweaks"},
    {"Shoot Preferences", "Shoot", "Shoot Preferences"},
};
static const struct photo_item photo_focus[] = {
    {"Trap Focus", "Focus", "Trap Focus"},
    {"Focus Stacking", "Focus", "Focus Stacking"},
    {"Rack Focus", "Focus", "Rack Focus"},
    {"Follow Focus", "Focus", "Follow Focus"},
    {"Focus End Point", "Focus", "Focus End Point"},
    {"Focus Settings", "Focus", "Focus Settings"},
    {"DOF Settings", "Focus", "DOF Settings"},
};
static const struct photo_item photo_expo[] = {
    {"White Balance", "Expo", "White Balance"},
    {"ISO", "Expo", "ISO"},
    {"Shutter", "Expo", "Shutter"},
    {"Aperture", "Expo", "Aperture"},
    {"Picture Style", "Expo", "Picture Style"},
    {"Dual ISO", "Expo", "Dual ISO"},
    {"Auto ETTR", "Expo", "Auto ETTR"},
};
static const struct photo_item photo_overlay[] = {
    {"Zebras", "Overlay", "Zebras"},
    {"Focus Peak", "Overlay", "Focus Peak"},
    {"Magic Zoom", "Overlay", "Magic Zoom"},
    {"Histogram", "Overlay", "Histogram"},
    {"Spotmeter", "Overlay", "Spotmeter"},
    {"Cropmarks", "Overlay", "Cropmarks"},
    {"Waveform", "Overlay", "Waveform"},
    {"Global Draw", "Overlay", "Global Draw"},
};
static const struct photo_item photo_movie[] = {
    {"Time Indicator", "Movie Tweaks", "Time Indicator"},
    {"REC key", "Movie", "REC key"},
    {"Movie Tweaks", "Movie", "Movie Tweaks"},
};
static const struct photo_item photo_setup[] = {
    {"Modules", "Modules", NULL},
    {"Preferences", "Prefs", NULL},
    {"Display", "Display", NULL},
    {"Version / Help", "Help", NULL},
    {"Diagnostics", "Debug", NULL},
};
#define PHOTO_PAGE(name, badge, items) {name, badge, items, COUNT(items)}
static const struct photo_page photo_pages[] = {
    PHOTO_PAGE("Shoot", "S", photo_shoot),
    PHOTO_PAGE("Focus", "F", photo_focus),
    PHOTO_PAGE("Expo", "E", photo_expo),
    PHOTO_PAGE("Overlay", "O", photo_overlay),
    PHOTO_PAGE("Movie", "V", photo_movie),
    PHOTO_PAGE("Setup", "+", photo_setup),
};

static int photo_page_index;
static int photo_selection[COUNT(photo_pages)];
static int photo_classic;

static int photo_home_active(void)
{
    return !photo_classic && !SUBMENU_OR_EDIT &&
        !menu_lv_transparent_mode && !menu_help_active;
}

/* The caller holds menu_sem. Resolve afresh: modules can add/remove entries. */
static struct menu_entry * photo_resolve(const struct photo_item * item, struct menu ** parent)
{
    *parent = NULL;
    for (struct menu * m = menus; m; m = m->next)
    {
        if (!streq(m->name, item->menu)) continue;
        *parent = m;
        if (!item->entry) return NULL;
        for (struct menu_entry * e = m->children; e; e = e->next)
            if (streq(e->name, item->entry) && !e->shidden && !e->placeholder)
                return e;
        return NULL;
    }
    return NULL;
}

static int photo_select_original(struct menu * parent, struct menu_entry * entry)
{
    int depth = 0;
    struct menu * root = parent;
    while (root)
    {
        if (entry)
            for (struct menu_entry * e = root->children; e; e = e->next)
                e->selected = (e == entry);
        if (!IS_SUBMENU(root)) break;
        entry = root->parent_entry;
        root = root->parent_menu;
        depth++;
    }
    for (struct menu * m = menus; m; m = m->next)
        if (!IS_SUBMENU(m)) m->selected = (m == root);
    return depth;
}

/* Clip by actual font width, not character count, to keep the two panes apart. */
static void photo_text(int font, int x, int y, int width, const char * text)
{
    char buf[MENU_MAX_HELP_LEN];
    snprintf(buf, sizeof(buf), "%s", text ? text : "");
    char * newline = strchr(buf, '\n');
    if (newline) *newline = 0;
    int len = strlen(buf);
    if (bmp_string_width(font, buf) > width)
    {
        while (len && bmp_string_width(font, buf) > width - bmp_string_width(font, "..."))
            buf[--len] = 0;
        if (len + 3 < (int)sizeof(buf)) snprintf(buf + len, sizeof(buf) - len, "...");
    }
    bmp_printf(font, x, y, "%s", buf);
}

static void photo_read_info(struct menu_entry * entry, struct menu_display_info * info)
{
    entry_default_display_info(entry, info);
    info->x = 380;
    info->y = 124;
    info->x_val = 560;
    info->can_custom_draw = 0;
    if (entry->update) entry->update(entry, info);
}

static void photo_detail_row(int row, const char * name, const char * value)
{
    int y = 122 + row * 39;
    draw_line(376, y + 33, 704, y + 33, COLOR_GRAY(15));
    photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 381, y, 183, name);
    photo_text(FONT(FONT_MED, COLOR_CYAN, COLOR_GRAY(5)), 568, y, 133, value);
}

static int photo_menu_draw(void)
{
    if (!photo_home_active()) return 0;
    take_semaphore(menu_sem, 0);
    const struct photo_page * page = &photo_pages[photo_page_index];
    int index = photo_selection[photo_page_index];
    const struct photo_item * item = &page->items[index];
    struct menu * parent;
    struct menu_entry * entry = photo_resolve(item, &parent);
    if (parent && entry) photo_select_original(parent, entry);

    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);
    bmp_fill(COLOR_GRAY(5), 0, 0, 720, 48);
    bmp_printf(FONT(FONT_LARGE, COLOR_WHITE, COLOR_GRAY(5)), 16, 6, "%s", page->name);
    bmp_printf(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 540, 14, "Page %d/%d",
        index / PHOTO_ROWS + 1, (page->count + PHOTO_ROWS - 1) / PHOTO_ROWS);
    draw_line(0, 48, 719, 48, COLOR_GRAY(20));

    /* Six category badges in the PDF's left-hand rail. */
    for (int i = 0; i < (int)COUNT(photo_pages); i++)
    {
        int y = 60 + i * 58;
        int bg = i == photo_page_index ? COLOR_BLUE : COLOR_GRAY(10);
        bmp_fill(bg, 8, y, 44, 46);
        bmp_printf(FONT(FONT_LARGE, COLOR_WHITE, bg), 18, y + 5, "%s", photo_pages[i].badge);
        if (i == photo_page_index) bmp_draw_rect(COLOR_WHITE, 7, y - 1, 46, 48);
    }

    int first = (index / PHOTO_ROWS) * PHOTO_ROWS;
    for (int row = 0; row < PHOTO_ROWS && first + row < page->count; row++)
    {
        int n = first + row;
        int y = 62 + row * 48;
        int selected = n == index;
        int bg = selected ? COLOR_ORANGE : COLOR_BLACK;
        int fg = selected ? COLOR_BLACK : COLOR_WHITE;
        bmp_fill(bg, 64, y, 296, 43);
        bmp_fill(selected ? COLOR_BLACK : COLOR_BLUE, 70, y + 6, 27, 30);
        bmp_printf(FONT(FONT_MED, COLOR_WHITE, selected ? COLOR_BLACK : COLOR_BLUE),
            76, y + 9, "%d", row + 1);
        photo_text(FONT(FONT_MED_LARGE, fg, bg), 104, y + 6, 249, page->items[n].label);
    }

    bmp_fill(COLOR_GRAY(5), 370, 60, 342, 344);
    photo_text(FONT(FONT_MED_LARGE, COLOR_ORANGE, COLOR_GRAY(5)), 382, 72, 316, item->label);
    draw_line(376, 110, 704, 110, COLOR_GRAY(20));
    char help[MENU_MAX_HELP_LEN] = "";
    if (!item->entry)
    {
        photo_detail_row(0, "Open", "SET / Q");
        photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 382, 185, 316, "Original system menu");
        photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 382, 214, 316, "INFO returns to Photo UI");
        snprintf(help, sizeof(help), "Modules, settings and recovery remain available.");
    }
    else if (!entry)
    {
        photo_detail_row(0, "Status", "Unavailable");
        photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 382, 185, 316, "Module may not be loaded.");
        photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 382, 214, 316, "See Setup > Modules.");
        snprintf(help, sizeof(help), "No setting is changed when an item is unavailable.");
    }
    else
    {
        struct menu_display_info info;
        photo_read_info(entry, &info);
        /* Default display strings share storage; copy before reading children. */
        snprintf(help, sizeof(help), "%s", info.warning[0] ? info.warning :
            info.help[0] ? info.help : entry->help ? entry->help : "");
        photo_detail_row(0, "Current", info.value[0] ? info.value : entry->children ? "Q: options" : "SET: action");
        int row = 1;
        for (struct menu_entry * child = entry->children; child && row < 6; child = child->next)
        {
            if (child->shidden || child->placeholder || child->advanced) continue;
            photo_read_info(child, &info);
            if (child->shidden) continue;
            photo_detail_row(row++, info.name, info.value[0] ? info.value : "--");
        }
        if (entry->children)
            photo_text(FONT(FONT_SMALL, COLOR_CYAN, COLOR_GRAY(5)), 382, 374, 318, "Q opens all original options");
    }
    draw_line(0, 418, 719, 418, COLOR_GRAY(20));
    photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_BLACK), 12, 425, 696, help);
    photo_text(FONT(FONT_SMALL, COLOR_CYAN, COLOR_BLACK), 12, 458, 696,
        RECORDING
        ? "L/R Tab  Up/Down Item  SET Edit  Q/INFO Options  MENU Close"
        : "L/R Tab  Up/Down Item  SET Edit  Q Options  MENU Close  INFO Classic");
    give_semaphore(menu_sem);
    return 1;
}

/* Return 1 when consumed. Called outside menu_sem by the normal key handler. */
static int photo_menu_key(int key)
{
    /* INFO is Q on 600D while recording; leave that established mapping alone. */
    if (key == BGMT_INFO && !RECORDING)
    {
        photo_classic = !photo_classic;
        submenu_level = edit_mode = menu_lv_transparent_mode = menu_help_active = 0;
        return 1;
    }
    if (!photo_home_active()) return 0;
    const struct photo_page * page = &photo_pages[photo_page_index];
    switch (key)
    {
        case BGMT_PRESS_LEFT:
        case BGMT_WHEEL_LEFT:
            photo_page_index = MOD(photo_page_index - 1, COUNT(photo_pages));
            return 1;
        case BGMT_PRESS_RIGHT:
        case BGMT_WHEEL_RIGHT:
            photo_page_index = MOD(photo_page_index + 1, COUNT(photo_pages));
            return 1;
        case BGMT_PRESS_UP:
        case BGMT_WHEEL_UP:
            photo_selection[photo_page_index] = MOD(photo_selection[photo_page_index] - 1, page->count);
            return 1;
        case BGMT_PRESS_DOWN:
        case BGMT_WHEEL_DOWN:
            photo_selection[photo_page_index] = MOD(photo_selection[photo_page_index] + 1, page->count);
            return 1;
        case BGMT_MENU:
            give_semaphore(gui_sem);
            return 1;
        case BGMT_PRESS_SET:
        case BGMT_Q:
        case BGMT_PLAY:
        {
            const struct photo_item * item = &page->items[photo_selection[photo_page_index]];
            struct menu * parent;
            take_semaphore(menu_sem, 0);
            struct menu_entry * entry = photo_resolve(item, &parent);
            int ok = parent && (!item->entry || (entry && is_visible(entry)));
            int depth = ok ? photo_select_original(parent, entry) : 0;
            give_semaphore(menu_sem);
            if (!ok) return 1; /* Never act on an unrelated previously selected entry. */
            if (!item->entry) photo_classic = 1;
            else
            {
                submenu_level = depth;
                menu_entry_select(parent, key == BGMT_PRESS_SET ? 3 : 2);
            }
            return 1;
        }
        default:
            return 0;
    }
}
#endif
