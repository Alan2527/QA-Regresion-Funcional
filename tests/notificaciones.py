import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    # Volvemos a la URL que no falla
    url_nota = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-historia/"
    wait = WebDriverWait(driver, 20)
    
    driver.get(url_nota)
    
    # XPath original (el que funcionaba en tu entorno)
    xpath_campana = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/button'
    
    boton_campana = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_campana)))
    boton_campana.click()
    
    # Captura de evidencia
    allure.attach(driver.get_screenshot_as_png(), name="Notificaciones_OK", attachment_type=allure.attachment_type.PNG)
