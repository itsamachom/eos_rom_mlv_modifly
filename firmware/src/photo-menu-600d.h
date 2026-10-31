/* Canon 600D Photo menu front end, GPL-2.0-or-later.
 * Modified 2026-10-30: serialize Photo UI state and bind edit/confirmation identity.
 * Included by menu.c: reuse its locking, values and editing paths.
 * No camera addresses or exposure/recording algorithms are changed here.
 */
#ifdef CONFIG_600D

#include "photo-thai-600d.h"

#define PHOTO_ROWS 6
#define PHOTO_DETAIL_ROWS (photo_thai_active() ? 3 : 4)
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
    {"Time-lapse", "Shoot", "Intervalometer"},
    {"Bulb Timer", "Shoot", "Bulb Timer"},
    {"Bracketing", "Shoot", "Advanced Bracket"},
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
    {"zebra settings", "Overlay", "Zebras"},
    {"Focus Peaking", "Overlay", "Focus Peak"},
    {"Magic Zoom", "Overlay", "Magic Zoom"},
    {"Histogram", "Overlay", "Histogram"},
    {"Spotmeter", "Overlay", "Spotmeter"},
    {"Cropmarks", "Overlay", "Cropmarks"},
    {"Waveform", "Overlay", "Waveform"},
    {"Global Draw", "Overlay", "Global Draw"},
};
static const struct photo_item photo_movie[] = {
    {"Bitrate (CBR)", "Movie", "Bit Rate"},
    {"Time Indicator", "Movie Tweaks", "Time Indicator"},
    {"REC key", "Movie", "REC key"},
    {"Movie Tweaks", "Movie", "Movie Tweaks"},
};
static const struct photo_item photo_setup[] = {
    {"Language", "Prefs", "Photo UI Language"},
    {"Modules", "Modules", NULL},
    {"Preferences", "Prefs", NULL},
    {"Display", "Display", NULL},
    {"Version / Help", "Help", NULL},
    {"Diagnostics", "Debug", NULL},
    {"Camera Info", "Help", "Camera Info"},
    {"Shutter Count", "Debug", "Shutter Count"},
    {"Audio", "Audio", NULL},
    {"Shoot (all)", "Shoot", NULL},
    {"Focus (all)", "Focus", NULL},
    {"Expo (all)", "Expo", NULL},
    {"Overlay (all)", "Overlay", NULL},
    {"Movie (all)", "Movie", NULL},
};
static const struct photo_item photo_games[] = {
    {"Arkanoid", "Games", "Arkanoid"},
    {"Pong", "Scripts", "Pong Game"},
    {"Sokoban", "Scripts", "Sokoban Game"},
    {"Modules", "Modules", NULL},
    {"Scripts", "Scripts", NULL},
};
#define PHOTO_PAGE(name, badge, items) {name, badge, items, COUNT(items)}
static const struct photo_page photo_pages[] = {
    PHOTO_PAGE("Shoot", "S", photo_shoot),
    PHOTO_PAGE("Focus", "F", photo_focus),
    PHOTO_PAGE("Expo", "E", photo_expo),
    PHOTO_PAGE("Overlay", "O", photo_overlay),
    PHOTO_PAGE("Movie", "V", photo_movie),
    PHOTO_PAGE("Setup", "+", photo_setup),
    PHOTO_PAGE("Games", "G", photo_games),
};

static int photo_page_index;
static int photo_selection[COUNT(photo_pages)];
static int photo_classic;
enum { PHOTO_CATEGORIES, PHOTO_ITEMS, PHOTO_DETAILS };
static int photo_pane;
static int photo_detail_index;
static int photo_editing;
static int photo_confirm;
static int photo_native_busy;
struct photo_identity {
    uintptr_t root, entry, parent, priv;
    menu_select_func select, select_Q;
    unsigned root_name, entry_name;
    int page, item, min, max, icon;
    int valid;
};
static struct photo_identity photo_display_identity;
static struct photo_identity photo_armed_identity;
/* Names, not cached pointers: modules may remove/reorder entries. */
static char photo_display_target[MENU_MAX_NAME_LEN];
static int photo_display_page = -1;
static int photo_display_item = -1;

