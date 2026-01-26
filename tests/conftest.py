import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    options = Options()
    
    # --- 1. CONFIGURACIÓN DE IDENTIDAD (Anti-Bot) ---
    options.add_argument("--headless=new") 
    
    # Ocultamos que el navegador es controlado por Selenium
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # User-agent actualizado
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    # --- 2. CONFIGURACIÓN DE AUDIO Y AUTOPLAY (CRÍTICO PARA TRINITY) ---
    # Permite que el audio se reproduzca sin interacción humana real
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    # Silenciamos para evitar errores de drivers de sonido en servidores de CI
    options.add_argument("--mute-audio") 

    # --- 3. CONFIGURACIÓN DE ESTABILIDAD ---
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu") # Recomendado para modo headless en CI
    
    # Inicialización del driver con WebDriver Manager para evitar problemas de versiones
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # --- 4. PARCHE FINAL DE JAVASCRIPT ---
    # Borramos el rastro de la propiedad 'navigator.webdriver'
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    
    driver.quit()
