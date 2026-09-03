from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
s = (ROOT / "index.html").read_text(encoding="utf-8")
ids = set(re.findall(r'id="([^"]+-screen)"', s))
opens = re.findall(r'data-open="([^"]+)"', s)
gos = re.findall(r'data-go="([^"]+)"', s)
backs = re.findall(r'data-back="([^"]+)"', s)

missing = []
for screen_id in opens:
    if screen_id not in ids:
        missing.append(screen_id)
for target in gos + backs:
    screen_id = f"{target}-screen"
    if screen_id not in ids:
        missing.append(screen_id)

print("screens", len(ids), sorted(ids))
print("missing", missing)
