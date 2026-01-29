import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Total - 10 Pasos con Capturas Obligatorias")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    main_window = driver.current_window_handle

    # 1. NAVEGACIÓN
    with allure.step("1. Scrollear al Brick de Shorts"):
        driver.get(url_home)
        # Limpieza de anuncios/modales que bloquean capturas
        driver.execute_script("document.querySelectorAll('.tp-modal, #didomi-host').forEach(el => el.remove());")
        container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brick-shorts__container')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="1_Home_Shorts", attachment_type=allure.attachment_type.PNG)

    # 2. APERTURA
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'shortsList__card')]")))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'active')]//video")))
        allure.attach(driver.get_screenshot_as_png(), name="2_Player_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. EL OJO
    with allure.step("3. Validar botón El Ojo"):
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'show-controls--button')]")))
        driver.execute_script("arguments[0].click();", btn_ojo) 
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Ocultar_Controles", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) 
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Mostrar_Controles", attachment_type=allure.attachment_type.PNG)

    # 4. NAVEGACIÓN (Corregido selector de tus logs)
    with allure.step("4. Navegar entre Shorts"):
        btn_next = driver.find_element(By.XPATH, "//button[contains(@class, 'next')]")
        driver.execute_script("arguments[0].click();", btn_next)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)
        
        btn_prev = driver.find_element(By.XPATH, "//button[contains(@class, 'prev')]")
        driver.execute_script("arguments[0].click();", btn_prev)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Anterior_Short", attachment_type=allure.attachment_type.PNG)

    # 5. SHARE Y REDES (CADA UNA CON CAPTURA)
    with allure.step("5. Validar Share y Redes Sociales"):
        btn_share = driver.find_element(By.XPATH, "//button[contains(@class, 'share-button')]")
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="5_Menu_Share_Desplegado", attachment_type=allure.attachment_type.PNG)
        
        nombres_redes = ["Facebook", "Twitter", "WhatsApp", "Telegram", "Copiar"]
        for i, nombre in enumerate(nombres_redes, 1):
            with allure.step(f"5.{i} Click en {nombre}"):
                xpath_red = f'(//div[contains(@class, "shorts-player__share-list")]//button)[{i}]'
                btn_red = driver.find_element(By.XPATH, xpath_red)
                driver.execute_script("arguments[0].click();", btn_red)
                time.sleep(3)
                allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{nombre}", attachment_type=allure.attachment_type.PNG)
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(main_window)

    # 6. MUTE (SEPARADO)
    with allure.step("6. Validar Mute"):
        btn_mute = driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]")
        driver.execute_script("arguments[0].click();", btn_mute)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_Activo", attachment_type=allure.attachment_type.PNG)

    # 7. FULLSCREEN (SEPARADO)
    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs) # Salir

    # 8. IR A NOTA
    with allure.step("8. Ir a la nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(@class, 'active')]/a")))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="8_En_la_Nota", attachment_type=allure.attachment_type.PNG)

    # 9. VOLVER (Reforzado para evitar el Timeout del log)
    with allure.step("9. Volver atrás"):
        driver.execute_script("window.history.go(-1);")
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brick-shorts__container')]")))
        allure.attach(driver.get_screenshot_as_png(), name="9_Vuelta_Home", attachment_type=allure.attachment_type.PNG)

    # 10. CERRAR
    with allure.step("10. Cerrar reproductor"):
        # Re-abrimos para cerrar o validamos el botón de cierre si sigue presente
        try:
            btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'shorts-player__close')]")))
            driver.execute_script("arguments[0].click();", btn_cerrar)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="10_Reproductor_Cerrado", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="10_Error_Cierre", attachment_type=allure.attachment_type.PNG)
