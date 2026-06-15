#!/usr/bin/env python3
import re
import urllib.request

BASE = "https://git.rockbox.org/cgit/rockbox.git/plain/apps/"
html = urllib.request.urlopen("https://git.rockbox.org/cgit/rockbox.git/tree/apps", timeout=20).read().decode(
    "utf-8", "replace"
)
files = sorted(set(re.findall(r"plain/apps/([^\"#]+?\.c)", html)))
print("files", len(files))

terms = [
    "LANG_THEME_SETTINGS",
    "LANG_TIME_AND_DATE",
    "LANG_GENERAL_SETTINGS",
    "Icon_General_settings_menu",
    "Icon_Display_menu",
]

for name in files:
    try:
        data = urllib.request.urlopen(BASE + name, timeout=8).read().decode("utf-8", "replace")
    except Exception:
        continue
    hits = [line.strip() for line in data.splitlines() if any(t in line for t in terms)]
    if hits:
        print(f"\n=== {name} ===")
        for h in hits:
            print(h)
