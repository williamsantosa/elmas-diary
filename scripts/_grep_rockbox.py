#!/usr/bin/env python3
import urllib.request

BASE = "https://git.rockbox.org/cgit/rockbox.git/plain/apps/"
CANDIDATES = [
    "root_menu.c",
    "menu.c",
    "settings.c",
    "sound.c",
    "playlist.c",
    "plugin.c",
    "bookmark.c",
    "tagcache.c",
    "file.c",
    "filetypes.c",
    "onplay.c",
    "screens.c",
    "debug_menu.c",
    "info.c",
    "language.c",
    "keyboard.c",
    "shortcuts.c",
    "shortcut.c",
    "shortcut_menu.c",
    "shortcuts_menu.c",
    "general_settings.c",
    "theme_settings.c",
    "display_settings.c",
    "time_settings.c",
    "time_and_date.c",
    "time.c",
    "manage_settings.c",
    "main_menu.c",
    "settings_menu.c",
    "menus.c",
    "menu_data.c",
]

TERMS = [
    "LANG_THEME_SETTINGS",
    "LANG_TIME_AND_DATE",
    "LANG_GENERAL_SETTINGS",
    "LANG_SHORTCUTS",
    "Icon_General_settings_menu",
    "Icon_Display_menu",
    "Icon_Submenu",
    "Icon_Menu_setting",
    "Icon_Bookmark",
    "Icon_Submenu_Entered",
]

for name in CANDIDATES:
    try:
        data = urllib.request.urlopen(BASE + name, timeout=10).read().decode("utf-8", "replace")
    except Exception:
        continue
    hits = [line.strip() for line in data.splitlines() if any(t in line for t in TERMS)]
    if hits:
        print(f"\n=== {name} ===")
        for h in hits:
            print(h)
