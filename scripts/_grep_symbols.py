#!/usr/bin/env python3
import re
import urllib.request

BASE = "https://git.rockbox.org/cgit/rockbox.git/plain/apps/"
html = urllib.request.urlopen("https://git.rockbox.org/cgit/rockbox.git/tree/apps", timeout=20).read().decode(
    "utf-8", "replace"
)
files = sorted(set(re.findall(r"plain/apps/([^\"#]+?\.c)", html)))

terms = [
    "general_settings",
    "theme_settings",
    "time_and_date",
    "manage_settings",
    "main_menu_",
    "Icon_General_settings",
    "Icon_Display_menu",
    "MAKE_MENU",
]

for name in files:
    try:
        data = urllib.request.urlopen(BASE + name, timeout=8).read().decode("utf-8", "replace")
    except Exception:
        continue
    hits = [line.strip() for line in data.splitlines() if any(t in line for t in terms)]
    if hits:
        print(f"\n=== {name} ===")
        for h in hits[:25]:
            print(h)
