import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    
    # --- 1. CONFIGURACIÓN DE IDENTIDAD & HEADLESS ---
    options.add_argument("--headless=new") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    # --- 2. PERMISOS DE AUDIO (Para que Trinity avance el tiempo) ---
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--mute-audio") 

    # --- 3. ESTABILIDAD CI ---
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    
    # En el CI de GitHub no hace falta Service(ChromeDriverManager) 
    # porque el driver ya está en el sistema.
    driver = webdriver.Chrome(options=options)
    
    # Parche anti-detección
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    driver.quit()
