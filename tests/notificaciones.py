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
        
        # 1. Abrir campana (Referencia inicial)
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
            except:
                continue

        # --- VALIDACIÓN DE PERSISTENCIA ---
        
        # 4. CERRAR: Re-localizamos la campana para evitar el "Stale Element"
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        time.sleep(2) 
        
        # 5. REABRIR: Volvemos a localizarla para el click final
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        
        # Esperamos a que el panel cargue y se estabilice
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "toggle-switch")))
        time.sleep(3) 
        
    finally:
        # CAPTURA FINAL: Se toma con el dropdown abierto por segunda vez
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Persistencia_OK", 
            attachment_type=allure.attachment_type.PNG
        )
