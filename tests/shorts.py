import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral: Controles, Redes y Navegación")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    main_window = driver.current_window_handle
    
    # XPaths base
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    xpath_btn_cerrar = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button'

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
    with allure.step("3. Validar botón El Ojo (Mostrar/Ocultar)"):
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo) # Oculta
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) # Muestra
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Visibles", attachment_type=allure.attachment_type.PNG)

    # 4. NAVEGACIÓN (NEXT / PREV)
    with allure.step("4. Validar Navegación entre Shorts"):
        btn_next = driver.find_element(By.XPATH, "//button[contains(@class, 'next--button')]")
        driver.execute_script("arguments[0].click();", btn_next)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)
        try:
            btn_prev = driver.find_element(By.XPATH, "//button[contains(@class, 'prev--button')]")
            driver.execute_script("arguments[0].click();", btn_prev)
            time.sleep(1)
        except: pass
        allure.attach(driver.get_screenshot_as_png(), name="4_Regreso_Anterior", attachment_type=allure.attachment_type.PNG)

    # 5. SHARE Y CAPTURAS DE REDES
    with allure.step("5. Validar Botón Share y Ventanas de Redes"):
        xpath_share_principal = "//button[contains(@class, 'share-button')]"
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share_principal))
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="5_Menu_Share_Abierto", attachment_type=allure.attachment_type.PNG)

        for i in range(1, 6):
            xpath_red = f'//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[{i}]'
            try:
                btn_red = driver.find_element(By.XPATH, xpath_red)
                driver.execute_script("arguments[0].click();", btn_red)
                time.sleep(4) # Esperar a que cargue la ventana
                
                windows = driver.window_handles
                if len(windows) > 1:
                    driver.switch_to.window(windows[1])
                    allure.attach(driver.get_screenshot_as_png(), name=f"5_Ventana_Red_Social_{i}", attachment_type=allure.attachment_type.PNG)
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    allure.attach(driver.get_screenshot_as_png(), name=f"5_Red_{i}_Sin_Nueva_Ventana", attachment_type=allure.attachment_type.PNG)
            except: pass
        
        # Cerrar el panel de share si quedó abierto
        try: driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_share_principal))
        except: pass

    # 6. MUTE
    with allure.step("6. Validar Mute"):
        btn_mute = driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]")
        driver.execute_script("arguments[0].click();", btn_mute)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_Activo", attachment_type=allure.attachment_type.PNG)

    # 7. FULLSCREEN
    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen_In", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(1)

    # 8. CLICK EN NOTA
    with allure.step("8. Click en el link de la nota"):
        xpath_link_nota = "//h2[contains(@class, 'shorts-player__description') and contains(@class, 'active')]/a"
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_link_nota)))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="8_Pagina_de_la_Nota", attachment_type=allure.attachment_type.PNG)

    # 9. VOLVER Y LIMPIEZA DE ADS
    with allure.step("9. Volver atrás y limpiar bloqueos"):
        driver.back()
        time.sleep(5)
        # Script para borrar cualquier Ad o Overlay que bloquee el botón de cerrar
        driver.execute_script("""
            const blockers = document.querySelectorAll('iframe, .adsbygoogle, [id*="google_ads"], [class*="interstitial"], [class*="overlay"]');
            blockers.forEach(el => el.remove());
            document.body.style.overflow = 'auto';
        """)
        allure.attach(driver.get_screenshot_as_png(), name="9_Vuelta_a_Home", attachment_type=allure.attachment_type.PNG)

    # 10. CERRAR
    with allure.step("10. Cerrar reproductor"):
        btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_btn_cerrar)))
        driver.execute_script("arguments[0].click();", btn_cerrar)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="10_Final_Test", attachment_type=allure.attachment_type.PNG)
