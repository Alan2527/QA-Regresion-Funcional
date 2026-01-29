import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Completa del Reproductor")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30)
    
    # Selectores Actualizados
    xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    # Selector solicitado: El enlace que envuelve el short
    xpath_card_short = "//a[contains(@class, 'shortsList__card')]"

    # 1. BUSCAR Y SCROLLEAR
    with allure.step("1. Buscar y scrollear al Brick de Shorts"):
        driver.get(url_home)
        try:
            # Intentar cerrar el botón de Aceptar (Cookies/Ads)
            btn_aceptar = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        # Esperar al contenedor principal
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", container)
        time.sleep(3) 
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Seccion_Shorts", attachment_type=allure.attachment_type.PNG)

    # 2. CLICK EN EL SHORT (Uso de shortsList__card)
    with allure.step("2. Click en el elemento shortsList__card"):
        try:
            # Esperamos a que la "card" sea clickeable
            short_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card_short)))
            
            # Forzamos scroll al elemento específico por si el contenedor es muy grande
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", short_card)
            time.sleep(1)
            
            # Click vía JavaScript para evitar intercepciones de otros elementos
            driver.execute_script("arguments[0].click();", short_card)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Click_Card", attachment_type=allure.attachment_type.PNG)
            raise Exception(f"No se pudo clickear en la card de Shorts: {e}")

    # 3. VALIDAR REPRODUCTOR VISIBLE
    with allure.step("3. Validar que el reproductor se activó"):
        xpath_player = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player)))
            time.sleep(4) 
            allure.attach(driver.get_screenshot_as_png(), name="Captura_Short_Reproduciendo", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Reproductor_No_Abrio", attachment_type=allure.attachment_type.PNG)
            pytest.fail("El reproductor de Shorts no se mostró tras el click.")

    # 4. PRUEBA DE CONTROLES (MUTE)
    with allure.step("4. Probar Mute en el reproductor"):
        xpath_mute = "//button[contains(@class, 'mute--button')]"
        btn_mute = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_mute)))
        driver.execute_script("arguments[0].click();", btn_mute)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Short_Mute", attachment_type=allure.attachment_type.PNG)

    # 5. CERRAR
    with allure.step("5. Cerrar reproductor"):
        close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'shorts-player__close')]")
        driver.execute_script("arguments[0].click();", close_btn)
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player)))
