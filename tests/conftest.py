import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    # Bloqueo básico para que vuele la carga
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*google-analytics.com*", "*doubleclick.net*", "*ads*", "*video*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    yield driver
    driver.quit()
