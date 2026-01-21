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
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    # Bloqueo por preferencias de Chrome
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.ads": 2,
        "profile.managed_default_content_settings.stylesheets": 1 # Mantenemos CSS
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60) # Aumentamos tiempo de carga pero no de lectura
    driver.set_window_size(1280, 800) # Tamaño menor para que la captura sea más liviana
    
    yield driver
    driver.quit()
