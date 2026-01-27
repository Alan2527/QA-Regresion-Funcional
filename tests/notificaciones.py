import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Notificaciones")
@allure.story("Configuración de Preferencias")
def test_configuracion_notificaciones(driver):
    # BLOQUEO DE ADS E IMÁGENES (Para optimizar y evitar distracciones)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "*.googlesyndication.com", "*.doubleclick.net", "*.ads*", 
            "*.image*", "*.jpg", "*.png", "*.gif", "*.jpeg", "*.webp"
        ]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN (Sin captura)
    with allure.step("1. Navegación y cierre de popup inicial"):
        driver.get(url)
        try:
            # Cerramos el popup de 'Aceptar' si aparece para que no bloquee la campanita
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

    # 2. ABRIR CAMPANA (Sin captura)
    with allure.step("2. Abrir menú de notificaciones"):
        # Localizamos y clickeamos la campanita
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # Click en "Activá las notificaciones"
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

    # 3. ACTIVACIÓN DE SWITCHES (Con captura)
    with allure.step("3. Activación de los 10 switches de temas"):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.3)
            except:
                continue
        
        # Captura después de activar todos los switches
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Switches_Activados", 
            attachment_type=allure.attachment_type.PNG
        )

    # 4. CICLO DE VALIDACIÓN (Con captura final)
    with allure.step("4. Validación de persistencia"):
        # Cerrar
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        time.sleep(2)
        
        # Reabrir
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        
        # Validar visibilidad por XPath
        xpath_especifico = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[2]/div[1]'
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_especifico)))
        
        time.sleep(2)
        # Captura final del estado del dropdown reabierto
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Validacion_Persistencia_Final", 
            attachment_type=allure.attachment_type.PNG
        )