static void photo_menu_reset(void)
{
    take_semaphore(menu_sem, 0);
    photo_classic = 0;
    photo_pane = PHOTO_CATEGORIES;
    photo_detail_index = photo_editing = photo_confirm = 0;
    photo_display_target[0] = 0;
    photo_display_page = photo_display_item = -1;
    photo_display_identity.valid = photo_armed_identity.valid = 0;
    give_semaphore(menu_sem);
}

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
    if (photo_thai_text(font, x, y, width, text)) return;
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

/* Resolve visible detail rows without retaining pointers between events. */
static struct menu_entry * photo_detail_entry(struct menu_entry * root, int index, int * count)
{
    struct menu_entry * result = NULL;
    int n = 0;
    if (root && is_visible(root))
    {
        int game_script = photo_page_index == 6 && root->select == menu_open_submenu &&
            root->icon_type == IT_ACTION && root->children;
        if (!game_script && (!root->children || root->priv || (root->select && root->select != menu_open_submenu)))
        {
            if (n == index) result = root;
            n++;
        }
        for (struct menu_entry * e = root->children; e; e = e->next)
        {
            if (!is_visible(e) || e->placeholder) continue;
            if (n == index) result = e;
            n++;
        }
    }
    *count = n;
    return result;
}

static int photo_can_edit(struct menu_entry * e)
{
    return e && e->icon_type != IT_ACTION && e->icon_type != IT_SUBMENU &&
        e->select != menu_open_submenu &&
        (e->select || (IS_ML_PTR(e->priv) && e->max > e->min));
}

static void photo_invalidate(void)
{
    photo_editing = photo_confirm = 0;
    photo_display_target[0] = 0;
    photo_display_identity.valid = photo_armed_identity.valid = 0;
}

/* All Photo UI state below is read/written with menu_sem held. No cached
 * object is dereferenced: re-resolve entries and compare their identities. */
static unsigned photo_name_hash(const char * name)
{
    unsigned hash = 2166136261u;
    while (name && *name) { hash ^= (unsigned char)*name++; hash *= 16777619u; }
    return hash;
}

static struct photo_identity photo_identity_of(struct menu_entry * root,
    struct menu_entry * entry, struct menu * parent)
{
    struct photo_identity id = {0};
    if (!root || !entry || !parent || !is_visible(root) || !is_visible(entry)) return id;
    id.root = (uintptr_t)root;
    id.entry = (uintptr_t)entry;
    id.parent = (uintptr_t)parent;
    id.priv = (uintptr_t)entry->priv;
    id.select = entry->select; id.select_Q = entry->select_Q;
    id.root_name = photo_name_hash(root->name); id.entry_name = photo_name_hash(entry->name);
    id.page = photo_page_index; id.item = photo_selection[photo_page_index];
    id.min = entry->min; id.max = entry->max; id.icon = entry->icon_type;
    id.valid = 1;
    return id;
}

static int photo_same_identity(const struct photo_identity * a, const struct photo_identity * b)
{
    return a->valid && b->valid && a->root == b->root && a->entry == b->entry &&
        a->parent == b->parent && a->priv == b->priv && a->select == b->select &&
        a->select_Q == b->select_Q && a->root_name == b->root_name &&
        a->entry_name == b->entry_name && a->page == b->page && a->item == b->item &&
        a->min == b->min && a->max == b->max && a->icon == b->icon;
}

static void photo_check_armed(const struct photo_identity * current)
{
    if ((photo_editing || photo_confirm) &&
        (photo_pane != PHOTO_DETAILS || !photo_same_identity(&photo_armed_identity, current)))
        photo_invalidate();
}

static void photo_validate_selection(void)
{
    if (photo_page_index < 0 || photo_page_index >= (int)COUNT(photo_pages))
    {
        photo_page_index = 0; photo_detail_index = 0; photo_invalidate();
    }
    int * index = &photo_selection[photo_page_index];
    if (*index < 0 || *index >= photo_pages[photo_page_index].count)
    {
        *index = 0; photo_detail_index = 0; photo_invalidate();
    }
    if (photo_pane < PHOTO_CATEGORIES || photo_pane > PHOTO_DETAILS)
    {
        photo_pane = PHOTO_CATEGORIES; photo_invalidate();
    }
    if (photo_detail_index < 0) { photo_detail_index = 0; photo_invalidate(); }
}

