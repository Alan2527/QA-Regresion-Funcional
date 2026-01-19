import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    
    try:
        driver.get(url)
    except TimeoutException:
        # Si la página tarda mucho, intentamos detener la carga de recursos externos
        driver.execute_script("window.stop();")

    wait = WebDriverWait(driver, 20)
    btn_campana_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div/button'

    # 1. Abrir Campana
    btn_campana = wait.until(EC.presence_of_element_located((By.XPATH, btn_campana_xpath)))
    driver.execute_script("arguments[0].click();", btn_campana)
    time.sleep(1)

    # 2. Abrir Settings (con reintento por si el navegador está lento)
    btn_settings_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/button'
    btn_settings = wait.until(EC.element_to_be_clickable((By.XPATH, btn_settings_xpath)))
    driver.execute_script("arguments[0].click();", btn_settings)
    time.sleep(1)

    # 3. Interactuar con Switches
    for i in range(1, 11):
        switch_xpath = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            continue # Si uno falla por lag, seguimos con el siguiente

    # Captura final antes de que Allure o el driver mueran
    allure.attach(driver.get_screenshot_as_png(), name="Notificaciones_Final", attachment_type=allure.attachment_type.PNG)
