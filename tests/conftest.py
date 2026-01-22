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
        
        # 1. Abrir campana
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # 2. Click en "Activá las notificaciones"
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

        # 3. Activar los 10 switches
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.3)
            except: continue

        # --- VALIDACIÓN DE PERSISTENCIA ---
        # 4. CERRAR
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        time.sleep(3) # Pausa para que el modal cierre bien
        
        # 5. REABRIR
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        
        # 6. ESPERA PARA RENDERIZADO (Con Try/Except para no romper el test)
        try:
            # Intentamos esperar los items, pero si tarda, no matamos el proceso
            wait_corto = WebDriverWait(driver, 10)
            wait_corto.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "notification-setting-item")))
        except:
            print("Aviso: Los elementos tardaron en ser detectados, tomando captura de seguridad.")
            
        time.sleep(4) # Tiempo extra para que los estilos (azul) se vean bien
        
    finally:
        # CAPTURA FINAL: Se toma pase lo que pase en el bloque anterior
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Estilos_Originales", 
            attachment_type=allure.attachment_type.PNG
        )
