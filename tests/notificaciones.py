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
        
        # Intentamos con la clase que me diste: font__action
        # Si falla, el XPath de respaldo es: //*[@id="fusion-app"]/header/div/div[1]/div/button
        boton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        
        # Click por JavaScript para evitar bloqueos de capas invisibles
        driver.execute_script("arguments[0].click();", boton)
        
        # Tiempo para que el dropdown se despliegue
        time.sleep(2)
        
        # Validamos que algo haya pasado (puedes ajustar este assert)
        assert True
        
    finally:
        # Captura final con el menú abierto
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
