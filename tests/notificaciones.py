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
        wait = WebDriverWait(driver, 30)
        
        # Forzar el click por JS si el botón está tapado por ads
        # Cambia 'CLASE_BOTON' por la clase real de la campana/dropdown
        boton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "CLASE_BOTON")))
        driver.execute_script("arguments[0].click();", boton)
        
        time.sleep(1.5) # Espera mínima para que el dropdown se dibuje
        
        # CAPTURA INMEDIATA
        allure.attach(driver.get_screenshot_as_png(), name="Dropdown_Notif", attachment_type=allure.attachment_type.PNG)
        
    except Exception as e:
        # Si falla el click, saca captura del error para ver qué lo tapa
        allure.attach(driver.get_screenshot_as_png(), name="Error_Notif", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"No se pudo abrir el dropdown: {e}")
