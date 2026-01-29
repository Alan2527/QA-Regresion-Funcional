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
    
    # Selectores de Clase (Más estables que los IDs dinámicos)
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_card_short = "//a[contains(@class, 'shortsList__card')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"

    # 1. BUSCAR Y SCROLLEAR AL BRICK
    with allure.step("1. Buscar y scrollear al Brick de Shorts"):
        driver.get(url_home)
        try:
            btn_aceptar = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="1_Seccion_Shorts", attachment_type=allure.attachment_type.PNG)

    # 2. CLICK EN LA CARD (Entrar al reproductor)
    with allure.step("2. Click en shortsList__card para abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card_short)))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player_active)))
        time.sleep(4) # Espera para que cargue el primer video
        allure.attach(driver.get_screenshot_as_png(), name="2_Reproductor_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. EL OJO (Ocultar/Mostrar Controles)
    with allure.step("3. Validar botón El Ojo"):
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo) 
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_h2_desc)))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) 
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_h2_desc)))

    # 4. NAVEGACIÓN (Next / Previous)
    with allure.step("4. Validar Navegación (Next/Prev)"):
        xpath_next = "//button[contains(@class, 'next--button')]"
        xpath_prev = "//button[contains(@class, 'previous--button')]"
        
        desc_inicial = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_next))
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_inicial)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="4a_Siguiente_Video", attachment_type=allure.attachment_type.PNG)

        desc_actual = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_prev))
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_actual)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4b_Video_Anterior", attachment_type=allure.attachment_type.PNG)

    # 5. SHARE BUTTON
    with allure.step("5. Validar Botón Share"):
        xpath_share = "//button[contains(@class, 'share-button')]"
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="5_Panel_Share", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share))

    # 6. MUTE Y FULLSCREEN
    with allure.step("6. Validar Mute y Fullscreen"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]"))
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]"))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_y_Fullscreen", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]"))

    # 7. CLICK EN LINK DE DESCRIPCIÓN Y VOLVER
    with allure.step("7. Click en link de la nota y volver"):
        link_nota = driver.find_element(By.XPATH, f"{xpath_h2_desc}/a")
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="7_Pagina_de_la_Nota", attachment_type=allure.attachment_type.PNG)
        driver.back()
        # Re-confirmamos que volvimos a los shorts
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))

    # 8. CERRAR REPRODUCTOR
    with allure.step("8. Cerrar reproductor (X)"):
        # Limpieza por si el banner de OneSignal molesta
        driver.execute_script("var n = document.getElementById('onesignal-slidedown-container'); if(n) n.remove();")
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'shorts-player__close')]")))
        driver.execute_script("arguments[0].click();", close_btn)
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player_active)))
        allure.attach(driver.get_screenshot_as_png(), name="8_Home_TN_Final", attachment_type=allure.attachment_type.PNG)
