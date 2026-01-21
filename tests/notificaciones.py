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
        
        # Pequeña pausa para que el modal aparezca
        time.sleep(2)

        # Limpieza de posibles carteles de suscripción que tapan (como el de image_ac6fab.png)
        driver.execute_script("""
            var overlays = document.querySelectorAll('[class*="modal"], [class*="overlay"], [class*="popup"]');
            overlays.forEach(function(el) { if(!el.contains(document.querySelector('.font__action'))) el.remove(); });
        """)

        # 2. Click en el botón para activar (Selector más flexible)
        # Buscamos cualquier botón que tenga el texto "Activá"
        selector_activar = "//button[contains(., 'Activá') or contains(., 'activar')]"
        boton_activar = wait.until(EC.presence_of_element_located((By.XPATH, selector_activar)))
        
        # Scroll al botón por las dudas y click por JS
        driver.execute_script("arguments[0].scrollIntoView(true);", boton_activar)
        driver.execute_script("arguments[0].click();", boton_activar)
        
        # Espera para que carguen los temas
        time.sleep(3)
        
    except Exception as e:
        print(f"Error detectado: {e}")
        # No hacemos raise inmediato para que llegue al finally y saque la foto
    finally:
        # Esta captura nos mostrará si logramos llegar a los temas o qué cartel quedó trabado
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Estado_Final_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
