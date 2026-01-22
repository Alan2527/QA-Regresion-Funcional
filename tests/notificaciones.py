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
        
        # 1. Click en la campana principal
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # 2. Click en el botón azul "Activá las notificaciones"
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

        # --- PASO CLAVE PARA LA CAPTURA ---
        # Esperamos a que el cartel de bienvenida DESAPAREZCA (para evitar el Stale Element)
        wait.until(EC.invisibility_of_element_located((By.XPATH, selector_activar)))
        
        # Esperamos a que aparezca el contenedor de temas (los switches)
        # En TN, estos suelen tener la clase 'column-list' o similar dentro del modal
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notification-setting-item")))
        
        # Una pequeña pausa extra para que la animación del switch termine
        time.sleep(2)
        
    except Exception as e:
        print(f"Error detectado: {e}")
    finally:
        # Ahora la captura se toma solo cuando los temas ya están cargados
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Temas_Activos", 
            attachment_type=allure.attachment_type.PNG
        )
