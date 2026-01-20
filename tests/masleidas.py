import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_most_read_component(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Localizar el componente
        xpath_principal = "//aside[contains(@class, 'brick_most-read')]"
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        
        # 2. Mover la vista al componente (ayuda a que la captura no pese tanto)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(1) # Breve pausa para que el renderizado se estabilice

        # 3. Validaciones básicas
        stories = container.find_elements(By.CSS_SELECTOR, "article, .brick_most-read__story")
        assert len(stories) > 0, "No se encontraron noticias"

        # 4. LA CAPTURA (Ahora debería funcionar)
        # Usamos una técnica de captura de elemento específico para que sea más liviana
        allure.attach(
            container.screenshot_as_png, 
            name="Componente_Mas_Leidas", 
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:
        # Si falla, intentamos una captura de emergencia de toda la página
        allure.attach(driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Fallo en el componente: {e}")
