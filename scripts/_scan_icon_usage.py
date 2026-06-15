#!/usr/bin/env python3
import re
import urllib.request

terms = ["Icon_Display_menu", "Icon_General_settings_menu", "Icon_Menu_setting", "Icon_Submenu"]

html = urllib.request.urlopen(
    "https://git.rockbox.org/cgit/rockbox.git/tree/apps", timeout=15
).read().decode("utf-8", "replace")
files = sorted(set(re.findall(r"plain/apps/([^\"#]+)", html)))
for name in files:
    if not name.endswith(".c"):
        continue
    try:
        data = urllib.request.urlopen(
            f"https://git.rockbox.org/cgit/rockbox.git/plain/apps/{name}", timeout=8
        ).read().decode("utf-8", "replace")
    except Exception:
        continue
    hits = [line.strip() for line in data.splitlines() if any(t in line for t in terms)]
    if hits:
        print(f"\n=== apps/{name} ===")
        for h in hits:
            print(h)
