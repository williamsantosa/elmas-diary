#!/usr/bin/env python3
import re
import urllib.request

terms = [
    "LANG_THEME_MENU",
    "LANG_GENERAL_SETTINGS",
    "LANG_TIME_MENU",
    "Icon_General_settings_menu",
    "Icon_Display_menu",
]

for tree in ["apps", "firmware/common", "firmware/target", "lib"]:
    try:
        html = urllib.request.urlopen(
            f"https://git.rockbox.org/cgit/rockbox.git/tree/{tree}", timeout=15
        ).read().decode("utf-8", "replace")
    except Exception:
        continue
    files = sorted(set(re.findall(rf"plain/{re.escape(tree)}/([^\"#]+)", html)))
    for name in files:
        if not name.endswith((".c", ".h", ".S", ".cpp")):
            continue
        try:
            data = urllib.request.urlopen(
                f"https://git.rockbox.org/cgit/rockbox.git/plain/{tree}/{name}", timeout=8
            ).read().decode("utf-8", "replace")
        except Exception:
            continue
        hits = [line.strip() for line in data.splitlines() if any(t in line for t in terms)]
        if hits:
            print(f"\n=== {tree}/{name} ===")
            for h in hits:
                print(h)
