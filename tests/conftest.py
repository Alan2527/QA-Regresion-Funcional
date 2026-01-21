import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1000")
    
    driver = webdriver.Chrome(options=options)
    
    # BLOQUEO AGRESIVO NIVEL RED (CDP)
    # Esto mata el tráfico de imágenes y ads antes de que consuman RAM
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            "*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*.svg", "*.woff*", 
            "*google-analytics.com*", "*doubleclick.net*", "*googletagservices.com*",
            "*facebook.net*", "*twitter.com*", "*ads*", "*metrics*", "*video*"
        ]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    # Timeouts de seguridad
    driver.set_page_load_timeout(45)
    driver.set_script_timeout(15)
    
    yield driver
    driver.quit()