static void photo_detail_row(int row, const char * name, const char * value, int selected)
{
    int pitch = photo_thai_active() ? 92 : 70;
    int y = 113 + row * pitch;
    int bg = selected ? COLOR_ORANGE : COLOR_GRAY(5);
    int fg = selected ? COLOR_BLACK : COLOR_WHITE;
    bmp_fill(bg, 376, y, 330, pitch - 3);
    photo_text(FONT(FONT_MED_LARGE, fg, bg), 382, y + 1, 318, name);
    photo_text(FONT(FONT_LARGE, selected ? COLOR_BLACK : COLOR_CYAN, bg),
        382, y + (photo_thai_active() ? 39 : 31), 318, value);
    draw_line(376, y + pitch - 2, 705, y + pitch - 2, COLOR_GRAY(15));
}

static int photo_menu_draw(void)
{
    take_semaphore(menu_sem, 0);
    if (photo_native_busy)
    {
        /* Keep the displayed buffer until a callback (which may lock menus)
         * finishes. Do not reselect or dereference its menu in another task. */
        menu_redraw_cancel = 1;
        give_semaphore(menu_sem);
        return 1;
    }
    if (!photo_home_active()) { give_semaphore(menu_sem); return 0; }
    photo_validate_selection();
    photo_thai_prepare();
    const int page_index = photo_page_index;
    const struct photo_page * page = &photo_pages[page_index];
#ifdef PHOTO_MENU_SNAPSHOT_OBSERVER
    PHOTO_MENU_SNAPSHOT_OBSERVER();
#endif
    int index = photo_selection[page_index];
    const struct photo_item * item = &page->items[index];
    struct menu * parent;
    struct menu_entry * entry = photo_resolve(item, &parent);
    if (parent && entry) photo_select_original(parent, entry);
    int count = 0;
    photo_detail_entry(entry, -1, &count);
    if (photo_detail_index >= count)
    {
        photo_detail_index = count ? count - 1 : 0;
        photo_invalidate();
    }
    struct menu_entry * current = photo_detail_entry(entry, photo_detail_index, &count);
    struct menu * current_parent = current == entry ? parent : current ? current->parent_menu : NULL;
    struct photo_identity current_id = photo_identity_of(entry, current, current_parent);
    photo_check_armed(&current_id);

    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);
    bmp_fill(COLOR_GRAY(5), 0, 0, 720, 48);
    photo_text(FONT(FONT_LARGE, COLOR_WHITE, COLOR_GRAY(5)), 16, 2, 500, page->name);
    photo_text(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 530, 8, 92,
        photo_pane == PHOTO_DETAILS ? "Options" : "Page");
    bmp_printf(FONT(FONT_MED, COLOR_WHITE, COLOR_GRAY(5)), 633, 14, "%d/%d",
        photo_pane == PHOTO_DETAILS ? photo_detail_index / PHOTO_DETAIL_ROWS + 1 : index / PHOTO_ROWS + 1,
        photo_pane == PHOTO_DETAILS ? (count ? (count + PHOTO_DETAIL_ROWS - 1) / PHOTO_DETAIL_ROWS : 1) :
        (page->count + PHOTO_ROWS - 1) / PHOTO_ROWS);
    draw_line(0, 48, 719, 48, COLOR_GRAY(20));

    for (int i = 0; i < (int)COUNT(photo_pages); i++)
    {
        int y = 60 + i * 48;
        int bg = i == photo_page_index ? COLOR_BLUE : COLOR_GRAY(10);
        bmp_fill(bg, 8, y, 44, 42);
        bmp_printf(FONT(FONT_LARGE, COLOR_WHITE, bg), 18, y + 5, "%s", photo_pages[i].badge);
        if (i == photo_page_index)
            bmp_draw_rect(photo_pane == PHOTO_CATEGORIES ? COLOR_ORANGE : COLOR_WHITE, 7, y - 1, 46, 44);
    }

    int first = (index / PHOTO_ROWS) * PHOTO_ROWS;
    for (int row = 0; row < PHOTO_ROWS && first + row < page->count; row++)
    {
        int n = first + row;
        int y = 60 + row * 56;
        int selected = n == index;
        int bg = selected ? (photo_pane == PHOTO_ITEMS ? COLOR_ORANGE : COLOR_GRAY(15)) : COLOR_BLACK;
        int fg = selected && photo_pane == PHOTO_ITEMS ? COLOR_BLACK : COLOR_WHITE;
        bmp_fill(bg, 64, y, 296, 51);
        photo_text(FONT(FONT_LARGE, fg, bg), 76, y + (photo_thai_active() ? 3 : 8), 276, page->items[n].label);
    }

    bmp_fill(COLOR_GRAY(5), 370, 60, 342, 334);
    if (photo_pane == PHOTO_DETAILS)
        bmp_draw_rect(photo_editing ? COLOR_ORANGE : COLOR_CYAN, 369, 59, 344, 336);
    photo_text(FONT(photo_thai_active() ? FONT_MED_LARGE : FONT_LARGE, COLOR_ORANGE, COLOR_GRAY(5)),
        382, 64, 316, item->label);
    draw_line(376, 106, 704, 106, COLOR_GRAY(20));
    char help[MENU_MAX_HELP_LEN] = "";
    photo_display_target[0] = 0;
    photo_display_identity.valid = 0;
    photo_display_page = page_index;
    photo_display_item = index;
    if (!item->entry && parent)
    {
        photo_detail_row(0, "System menu", "SET: Open", 0);
        photo_text(FONT(FONT_MED_LARGE, COLOR_WHITE, COLOR_GRAY(5)), 382, 218, 316, "INFO: Photo / Classic");
        snprintf(help, sizeof(help), "Original system settings remain available.");
    }
    else if (!entry || !is_visible(entry))
    {
        photo_detail_row(0, "Status", "Unavailable", 0);
        const char * module_hint = photo_page_index == 6 && item->entry && streq(item->entry, "Arkanoid")
            ? "Load arkanoid; reboot." : photo_page_index == 6 && item->entry &&
            (streq(item->entry, "Pong Game") || streq(item->entry, "Sokoban Game"))
            ? "Load lua; reboot." : "See Setup > Modules";
        photo_text(FONT(FONT_MED_LARGE, COLOR_WHITE, COLOR_GRAY(5)), 382, 218, 316, module_hint);
        snprintf(help, sizeof(help), "%s", photo_page_index == 6 && item->entry && streq(item->entry, "Arkanoid")
            ? "Arkanoid needs arkanoid.mo loaded after restart." : photo_page_index == 6 && item->entry &&
            (streq(item->entry, "Pong Game") || streq(item->entry, "Sokoban Game"))
            ? "Pong and Sokoban use lua.mo, not separate modules."
            : "Module may not be loaded; no action is performed.");
    }
    else
    {
        struct menu_display_info info;
        photo_read_info(entry, &info);
        snprintf(help, sizeof(help), "%s", info.warning[0] ? info.warning :
            info.help[0] ? info.help : entry->help ? entry->help : "");
        int first_detail = (photo_detail_index / PHOTO_DETAIL_ROWS) * PHOTO_DETAIL_ROWS;
        for (int row = 0; row < PHOTO_DETAIL_ROWS && first_detail + row < count; row++)
        {
            int n = first_detail + row;
            struct menu_entry * e = photo_detail_entry(entry, n, &count);
            if (!e) continue;
            int selected = photo_pane == PHOTO_DETAILS && n == photo_detail_index;
            struct menu * ep = e == entry ? parent : e->parent_menu;
            if (selected && ep) photo_select_original(ep, e);
            photo_read_info(e, &info);
            if (selected)
            {
                struct photo_identity id = photo_identity_of(entry, e, ep);
                photo_check_armed(&id);
                photo_display_identity = id;
                snprintf(photo_display_target, sizeof(photo_display_target), "%s", e->name);
                if (info.warning[0] || info.help[0] || e->help)
                    snprintf(help, sizeof(help), "%s", info.warning[0] ? info.warning :
                        info.help[0] ? info.help : e->help);
            }
            const char * label = e == entry ? (e->icon_type == IT_ACTION ?
                (photo_page_index == 6 ? "Start game" : "Action") : "Current") : info.name;
            if (selected && photo_page_index == 6)
                snprintf(help, sizeof(help), "%s", streq(item->entry, "Arkanoid")
                    ? "SET twice starts Arkanoid; Left/Right advances intro."
                    : "Run Script starts the game; leave Autorun off.");
            photo_detail_row(row, label, info.value[0] ? info.value :
                e->children ? "SET: Open" : e->select ? "SET: Run" : "Read only", selected);
        }
    }
    /* Update callbacks can hide/reorder rows during this same redraw. Only
     * publish a display identity that still resolves to the row just shown. */
    current = photo_detail_entry(entry, photo_detail_index, &count);
    current_parent = current == entry ? parent : current ? current->parent_menu : NULL;
    current_id = photo_identity_of(entry, current, current_parent);
    photo_check_armed(&current_id);
    if (!photo_same_identity(&photo_display_identity, &current_id)) photo_display_identity.valid = 0;
    draw_line(0, 400, 719, 400, COLOR_GRAY(20));
    photo_text(FONT(FONT_MED_LARGE, COLOR_WHITE, COLOR_BLACK), 12, 402, 696,
        photo_thai_enabled && !photo_thai_active() && RECORDING && !photo_thai_attempted
        ? "Thai loads after recording; using English." :
        photo_thai_enabled && !photo_thai_active() ? "Thai font missing or mismatched; using English." :
        photo_confirm ? "Run this action? SET confirms; MENU cancels." : help);
    const char * hint = photo_pane == PHOTO_CATEGORIES
        ? "Up/Down Category   Right/SET Open   MENU Close"
        : photo_pane == PHOTO_ITEMS
        ? "Up/Down Item   Right/SET Options   Left Back"
        : photo_editing
        ? "Left/Right Change   SET Done   MENU Done"
        : "Up/Down Option   SET Edit   Left Back   Q More";
    photo_text(FONT(FONT_MED, COLOR_CYAN, COLOR_BLACK), 12, 445, 696,
        photo_confirm ? "SET Run   MENU Cancel" : hint);
    give_semaphore(menu_sem);
    return 1;
}

