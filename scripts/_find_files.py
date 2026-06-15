#!/usr/bin/env python3
import re
import urllib.request

html = urllib.request.urlopen("https://git.rockbox.org/cgit/rockbox.git/tree/", timeout=30).read().decode(
    "utf-8", "replace"
)
for pat in [r'plain/([^"]*manage[^"]*\.c)', r'plain/([^"]*main_menu[^"]*\.c)', r'plain/([^"]*settings_menu[^"]*)']:
    found = sorted(set(re.findall(pat, html, re.I)))
    print(pat, "->", found[:30])
