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
        print(f"INFO: Navegando a {url}")
        
        # 1. Abrir campana
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        print("INFO: Click en la campanita principal realizado.")
        
        # 2. Click en "Activá las notificaciones"
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)
        print("INFO: Click en el botón 'Activá las notificaciones' del dropdown realizado.")

        # 3. ACTIVACIÓN de los 10 switches
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        print("INFO: Iniciando la activación de los 10 switches de temas...")
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                print(f"   - Switch #{i} clickeado.")
                time.sleep(0.3)
            except:
                print(f"   - ERROR: No se pudo clickear el switch #{i}.")
                continue

        # --- CICLO DE VALIDACIÓN ---
        
        # 4. CERRAR
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        print("INFO: Cerrando el dropdown para validar persistencia.")
        time.sleep(3)
        
        # 5. REABRIR
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        print("INFO: Reabriendo el dropdown de notificaciones.")
        
        # 6. VALIDACIÓN POR XPATH ESPECÍFICO
        xpath_especifico = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[2]/div[1]'
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_especifico)))
        print("ÉXITO: Las notificaciones son visibles en el dropdown.")
        
        # Espera final para asegurar que la captura tome los switches en azul
        time.sleep(5)
        
    except Exception as e:
        print(f"ERROR DURANTE EL TEST: {str(e)}")
        raise e
        
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
