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
    
    # Selectores estables (Relativos)
    xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    # XPath corregido: busca el icono de play dentro del contenedor de shorts
    xpath_play = "//div[contains(@class, 'shorts-player__icon')]" 

    # 1. BUSCAR Y SCROLLEAR
    with allure.step("1. Buscar y scrollear al Brick 1 Short"):
        driver.get(url_home)
        try:
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(4) 
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Brick_1_Short", attachment_type=allure.attachment_type.PNG)

    # 2. CLICK EN PLAY ICON (Fix de XPath)
    with allure.step("2. Click en el PlayIcon"):
        try:
            # Usamos el selector de clase en lugar del ID absoluto
            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
            driver.execute_script("arguments[0].click();", play_btn)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="Error_Encontrar_PlayIcon", attachment_type=allure.attachment_type.PNG)
            raise e

    # 3. VALIDAR REPRODUCTOR VISIBLE
    with allure.step("3. Validar que el reproductor esté visible"):
        xpath_player = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player)))
        time.sleep(5) 
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Reproductor_Activo", attachment_type=allure.attachment_type.PNG)

    # 4. EL OJO (Controles)
    with allure.step("4. El Ojo (Ocultar/Mostrar Controles)"):
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo) 
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) 

    # 5. NAVEGACIÓN
    with allure.step("5. Navegación (Next / Previous)"):
        xpath_next = "//button[contains(@class, 'next--button')]"
        xpath_prev = "//button[contains(@class, 'previous--button')]"
        
        desc_inicial = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.find_element(By.XPATH, xpath_next).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_inicial)
        time.sleep(3) 
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Next_Short", attachment_type=allure.attachment_type.PNG)

    # 6. SHARE
    with allure.step("6. Share Button"):
        xpath_share = "//button[contains(@class, 'share-button')]"
        driver.find_element(By.XPATH, xpath_share).click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Menu_Share_Shorts", attachment_type=allure.attachment_type.PNG)
        driver.find_element(By.XPATH, xpath_share).click() 

    # 7. MUTE Y FULLSCREEN (Simplificado)
    with allure.step("7. Mute y Fullscreen"):
        driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]").click()
        driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]").click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Mute_Fullscreen", attachment_type=allure.attachment_type.PNG)
        driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]").click()

    # 8. CERRAR REPRODUCTOR
    with allure.step("8. Cerrar reproductor"):
        # Limpieza de posibles popups que tapen el botón X
        driver.execute_script("var n = document.getElementById('onesignal-slidedown-container'); if(n) n.remove();")
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'shorts-player__close')]")))
        driver.execute_script("arguments[0].click();", close_btn)
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player)))
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Shorts_Cerrado", attachment_type=allure.attachment_type.PNG)
