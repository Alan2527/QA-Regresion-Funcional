import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("https://tn.com.ar/")
    
    try:
        # 1. Abrir campana
        boton_campana = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/button')))
        boton_campana.click()
        print("INFO: Se hizo clic en la campana de notificaciones.")

        # 2. Click en Activar (si aparece)
        try:
            boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Activá')]")))
            boton_activar.click()
            print("INFO: Se presionó el botón 'Activá'.")
        except:
            print("INFO: El botón 'Activá' no fue necesario o ya estaba activo.")

        # 3. Activar los switches
        for i in range(1, 6): # Probamos con los primeros 5 para el ejemplo
            xpath_switch = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
            switch = driver.find_element(By.XPATH, xpath_switch)
            driver.execute_script("arguments[0].click();", switch)
            print(f"PASO: Switch {i} activado correctamente.")

    except Exception as e:
        print(f"ERROR: Falló la interacción con notificaciones: {e}")
        pytest.fail(f"Test fallido: {e}")
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="Notificaciones_Final", attachment_type=allure.attachment_type.PNG)
