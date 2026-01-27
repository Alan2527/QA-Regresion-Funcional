import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Notificaciones")
@allure.story("Configuración de Preferencias")
def test_configuracion_notificaciones(driver):
    # BLOQUEO DE ADS (Imágenes habilitadas para que rendericen)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "*.googlesyndication.com", "*.doubleclick.net", "*.ads*", 
            "*.adnxs*", "*.analytics*", "*.taboola*"
        ]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # Navegación inicial fuera de pasos o integrada al inicio
    driver.get(url)
    try:
        btn_aceptar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
        driver.execute_script("arguments[0].click();", btn_aceptar)
    except:
        pass

    # 1. ABRIR CAMPANA
    with allure.step("1. Abrir campana"):
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        # Espera de 5 segundos y captura como estaba en tu script original
        time.sleep(5)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Validacion_Inicial", 
            attachment_type=allure.attachment_type.PNG
        )

    # 2. CLICK EN ACTIVÁ LAS NOTIFICACIONES
    with allure.step("2. Click en 'Activá las notificaciones'"):
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

    # 3. ACTIVACIÓN DE LOS 10 SWITCHES
    with allure.step("3. ACTIVACIÓN de los 10 switches"):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        for i in range(1, 11):
            try:
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                span_slider = driver.find_element(By.XPATH, xpath_span)
                driver.execute_script("arguments[0].click();", span_slider)
                time.sleep(0.3)
            except:
                continue
        # Captura de los switches activados
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Switches_Activados", 
            attachment_type=allure.attachment_type.PNG
        )

    # 4. CERRAR
    with allure.step("4. CERRAR"):
        campana_cierre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_cierre)
        time.sleep(3)
        
    # 5. REABRIR
    with allure.step("5. REABRIR"):
        campana_reabrir = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", campana_reabrir)
        
    # 6. VALIDACIÓN POR XPATH ESPECÍFICO
    with allure.step("6. VALIDACIÓN POR XPATH ESPECÍFICO"):
        xpath_especifico = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[2]/div[1]'
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_especifico)))
        # Espera final de 5 segundos para la captura final
        time.sleep(5)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_Notificaciones", 
            attachment_type=allure.attachment_type.PNG
        )
