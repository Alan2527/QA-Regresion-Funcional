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
        wait = WebDriverWait(driver, 20)
        
        # Selector que me pasaste
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        
        # HACER SCROLL: Centra el componente en la pantalla
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(1.5) # Pausa para que el scroll termine y la captura sea estable
        
        stories = container.find_elements(By.CLASS_NAME, "brick_most-read__story")
        assert len(stories) > 0, "No se encontraron noticias en el ranking"
        
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_MasLeidas_Visible", 
            attachment_type=allure.attachment_type.PNG
        )