/* Re-resolve and select the exact visible target immediately before editing.
 * Caller holds menu_sem. Presentation and armed-operation identities are
 * separate, so redraw cannot transfer an edit or confirmation to a new row.
 */
static struct menu_entry * photo_edit_target(struct menu ** parent, int * depth)
{
    const struct photo_item * item = &photo_pages[photo_page_index].items[photo_selection[photo_page_index]];
    struct menu * root_parent;
    struct menu_entry * root = photo_resolve(item, &root_parent);
    int count;
    struct menu_entry * e = photo_detail_entry(root, photo_detail_index, &count);
    if (!e) return NULL;
    *parent = e == root ? root_parent : e->parent_menu;
    if (!*parent || !is_visible(e)) return NULL;
    struct photo_identity id = photo_identity_of(root, e, *parent);
    if (!photo_same_identity(&photo_display_identity, &id) ||
        ((photo_editing || photo_confirm) && !photo_same_identity(&photo_armed_identity, &id)))
    {
        photo_invalidate();
        return NULL;
    }
    *depth = photo_select_original(*parent, e);
    return e;
}

static void photo_run_original(struct menu * parent, int depth, int mode)
{
    int old_level = submenu_level;
    submenu_level = depth;
    menu_entry_select(parent, mode);
    /* Plain value changes stay inline. Native submenus, custom editors and
     * Live View editors keep the state they explicitly requested. */
    if (submenu_level == depth && !edit_mode && !menu_lv_transparent_mode)
        submenu_level = old_level;
}

