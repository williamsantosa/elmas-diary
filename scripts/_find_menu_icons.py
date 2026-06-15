#!/usr/bin/env python3
import re
import urllib.request

BASE = "https://git.rockbox.org/cgit/rockbox.git/plain/apps/"

html = urllib.request.urlopen("https://git.rockbox.org/cgit/rockbox.git/tree/apps", timeout=20).read().decode(
    "utf-8", "replace"
)
files = re.findall(r'plain/apps/([^"]+)"', html)
targets = [f for f in files if "menu" in f.lower() or "setting" in f.lower()]
print("candidate files:", len(targets))

terms = [
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

for name in sorted(targets):
    try:
        data = urllib.request.urlopen(BASE + name, timeout=12).read().decode("utf-8", "replace")
    except Exception:
        continue
    hits = [line.strip() for line in data.splitlines() if any(t in line for t in terms)]
    if hits:
        print(f"\n=== {name} ===")
        for h in hits[:30]:
            print(h)
