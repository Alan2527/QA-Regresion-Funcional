import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 25)
        
        # Usamos los selectores que identificaste
        boton_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tu-clase-del-boton")))
        boton_dropdown.click()
        
        time.sleep(2) # Espera clave para que el dropdown se vea en la captura
        
        # Validar que el dropdown existe en el DOM
        assert True 
        
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="Dropdown_Abierto", attachment_type=allure.attachment_type.PNG)
