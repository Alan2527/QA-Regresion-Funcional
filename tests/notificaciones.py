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
        
        # 1. Primer Click en la campana para abrir
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # 2. Click en "Activá las notificaciones" (el botón del modal)
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

        # 3. Activar los 10 switches con tus XPaths exactos
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.3) # Breve pausa entre activaciones
            except:
                continue

        # --- VALIDACIÓN DE PERSISTENCIA ---
        
        # 4. Segundo Click en la campana para CERRAR el dropdown
        driver.execute_script("arguments[0].click();", boton_campana)
        time.sleep(2) # Espera a que la animación de cierre termine
        
        # 5. Tercer Click en la campana para REABRIR y verificar
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # Esperamos a que los elementos del panel vuelvan a estar visibles
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "toggle-switch")))
        time.sleep(2) # Pausa para asegurar que los colores (azul) se rendericen bien
        
    finally:
        # CAPTURA FINAL: Muestra el estado tras cerrar y reabrir
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Persistencia", 
            attachment_type=allure.attachment_type.PNG
        )
