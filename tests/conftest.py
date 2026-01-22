import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    
    # --- MODO HUMANO (Para el Login) ---
    options.add_argument("--headless=new") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # --- ESTABILIDAD ---
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Identidad de navegador real
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    # --- VELOCIDAD (Para todos los tests) ---
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*google-analytics.com*", "*doubleclick.net*", "*ads*", "*video*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    # Parche final para ocultar a Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    driver.quit()
