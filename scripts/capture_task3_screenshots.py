import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

os.makedirs("screenshots/task3", exist_ok=True)

def get_driver():
    # Try Chrome first
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1280,800")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        print("Using Chrome WebDriver")
        return driver
    except Exception as e:
        print(f"Chrome failed: {e}, trying Edge...")

    # Fallback to Edge
    try:
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--window-size=1280,800")
        edge_options.add_argument("--disable-gpu")
        driver = webdriver.Edge(options=edge_options)
        print("Using Edge WebDriver")
        return driver
    except Exception as e:
        print(f"Edge failed: {e}")
        raise

driver = get_driver()
driver.set_window_size(1280, 800)

pages = [
    ("http://localhost:8080/", "screenshots/task3/dashboard_live.png"),
    ("http://localhost:8080/cards", "screenshots/task3/cards_live.png"),
    ("http://localhost:8080/apply", "screenshots/task3/apply_live.png"),
    ("http://localhost:8080/actuator/health", "screenshots/task3/actuator_live.png")
]

for url, out_path in pages:
    print(f"Navigating to {url} ...")
    driver.get(url)
    driver.save_screenshot(out_path)
    print(f"Saved screenshot: {out_path} ({os.path.getsize(out_path)} bytes)")

driver.quit()
print("All live screenshots captured successfully!")
