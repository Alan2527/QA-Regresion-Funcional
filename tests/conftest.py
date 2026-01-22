import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    # --- CONFIGURACIÓN DE CHROME ---
    options = Options()
    options.add_argument("--headless=new")  # Modo sin ventana para GitHub Actions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1000") # Tamaño de ventana fijo para capturas consistentes
    
    driver = webdriver.Chrome(options=options)
    
    # --- BLOQUEO SELECTIVO DE RED (CDP) ---
    # Bloqueamos solo lo pesado/molesto para que la página sea liviana 
    # pero conserve los ESTILOS (CSS) y FUENTES para que se vea bien.
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            # Bloqueamos imágenes pesadas
            "*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*.svg", 
            # Bloqueamos trackers y publicidad (lo que suele trabar el sitio)
            "*google-analytics.com*", "*doubleclick.net*", "*googletagservices.com*",
            "*facebook.net*", "*twitter.com*", "*ads*", "*metrics*", "*video*",
            # Bloqueamos otros elementos innecesarios
            "*.mp4", "*.m4v"
        ]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    # --- TIMEOUTS DE SEGURIDAD ---
    # Tiempo máximo para cargar la estructura de la página
    driver.set_page_load_timeout(45)
    # Tiempo máximo para que los scripts internos respondan
    driver.set_script_timeout(15)
    
    yield driver
    
    # --- CIERRE ---
    driver.quit()
