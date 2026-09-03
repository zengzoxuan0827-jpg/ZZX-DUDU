import subprocess, time, sys
from pathlib import Path

VENV = Path(r"C:\Users\Windows\.workbuddy\binaries\python\envs\default")
PY = str(VENV / "Scripts" / "python.exe")
ROOT = Path(r"C:\Users\Windows\Desktop\嘟嘟今天吃什么")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1) 启动静态服务器
srv = subprocess.Popen([PY, "-m", "http.server", "8102", "--bind", "127.0.0.1"],
                       cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# 2) 用 Playwright + 系统 Chrome 截图
import playwright
from playwright.sync_api import sync_playwright

out = ROOT / "verify_before_after.png"
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 400, "height": 900}, device_scale_factor=2)
    page.goto("http://127.0.0.1:8102/index.html", wait_until="networkidle")
    # 切到记录页
    page.evaluate("""() => {
        const el = document.querySelector('[data-go=\"record\"]');
        if (el) el.click();
    }""")
    page.wait_for_timeout(600)
    page.screenshot(path=str(out))
    browser.close()

srv.terminate()
print("SCREENSHOT:", out)
