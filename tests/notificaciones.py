import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    url_nota = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_nota)
        print("INFO: Iniciando prueba de notificaciones")

        # 1. Selector Robusto: Buscamos el botón que tenga la clase de la campana
        # Esto ignora si hay anuncios arriba o abajo.
        xpath_campana = "//button[contains(@class, 'notification-bell') or contains(@class, 'bell')]"
        boton_campana = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_campana)))
        
        # Usamos JS para el click por si hay un modal invisible
        driver.execute_script("arguments[0].click();", boton_campana)
        print("INFO: Se abrió el panel de notificaciones.")

        # 2. Validar que el panel se desplegó buscando el texto 'Activá'
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Activá')]")))
        print("ÉXITO: El panel de alertas es visible.")

    except Exception as e:
        print(f"ERROR: No se pudo interactuar con la campana: {e}")
        pytest.fail(f"Fallo en Notificaciones: {e}")
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="Notificaciones_Final", attachment_type=allure.attachment_type.PNG)
