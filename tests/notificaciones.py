import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    driver.get(url)
    wait = WebDriverWait(driver, 25)

    # --- SOLUCIÓN AL STALE ELEMENT CON REINTENTO ---
    btn_campana_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div/button'
    
    for _ in range(3): # Intentar hasta 3 veces si el elemento se vuelve 'stale'
        try:
            btn_campana = wait.until(EC.element_to_be_clickable((By.XPATH, btn_campana_xpath)))
            # Usamos un clic por JavaScript para que sea más fulminante y evitar bloqueos
            driver.execute_script("arguments[0].click();", btn_campana)
            break 
        except StaleElementReferenceException:
            time.sleep(1)
            continue

    # 2. Clic en Settings (Xpath proporcionado)
    btn_settings_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/button'
    btn_settings = wait.until(EC.element_to_be_clickable((By.XPATH, btn_settings_xpath)))
    driver.execute_script("arguments[0].click();", btn_settings)

    # 3. Bucle para los 10 switches con Scroll
    for i in range(1, 11):
        switch_xpath = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
        switch_element = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch_element)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", switch_element)

    # 4. Cerrar y Validar
    btn_campana = wait.until(EC.element_to_be_clickable((By.XPATH, btn_campana_xpath)))
    btn_campana.click()
    time.sleep(1)
    btn_campana.click()

    # Captura final para Allure
    allure.attach(driver.get_screenshot_as_png(), name="Panel_Final", attachment_type=allure.attachment_type.PNG)
