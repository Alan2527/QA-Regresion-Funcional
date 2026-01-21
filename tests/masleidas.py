import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_most_read_component(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        
        # Localizamos el contenedor (usando clase que es más estable que XPath largo)
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "brick_most-read")))
        
        # Hacemos scroll técnico rápido
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(1) 
        
        # CAPTURA INMEDIATA (Antes de que colapse)
        allure.attach(driver.get_screenshot_as_png(), name="MasLeidas", attachment_type=allure.attachment_type.PNG)
        
        # Validación posterior
        stories = container.find_elements(By.CLASS_NAME, "brick_most-read__story")
        assert len(stories) > 0

    except Exception as e:
        pytest.fail(f"Error crítico de conexión o renderizado: {e}")
