import subprocess, time, os, sys
from playwright.sync_api import sync_playwright

ROOT = r"C:\Users\Windows\Desktop\嘟嘟今天吃什么"
PORT = 8137
OUT = r"C:\Users\Windows\AppData\Local\Temp\shots_nav"
os.makedirs(OUT, exist_ok=True)
PY = r"C:\Users\Windows\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

srv = subprocess.Popen([PY, "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", ROOT],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

console_errors = []
page_errors = []

def snap(name):
    pg.screenshot(path=os.path.join(OUT, f"{name}.png"))
    print("shot", name)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.on("console", lambda m: console_errors.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: page_errors.append(str(e)))
    pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
    pg.wait_for_timeout(700)

    def state():
        return pg.evaluate("""() => {
          const active = document.querySelector('.screen.active');
          const tab = document.querySelector('.tabbar');
          const backs = [...document.querySelectorAll('.screen.active .back-button')].map(b=>b.dataset.back);
          const homeActive = active && active.id === 'home-screen';
          return {
            active: active ? active.id : null,
            tabHidden: tab ? tab.classList.contains('hidden') : null,
            backButtons: backs,
            mood: (document.getElementById('mood-title')||{}).textContent
          };
        }""")

    print("HOME:", state()); snap("home")
    # go to ingredients
    pg.evaluate("switchScreen('ingredients')"); pg.wait_for_timeout(400)
    print("INGREDIENTS:", state()); snap("ingredients")
    # back to home
    pg.evaluate("switchScreen('home')"); pg.wait_for_timeout(300)
    print("BACK HOME:", state())
    # go to record
    pg.evaluate("switchScreen('record')"); pg.wait_for_timeout(400)
    print("RECORD:", state()); snap("record")
    # open ingredient-detail from ingredients
    pg.evaluate("switchScreen('ingredients')"); pg.wait_for_timeout(300)
    pg.evaluate("openScreen('ingredient-detail-screen')"); pg.wait_for_timeout(400)
    print("ING-DETAIL:", state()); snap("ingredient-detail")
    # back to ingredients
    pg.evaluate("switchScreen('ingredients')"); pg.wait_for_timeout(300)
    print("ING-DETAIL BACK:", state())
    # sub screens
    for s in ["recipe-detail-screen","baby-profile-screen","add-ingredient-screen","record-detail-screen","history-screen","reminder-screen"]:
        pg.evaluate(f"openScreen('{s}')"); pg.wait_for_timeout(400); snap(s.split('-')[0])
    # amount label check
    amt = pg.evaluate("document.querySelector('.amount-card .form-name').textContent")
    print("AMOUNT LABEL:", amt)
    # use-up toast name (open ingredient detail, click use-up)
    pg.evaluate("openScreen('ingredient-detail-screen')"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('[data-action=use-up-ingredient]').click()"); pg.wait_for_timeout(300)
    toast = pg.evaluate("document.getElementById('toast').textContent")
    print("USE-UP TOAST:", toast)
    b.close()

srv.terminate()
print("\nCONSOLE(errors/warnings):", console_errors)
print("PAGE ERRORS:", page_errors)
print("\nRESULT:", "OK" if (not page_errors and not [e for e in console_errors if e.startswith('error')]) else "HAS ERRORS")
