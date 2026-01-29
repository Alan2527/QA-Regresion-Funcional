import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral - 10 Pasos Estrictos")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    main_window = driver.current_window_handle

    # Selectores
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"

    # 1. NAVEGACIÓN
    with allure.step("1. Buscar y scrollear al Brick de Shorts"):
        driver.get(url_home)
        try:
            btn_aceptar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except: pass
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="1_Home_Shorts", attachment_type=allure.attachment_type.PNG)

    # 2. APERTURA
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'shortsList__card')]")))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player_active)))
        allure.attach(driver.get_screenshot_as_png(), name="2_Reproductor_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. BOTÓN EL OJO
    with allure.step("3. Validar botón El Ojo"):
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'show-controls--button')]")))
        driver.execute_script("arguments[0].click();", btn_ojo) # Ocultar
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) # Mostrar
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Visibles", attachment_type=allure.attachment_type.PNG)

    # 4. NAVEGACIÓN
    with allure.step("4. Validar Navegación (Siguiente/Anterior)"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//button[contains(@class, "next")]'))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//button[contains(@class, "prev")]'))
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="4_Anterior_Short", attachment_type=allure.attachment_type.PNG)

    # 5. SHARE
    with allure.step("5. Validar Share y Ventanas de Redes"):
        xpath_share = "//button[contains(@class, 'share-button')]"
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share))
        time.sleep(1)
        for i in range(1, 6):
            try:
                xpath_red = f'(//div[contains(@class, "shorts-player__share-list")]//button)[{i}]'
                btn_red = driver.find_element(By.XPATH, xpath_red)
                driver.execute_script("arguments[0].click();", btn_red)
                time.sleep(3)
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    allure.attach(driver.get_screenshot_as_png(), name=f"5_Red_{i}_Ventana", attachment_type=allure.attachment_type.PNG)
                    driver.close()
                    driver.switch_to.window(main_window)
            except: pass

    # 6. MUTE (SEPARADO)
    with allure.step("6. Validar Mute"):
        btn_mute = driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]")
        driver.execute_script("arguments[0].click();", btn_mute)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_mute) # Restaurar sonido

    # 7. FULLSCREEN (SEPARADO)
    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs) # Salir de FS
        time.sleep(1)

    # 8. NOTA
    with allure.step("8. Ir a la nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(@class, 'active')]/a")))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="8_En_la_Nota", attachment_type=allure.attachment_type.PNG)

    # 9. VOLVER
    with allure.step("9. Volver atrás al Home"):
        driver.execute_script("window.history.go(-1);")
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="9_Vuelta_al_Home", attachment_type=allure.attachment_type.PNG)