struct photo_pending_action { struct menu * parent; int depth, mode; };

/* menu_sem is held. Callbacks are dispatched only after releasing it. */
static int photo_menu_key_locked(int key, struct photo_pending_action * pending)
{
    if (key == BGMT_INFO && !RECORDING)
    {
        /* INFO from a native modal editor returns directly to Photo UI. */
        photo_classic = photo_home_active();
        submenu_level = edit_mode = menu_lv_transparent_mode = menu_help_active = 0;
        photo_invalidate();
        return 1;
    }
    if (!photo_home_active()) return 0;
    if (key == BGMT_INFO && RECORDING) key = BGMT_Q;
    const struct photo_page * page = &photo_pages[photo_page_index];
    int up = key == BGMT_PRESS_UP || key == BGMT_WHEEL_UP;
    int down = key == BGMT_PRESS_DOWN || key == BGMT_WHEEL_DOWN;
    int left = key == BGMT_PRESS_LEFT || key == BGMT_WHEEL_LEFT;
    int right = key == BGMT_PRESS_RIGHT || key == BGMT_WHEEL_RIGHT;
    int set = key == BGMT_PRESS_SET;
    int q = key == BGMT_Q || key == BGMT_PLAY;

    if (key == BGMT_MENU)
    {
        if (photo_editing || photo_confirm) photo_invalidate();
        else give_semaphore(gui_sem);
        return 1;
    }
    if (photo_confirm && !set) photo_confirm = 0;
    if (photo_editing)
    {
        if (set) { photo_invalidate(); return 1; }
        if (left || right || key == BGMT_WHEEL_UP || key == BGMT_WHEEL_DOWN)
        {
            struct menu * parent = NULL;
            int depth = 0;
            struct menu_entry * e = photo_edit_target(&parent, &depth);
            int ok = photo_can_edit(e);
            if (ok) *pending = (struct photo_pending_action){parent, depth, (left || key == BGMT_WHEEL_UP) ? 1 : 0};
            else photo_invalidate();
            return 1;
        }
        return up || down || q; /* don't leave an edit accidentally */
    }
    if (up || down)
    {
        int delta = up ? -1 : 1;
        photo_invalidate();
        if (photo_pane == PHOTO_CATEGORIES)
        {
            photo_page_index = MOD(photo_page_index + delta, COUNT(photo_pages));
            photo_detail_index = 0;
        }
        else if (photo_pane == PHOTO_ITEMS)
        {
            photo_selection[photo_page_index] = MOD(photo_selection[photo_page_index] + delta, page->count);
            photo_detail_index = 0;
        }
        else
        {
            struct menu * parent;
            int count;
            struct menu_entry * root = photo_resolve(&page->items[photo_selection[photo_page_index]], &parent);
            photo_detail_entry(root, -1, &count);
            if (count) photo_detail_index = MOD(MOD(photo_detail_index, count) + delta, count);
        }
        return 1;
    }
    if (left)
    {
        if (photo_pane > PHOTO_CATEGORIES) photo_pane--;
        photo_invalidate();
        return 1;
    }
    if (photo_pane < PHOTO_DETAILS && (right || set || q))
    {
        const struct photo_item * item = &page->items[photo_selection[photo_page_index]];
        if (photo_pane == PHOTO_ITEMS && !item->entry)
        {
            struct menu * parent;
            photo_resolve(item, &parent);
            if (parent) { photo_select_original(parent, NULL); photo_classic = 1; }
        }
        else photo_pane++;
        photo_invalidate();
        return 1;
    }
    if (photo_pane == PHOTO_DETAILS && (set || q))
    {
        struct menu * parent = NULL;
        int depth = 0;
        struct menu_entry * e = photo_edit_target(&parent, &depth);
        int editable = photo_can_edit(e);
        int action = e && e->icon_type == IT_ACTION;
        int open = e && (e->children || e->select == menu_open_submenu);
        if (!e) { photo_invalidate(); return 1; }
        if (q) { photo_invalidate(); *pending = (struct photo_pending_action){parent, depth, 2}; }
        else if (editable)
        {
            photo_armed_identity = photo_display_identity;
            photo_editing = 1; photo_confirm = 0;
        }
        else if (action)
        {
            if (!photo_confirm) { photo_armed_identity = photo_display_identity; photo_confirm = 1; }
            else { photo_invalidate(); *pending = (struct photo_pending_action){parent, depth, 3}; }
        }
        else if (open) { photo_invalidate(); *pending = (struct photo_pending_action){parent, depth, 3}; }
        return 1;
    }
    /* Right at the rightmost pane does not modify anything. */
    return right;
}

