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
        wait = WebDriverWait(driver, 25)
        
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        
        # Centramos el componente para la foto
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2) # Pausa para renderizado
        
        stories = container.find_elements(By.CLASS_NAME, "brick_most-read__story")
        assert len(stories) > 0
        
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="Mas_Leidas_Visible", attachment_type=allure.attachment_type.PNG)
