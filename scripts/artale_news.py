"""Refresh the latest Artale announcements between the ARTALE markers in README.md."""
import json
import re
import urllib.request

SRC = "https://juzisphina.github.io/artale-news/data/news.json"
ICON = {"update": "🍊", "maintenance": "🔧", "event": "🎉", "shop": "🛍️", "sanction": "🚫"}

req = urllib.request.Request(SRC, headers={"User-Agent": "juzisphina-profile"})
posts = json.load(urllib.request.urlopen(req, timeout=30))["posts"]
posts = [p for p in posts if p["category"] != "sanction"][:5]
lines = [f"- {ICON.get(p['category'], '📌')} `{p['date']}` [{p['title']}]({p['url']})" for p in posts]
block = "<!-- ARTALE:START -->\n" + "\n".join(lines) + "\n<!-- ARTALE:END -->"

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
new = re.sub(r"<!-- ARTALE:START -->.*?<!-- ARTALE:END -->", lambda m: block, readme, flags=re.S)
if new != readme:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new)
    print("updated")
else:
    print("no change")
