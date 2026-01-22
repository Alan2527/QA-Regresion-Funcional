import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Identidad de navegador real para evitar bloqueos
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    # Mantener el bloqueo de red para velocidad
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*google-analytics.com*", "*doubleclick.net*", "*ads*", "*video*", "*metrics*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    yield driver
    driver.quit()