/* Modified 2026-10-30: all Photo UI key-state transitions share the renderer's
 * lock; callbacks remain outside it to permit native menu reentrancy. */
static int photo_menu_key(int key)
{
    /* Native-only keys (notably half-shutter) must not wait for a redraw. */
    switch (key)
    {
        case BGMT_INFO: case BGMT_MENU: case BGMT_PRESS_SET: case BGMT_Q: case BGMT_PLAY:
        case BGMT_PRESS_UP: case BGMT_PRESS_DOWN: case BGMT_PRESS_LEFT: case BGMT_PRESS_RIGHT:
        case BGMT_WHEEL_UP: case BGMT_WHEEL_DOWN: case BGMT_WHEEL_LEFT: case BGMT_WHEEL_RIGHT:
            break;
        default: return 0;
    }
    struct photo_pending_action pending = {0};
    take_semaphore(menu_sem, 0);
    if (photo_native_busy) { give_semaphore(menu_sem); return 1; }
    photo_validate_selection();
    int consumed = photo_menu_key_locked(key, &pending);
    if (pending.parent) photo_native_busy = 1;
    give_semaphore(menu_sem);
    if (pending.parent)
    {
        photo_run_original(pending.parent, pending.depth, pending.mode);
        take_semaphore(menu_sem, 0);
        photo_native_busy = 0;
        give_semaphore(menu_sem);
    }
    return consumed;
}
#endif
