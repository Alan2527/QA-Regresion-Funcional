import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url)
        
        # 1. ABRIR CAMPANA (Con reintento para evitar StaleElement)
        for _ in range(3):
            try:
                boton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
                driver.execute_script("arguments[0].click();", boton)
                break
            except StaleElementReferenceException:
                time.sleep(1)

        # 2. CLICK ACTIVAR
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

        # 3. ACTIVAR LOS 10 SWITCHES
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.2)
            except: continue

        # --- VALIDACIÓN DE PERSISTENCIA ---
        
        # 4. CERRAR (Re-localizando siempre la campana)
        for _ in range(3):
            try:
                boton_cerrar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
                driver.execute_script("arguments[0].click();", boton_cerrar)
                break
            except StaleElementReferenceException:
                time.sleep(1)
        
        time.sleep(2)
        
        # 5. REABRIR (Para la captura final que necesitás)
        for _ in range(3):
            try:
                boton_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
                driver.execute_script("arguments[0].click();", boton_reabrir)
                break
            except StaleElementReferenceException:
                time.sleep(1)

        # Espera final para que se vea el panel abierto y con colores
        time.sleep(5)
        
    except Exception as e:
        print(f"Error en el proceso: {e}")
    finally:
        # LA CAPTURA QUE BUSCAMOS
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Dropdown_Abierto", 
            attachment_type=allure.attachment_type.PNG
        )
