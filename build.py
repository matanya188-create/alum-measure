# -*- coding: utf-8 -*-
# בנייה: עוטף את src/alum-measure.html בשלד PWA מלא ← index.html
# שימוש: python build.py   (ואז git commit+push, ולהעלות VERSION ב-sw.js)
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "src", "alum-measure.html"), encoding="utf-8").read()
lines = src.split("\n")
body = "\n".join(l for l in lines if not (l.startswith("<title>") or l.startswith('<meta name="viewport"')))

head = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<title>פנקס מדידות אלומיניום</title>
<meta name="description" content="מדידת חלונות, דלתות וויטרינות בשטח — וייצוא קובץ מסודר ליצרן">
<meta name="theme-color" content="#2c4e9e">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function(){ navigator.serviceWorker.register("sw.js"); });
}
</script>
</body>
</html>
"""
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(head + body + tail)

# העלאת VERSION ב-sw.js אוטומטית (v3 -> v4 וכו')
swp = os.path.join(HERE, "sw.js")
sw = io.open(swp, encoding="utf-8").read()
m = re.search(r'const VERSION = "v(\d+)";', sw)
new_v = int(m.group(1)) + 1
sw = re.sub(r'const VERSION = "v\d+";', 'const VERSION = "v%d";' % new_v, sw)
io.open(swp, "w", encoding="utf-8").write(sw)
print("index.html built, sw bumped to v%d" % new_v)
