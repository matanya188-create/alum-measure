# -*- coding: utf-8 -*-
# בנייה: עוטף את src/alum-measure.html בשלד PWA מלא ← index.html
# מעלה אוטומטית את מספר הגרסה ב-sw.js, מזריק אותו ל-APP_VERSION וכותב version.json
# שימוש: python build.py ואז git add -A && git commit && git push
import io, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))

# 1) גרסה חדשה מתוך sw.js
swp = os.path.join(HERE, "sw.js")
sw = io.open(swp, encoding="utf-8").read()
new_v = int(re.search(r'const VERSION = "v(\d+)";', sw).group(1)) + 1
sw = re.sub(r'const VERSION = "v\d+";', 'const VERSION = "v%d";' % new_v, sw)

# 2) גוף האפליקציה + הזרקת מספר הגרסה
src = io.open(os.path.join(HERE, "src", "alum-measure.html"), encoding="utf-8").read()
lines = src.split("\n")
body = "\n".join(l for l in lines if not (l.startswith("<title>") or l.startswith('<meta name="viewport"')))
body = body.replace("const APP_VERSION = 0;", "const APP_VERSION = %d;" % new_v)

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
<script src="three.min.js"></script>
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
io.open(swp, "w", encoding="utf-8").write(sw)
io.open(os.path.join(HERE, "version.json"), "w", encoding="utf-8").write(json.dumps({"version": new_v}))
print("built: index.html + version.json, version v%d" % new_v)
