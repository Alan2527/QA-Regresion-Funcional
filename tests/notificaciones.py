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

        # 3. Esperar a que cargue la lista de temas
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notification-setting-item")))
        
        # --- NUEVO: ACTIVACIÓN DE TODOS LOS TEMAS ---
        # Buscamos todos los elementos de configuración
        temas = driver.find_elements(By.CLASS_NAME, "notification-setting-item")
        
        for tema in temas:
            try:
                # Buscamos el switch (input o span) dentro de cada fila y le damos click
                # Usualmente es un click en la fila misma o en el componente toggle
                driver.execute_script("arguments[0].click();", tema)
            except:
                continue # Si alguno falla, seguimos con el siguiente
        
        # Pausa para que el navegador procese los cambios visuales (color azul/verde)
        time.sleep(3)
        
    except Exception as e:
        print(f"Error durante la activación: {e}")
    finally:
        # La captura ahora debería mostrar los switches con color de "Activo"
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Temas_ACTIVADOS", 
            attachment_type=allure.attachment_type.PNG
        )
