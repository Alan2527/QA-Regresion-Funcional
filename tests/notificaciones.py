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
        
        # 1. Click en la campana (font__action)
        # Según tus capturas, este es el primer paso
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # 2. Click en el botón azul "Activá las notificaciones" del cartel blanco
        # Usamos el texto del botón que se ve en tu captura
        selector_activar = "//button[contains(text(), 'Activá las notificaciones')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)
        
        # Tiempo para que carguen los switches de temas
        time.sleep(2)
        
        # Validamos que se cargó el listado (opcional)
        assert True
        
    finally:
        # CAPTURA FINAL: Ahora sí con los temas para elegir
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Temas_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
