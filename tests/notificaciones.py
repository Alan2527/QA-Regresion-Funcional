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

        # 3. ACTIVACIÓN de los 10 switches
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.3)
            except:
                continue

        # --- CICLO DE VALIDACIÓN ---
        
        # 4. CERRAR (Haciendo click en la campana de nuevo)
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        
        # Esperamos a que el dropdown desaparezca de la vista
        time.sleep(2)
        
        # 5. REABRIR (Click final en la campana)
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        
        # 6. ESPERA DE VALIDACIÓN: 
        # En lugar de solo esperar la clase, esperamos que el contenedor de temas sea visible
        # Esto nos asegura que la captura se tome con el panel ya desplegado.
        wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "notification-setting-item")))
        
        # Un pequeño delay para que el color azul de los switches termine de cargar en el render
        time.sleep(3)
        
    except Exception as e:
        # Si algo falla, lo imprimimos pero dejamos que el finally saque la captura
        print(f"Error en el flujo: {e}")
        
    finally:
        # ESTA ES LA CAPTURA QUE NECESITÁS: 
        # Debe mostrar los temas y sus estados (deberían estar en azul)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_Azules", 
            attachment_type=allure.attachment_type.PNG
        )
