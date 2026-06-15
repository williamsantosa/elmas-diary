#!/usr/bin/env python3
import re
import urllib.request

for tree in ["firmware/common", "lib", "apps"]:
    try:
        html = urllib.request.urlopen(
            f"https://git.rockbox.org/cgit/rockbox.git/tree/{tree}", timeout=15
        ).read().decode("utf-8", "replace")
    except Exception:
        continue
    files = sorted(set(re.findall(rf"plain/{tree}/([^\"#]+?\.c)", html)))
    print(tree, "files", len(files))
    for name in files:
        try:
            data = urllib.request.urlopen(
                f"https://git.rockbox.org/cgit/rockbox.git/plain/{tree}/{name}", timeout=8
            ).read().decode("utf-8", "replace")
        except Exception:
            continue
        if "main_menu_" in data or "manage_settings" in data or "LANG_GENERAL_SETTINGS" in data:
            print(f"  HIT {tree}/{name}")
            for line in data.splitlines():
                if any(
                    x in line
                    for x in [
                        "main_menu_",
                        "manage_settings",
                        "LANG_GENERAL_SETTINGS",
                        "LANG_THEME_SETTINGS",
                        "LANG_TIME_AND_DATE",
                        "Icon_General_settings",
                        "Icon_Display_menu",
                        "MAKE_MENU",
                        "MENUITEM_RETURNVALUE",
                    ]
                ):
                    print("   ", line.strip()[:140])
