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
    
    # XPaths de estructura y estados
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_card_short = "//a[contains(@class, 'shortsList__card')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    
    # XPaths específicos solicitados
    xpath_link_nota = "//h2[contains(@class, 'shorts-player__description') and contains(@class, 'active')]/a"
    xpath_btn_cerrar = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button'

    # 1. NAVEGACIÓN
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

    # 2. APERTURA
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card_short)))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player_active)))
        time.sleep(4)

    # 3. EL OJO
    with allure.step("3. Validar botón El Ojo"):
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo) 
        time.sleep(1)
        driver.execute_script("arguments[0].click();", btn_ojo) 
        time.sleep(1)

    # 4. NAVEGACIÓN (NEXT / PREV)
    with allure.step("4. Validar Navegación entre Shorts"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'next--button')]"))
        time.sleep(3)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'prev--button')]"))
        time.sleep(3)

    # 5. SHARE Y BOTONES ESPECÍFICOS
    with allure.step("5. Validar Botón Share y sus Redes"):
        xpath_share_principal = "//button[contains(@class, 'share-button')]"
        btn_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_share_principal)))
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(2)

        redes = [
            {"n": "Facebook", "x": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'},
            {"n": "X", "x": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'},
            {"n": "Copiar", "x": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]', "fast": True},
            {"n": "WhatsApp", "x": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]'},
            {"n": "Telegram", "x": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]'}
        ]

        for r in redes:
            btn_r = driver.find_element(By.XPATH, r["x"])
            driver.execute_script("arguments[0].click();", btn_r)
            if r.get("fast"):
                allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{r['n']}_Tooltip", attachment_type=allure.attachment_type.PNG)
            else:
                time.sleep(1)
                allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{r['n']}", attachment_type=allure.attachment_type.PNG)
        
        driver.execute_script("arguments[0].click();", btn_share)

    # 6. MUTE Y 7. FULLSCREEN
    with allure.step("6. Validar Mute"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]"))
    
    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", btn_fs)

    # 8. CLICK EN NOTA
    with allure.step("8. Click en el link de la nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_link_nota)))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="8_En_la_Nota", attachment_type=allure.attachment_type.PNG)

    # 9. VOLVER ATRÁS
    with allure.step("9. Volver atrás"):
        driver.back()
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="9_Vuelta_a_Home", attachment_type=allure.attachment_type.PNG)

    # 10. CERRAR
    with allure.step("10. Cerrar reproductor"):
        btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_btn_cerrar)))
        driver.execute_script("arguments[0].click();", btn_cerrar)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="10_Finalizado", attachment_type=allure.attachment_type.PNG)
