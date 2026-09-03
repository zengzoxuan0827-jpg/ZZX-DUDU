import subprocess, time, os
from playwright.sync_api import sync_playwright
ROOT = r"C:\Users\Windows\Desktop\嘟嘟今天吃什么"
OUT = os.path.join(ROOT, "dist")
os.makedirs(OUT, exist_ok=True)
PORT = 8151
PY = r"C:\Users\Windows\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
srv = subprocess.Popen([PY, "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", ROOT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
    pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(OUT, "nav-home.png"))
    pg.evaluate("switchScreen('ingredients')"); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, "nav-ingredients.png"))
    pg.evaluate("switchScreen('record')"); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, "nav-record.png"))
    pg.evaluate("openScreen('ingredient-detail-screen')"); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, "nav-ingredient-detail.png"))
    b.close()
srv.terminate()
print("shots saved to", OUT)
