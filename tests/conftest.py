import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # --- CLAVE: BLOQUEO DE IMÁGENES Y RECURSOS PESADOS ---
    prefs = {
        "profile.managed_default_content_settings.images": 2, # 2 = Bloquear
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 2 # Opcional: bloquea CSS si quieres más velocidad
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    
    yield driver
    driver.quit()
