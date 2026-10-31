/* Canon camera properties; read-only Photo UI details. GPL-2.0-or-later. */
#ifdef CONFIG_600D
static MENU_UPDATE_FUNC(photo_camera_info_display)
{
    (void)entry;
    MENU_SET_VALUE("SET: Open");
}
static MENU_UPDATE_FUNC(photo_camera_model_display)
{
    (void)entry;
    MENU_SET_VALUE("%s", camera_model[0] ? camera_model : "Unavailable");
}
static MENU_UPDATE_FUNC(photo_camera_firmware_display)
{
    (void)entry;
    MENU_SET_VALUE("%s", firmware_version[0] ? firmware_version : "Unavailable");
}
static MENU_UPDATE_FUNC(photo_mechanical_display)
{
    (void)entry;
    if (!shutter_count_valid) { MENU_SET_VALUE("Unavailable"); return; }
    MENU_SET_VALUE("%d", shutter_count);
}
static MENU_UPDATE_FUNC(photo_liveview_display)
{
    (void)entry;
    if (!shutter_count_valid) { MENU_SET_VALUE("Unavailable"); return; }
    MENU_SET_VALUE("%d", shutter_count_plus_lv_actuations - shutter_count);
}
static MENU_UPDATE_FUNC(photo_combined_display)
{
    (void)entry;
    if (!shutter_count_valid) { MENU_SET_VALUE("Unavailable"); return; }
    MENU_SET_VALUE("%d", shutter_count_plus_lv_actuations);
}
static struct menu_entry photo_camera_info_menu[] = {
    { .name = "Camera Info", .update = photo_camera_info_display,
      .help = "Camera model and firmware reported by Canon.",
      .select = menu_open_submenu,
      .children = (struct menu_entry[]) {
          { .name = "Camera Model", .update = photo_camera_model_display,
            .icon_type = IT_ALWAYS_ON, .help = "Camera model reported by Canon." },
          { .name = "Canon Firmware", .update = photo_camera_firmware_display,
            .icon_type = IT_ALWAYS_ON, .help = "Canon firmware version reported by camera." },
          MENU_EOL,
      },
    },
};
static struct menu_entry photo_shutter_details[] = {
            { .name = "Mechanical Shutter", .update = photo_mechanical_display, .icon_type = IT_ALWAYS_ON,
              .help = "Mechanical shutter count from Canon." },
            { .name = "Live View Actuations", .update = photo_liveview_display, .icon_type = IT_ALWAYS_ON,
              .help = "Live View: combined minus mechanical." },
            { .name = "Combined Actuations", .update = photo_combined_display, .icon_type = IT_ALWAYS_ON,
              .help = "Combined mechanical and Live View count." },
            MENU_EOL,
        };
#endif
