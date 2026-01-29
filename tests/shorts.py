import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral con Capturas de Ventanas Externas")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    main_window = driver.current_window_handle

    # --- INICIO ---
    driver.get(url_home)
    
    # 0. ONESIGNAL
    with allure.step("0. Cerrar popup OneSignal"):
        try:
            btn_onesignal = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onesignal-slidedown-cancel-button"]')))
            btn_onesignal.click()
        except:
            pass # Si no aparece, no es error crítico

    # 1. SCROLL AL BRICK
    with allure.step("1. Scrollear al Brick de Shorts"):
        container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brick-shorts__container')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="1_Home_Shorts", attachment_type=allure.attachment_type.PNG)

    # 2. ABRIR REPRODUCTOR
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'shortsList__card')]")))
        driver.execute_script("arguments[0].click();", short_card)
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="2_Reproductor_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. EL OJO (OCULTAR/MOSTRAR)
    with allure.step("3. Validar botón El Ojo"):
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'show-controls--button')]")))
        driver.execute_script("arguments[0].click();", btn_ojo) # Ocultar
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_ojo) # Mostrar
        time.sleep(1)

    # 4. NEXT / 5. PREVIOUS
    for step_num, direction, xpath in [("4", "Siguiente", "next"), ("5", "Anterior", "prev")]:
        with allure.step(f"{step_num}. Validar botón {direction}"):
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, '{xpath}')]")))
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name=f"{step_num}_{direction}_Short", attachment_type=allure.attachment_type.PNG)

    # 6. ABRIR SHARE
    with allure.step("6. Abrir Menú Share"):
        btn_share = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-button')]")))
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="6_Menu_Share", attachment_type=allure.attachment_type.PNG)

    # --- REDES SOCIALES CON CAMBIO DE VENTANA ---
    redes = [
        ("7_Facebook", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'),
        ("8_X", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'),
        ("9_Copiar", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]'),
        ("10_WhatsApp", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]'),
        ("11_Telegram", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]')
    ]

    for nombre, xpath in redes:
        with allure.step(f"Validar {nombre}"):
            btn = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", btn)
            
            if "Copiar" in nombre:
                time.sleep(1)
                allure.attach(driver.get_screenshot_as_png(), name=f"{nombre}_Tooltip", attachment_type=allure.attachment_type.PNG)
            else:
                time.sleep(5) # Tiempo para que cargue la ventana nueva
                handles = driver.window_handles
                if len(handles) > 1:
                    driver.switch_to.window(handles[-1])
                    allure.attach(driver.get_screenshot_as_png(), name=f"Captura_REAL_{nombre}", attachment_type=allure.attachment_type.PNG)
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    allure.attach(driver.get_screenshot_as_png(), name=f"ERROR_{nombre}_No_Abrio_Ventana", attachment_type=allure.attachment_type.PNG)
                    pytest.fail(f"La red social {nombre} no abrió una ventana nueva.")

    # 12. CERRAR SHARE
    with allure.step("12. Cerrar Menú Share"):
        close_share = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/button')
        driver.execute_script("arguments[0].click();", close_share)

    # 15. CLICK EN NOTA
    with allure.step("15. Ir a la Nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.shorts-player__description.active a")))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="15_Pagina_Nota", attachment_type=allure.attachment_type.PNG)

    # 16. VOLVER ATRÁS (SIN BUSCAR COMPONENTES)
    with allure.step("16. Volver atrás al Home"):
        driver.back() # Comando nativo de volver
        time.sleep(5)
        # Captura directa del Home sin buscar nada más
        allure.attach(driver.get_screenshot_as_png(), name="16_Regreso_Home_Exitoso", attachment_type=allure.attachment_type.PNG)

    # 17. CIERRE FINAL
    with allure.step("17. Cerrar componente Short"):
        # Solo intentamos cerrar si el reproductor sigue ahí (por si el 'back' lo cerró)
        try:
            btn_x_final = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button')))
            driver.execute_script("arguments[0].click();", btn_x_final)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="17_Pantalla_Final", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="17_Short_Ya_Estaba_Cerrado", attachment_type=allure.attachment_type.PNG)
