import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral - 10 Pasos Estrictos")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    main_window = driver.current_window_handle
    
    # XPaths
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    xpath_btn_cerrar = "//button[contains(@class, 'shorts-player__close')]"

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

    # 4. NAVEGACIÓN NEXT/PREV
    with allure.step("4. Validar Navegación entre Shorts"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'next--button')]"))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'prev--button')]"))
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="4_Anterior_Short", attachment_type=allure.attachment_type.PNG)

    # 5. REDES SOCIALES (CON CAPTURA DE VENTANAS)
    with allure.step("5. Validar Share y Ventanas de Redes"):
        xpath_share = "//button[contains(@class, 'share-button')]"
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share))
        time.sleep(1)
        
        for i in range(1, 6):
            xpath_red = f'(//div[contains(@class, "shorts-player__share-list")]//button)[{i}]'
            try:
                btn_red = driver.find_element(By.XPATH, xpath_red)
                driver.execute_script("arguments[0].click();", btn_red)
                time.sleep(4)
                
                handles = driver.window_handles
                if len(handles) > 1:
                    driver.switch_to.window(handles[1])
                    allure.attach(driver.get_screenshot_as_png(), name=f"5_Red_{i}_Ventana", attachment_type=allure.attachment_type.PNG)
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    allure.attach(driver.get_screenshot_as_png(), name=f"5_Red_{i}_No_Abre_Ventana", attachment_type=allure.attachment_type.PNG)
            except: pass
        
        # Cerrar menú share
        try: driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share))
        except: pass

    # 6. MUTE (PASO SEPARADO)
    with allure.step("6. Validar Mute"):
        btn_mute = driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]")
        driver.execute_script("arguments[0].click();", btn_mute)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_mute) # Desactivar

    # 7. FULLSCREEN (PASO SEPARADO)
    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs) # Salir
        time.sleep(1)

    # 8. NOTA
    with allure.step("8. Ir a la nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(@class, 'active')]/a")))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="8_En_la_Nota", attachment_type=allure.attachment_type.PNG)

    # 9. VOLVER ATRÁS
    with allure.step("9. Volver atrás al Home"):
        driver.execute_script("window.history.go(-1);")
        time.sleep(5)
        # RE-SINCRO: Buscamos el contenedor de nuevo para evitar el NoSuchElementException
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        allure.attach(driver.get_screenshot_as_png(), name="9_Vuelta_al_Home", attachment_type=allure.attachment_type.PNG)

    # 10. CERRAR
    with allure.step("10. Cerrar reproductor"):
        # Buscamos el botón de nuevo porque el DOM se refrescó al volver
        btn_cerrar = wait.until(EC.presence_of_element_located((By.XPATH, xpath_btn_cerrar)))
        driver.execute_script("arguments[0].click();", btn_cerrar)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="10_Final_Cerrado", attachment_type=allure.attachment_type.PNG)
