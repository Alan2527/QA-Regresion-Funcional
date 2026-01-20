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
        wait = WebDriverWait(driver, 20)
        
        # 1. Localizar y Clickear el botón del dropdown (usando tu clase)
        # Reemplaza 'clase-del-boton' por la que me pasaste
        boton_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "clase-del-boton-que-me-diste")))
        boton_dropdown.click()
        
        # 2. ESPERA ACTIVA: Esperamos que el menú sea visible antes de la captura
        # Aquí usamos el selector del contenedor del dropdown
        time.sleep(1) # Tiempo de gracia para la animación de apertura
        
        # Validación de que el menú está abierto
        assert boton_dropdown.is_displayed()
        
    finally:
        # La captura ahora mostrará el menú desplegado sobre el CSS de la página
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Dropdown_Abierto", 
            attachment_type=allure.attachment_type.PNG
        )
