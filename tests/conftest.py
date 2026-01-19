import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # Desactivar extensiones y anuncios de forma agresiva
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") 
    # Forzar uso de memoria en disco en lugar de RAM compartida
    chrome_options.add_argument("--disable-setuid-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    # Tiempos de espera cortos para que falle rápido si no puede
    driver.set_page_load_timeout(25) 
    driver.set_script_timeout(20)
    
    yield driver
    try:
        driver.quit()
    except:
        pass # Ignorar error si el proceso ya murió
