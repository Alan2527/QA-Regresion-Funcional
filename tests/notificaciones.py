import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Configuración")
@allure.story("Panel de Notificaciones")
def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/" # O la URL específica que uses para el test
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        
        # Simula aquí los pasos para abrir tus notificaciones
        # Por ejemplo, clic en el botón de campana o configuración:
        # campana = wait.until(EC.element_to_be_clickable((By.ID, "notif-icon")))
        # campana.click()
        
        # Tu validación principal
        assert True 
        
    finally:
        # Captura de pantalla final para el reporte de Allure
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
