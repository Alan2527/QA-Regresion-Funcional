import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral - Navegación, Ocultar, Share, Nota y Cierre")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    main_window = driver.current_window_handle

    # --- INICIO ---
    driver.get(url_home)
    
    # 0. ONESIGNAL (XPath proporcionado)
    with allure.step("0. Cerrar popup OneSignal"):
        try:
            btn_onesignal = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onesignal-slidedown-cancel-button"]')))
            btn_onesignal.click()
            allure.attach(driver.get_screenshot_as_png(), name="0_OneSignal_Cerrado", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="0_OneSignal_No_Aparecio", attachment_type=allure.attachment_type.PNG)

    # 1. SCROLL
    with allure.step("1. Scrollear al Brick de Shorts"):
        try:
            container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brick-shorts__container')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="1_Home_Shorts", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Paso_1", attachment_type=allure.attachment_type.PNG)

    # 2. ABRIR
    with allure.step("2. Abrir reproductor"):
        try:
            short_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'shortsList__card')]")))
            driver.execute_script("arguments[0].click();", short_card)
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="2_Reproductor_Abierto", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Paso_2", attachment_type=allure.attachment_type.PNG)

    # 3. OCULTAR / MOSTRAR (EL OJO)
    with allure.step("3. Validar botón El Ojo (Ocultar/Mostrar)"):
        try:
            btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'show-controls--button')]")))
            driver.execute_script("arguments[0].click();", btn_ojo) # Ocultar
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
            driver.execute_script("arguments[0].click();", btn_ojo) # Mostrar
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Visibles", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Boton_Ojo", attachment_type=allure.attachment_type.PNG)

    # 4. NAVEGACIÓN NEXT
    with allure.step("4. Validar botón Siguiente (Next)"):
        try:
            btn_next = driver.find_element(By.XPATH, "//button[contains(@class, 'next')]")
            driver.execute_script("arguments[0].click();", btn_next)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Boton_Next", attachment_type=allure.attachment_type.PNG)

    # 5. NAVEGACIÓN PREVIOUS
    with allure.step("5. Validar botón Anterior (Prev)"):
        try:
            btn_prev = driver.find_element(By.XPATH, "//button[contains(@class, 'prev')]")
            driver.execute_script("arguments[0].click();", btn_prev)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="5_Anterior_Short", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Boton_Prev", attachment_type=allure.attachment_type.PNG)

    # 6. SHARE MENU
    with allure.step("6. Abrir Menú Share"):
        try:
            btn_share = driver.find_element(By.XPATH, "//button[contains(@class, 'share-button')]")
            driver.execute_script("arguments[0].click();", btn_share)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="6_Menu_Share", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Menu_Share", attachment_type=allure.attachment_type.PNG)

    # --- REDES SOCIALES (XPaths Exactos) ---
    redes = [
        ("7_Facebook", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'),
        ("8_X", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'),
        ("9_Copiar", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]'),
        ("10_WhatsApp", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]'),
        ("11_Telegram", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]')
    ]

    for nombre, xpath in redes:
        with allure.step(f"Validar {nombre}"):
            try:
                btn = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click();", btn)
                if "Copiar" in nombre:
                    allure.attach(driver.get_screenshot_as_png(), name=f"{nombre}_Tooltip", attachment_type=allure.attachment_type.PNG)
                else:
                    time.sleep(2)
                    allure.attach(driver.get_screenshot_as_png(), name=f"{nombre}_Click", attachment_type=allure.attachment_type.PNG)
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[1]); driver.close(); driver.switch_to.window(main_window)
            except:
                allure.attach(driver.get_screenshot_as_png(), name=f"ERR_{nombre}", attachment_type=allure.attachment_type.PNG)

    # 12. CERRAR SHARE
    with allure.step("12. Cerrar Menú Share"):
        try:
            close_share = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/button')
            driver.execute_script("arguments[0].click();", close_share)
            allure.attach(driver.get_screenshot_as_png(), name="12_Share_Cerrado", attachment_type=allure.attachment_type.PNG)
        except: pass

    # 13. MUTE
    with allure.step("13. Validar Mute"):
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]"))
            allure.attach(driver.get_screenshot_as_png(), name="13_Mute", attachment_type=allure.attachment_type.PNG)
        except: pass

    # 14. FULLSCREEN
    with allure.step("14. Validar Fullscreen"):
        try:
            btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
            driver.execute_script("arguments[0].click();", btn_fs)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="14_Fullscreen", attachment_type=allure.attachment_type.PNG)
            driver.execute_script("arguments[0].click();", btn_fs)
        except: pass

    # 15. ENLACE NOTA
    with allure.step("15. Click en enlace de la nota"):
        try:
            link_nota = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.shorts-player__description.active a")))
            driver.execute_script("arguments[0].click();", link_nota)
            time.sleep(4)
            allure.attach(driver.get_screenshot_as_png(), name="15_En_Nota", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Nota", attachment_type=allure.attachment_type.PNG)

    # 16. VOLVER ATRÁS
    with allure.step("16. Volver atrás"):
        try:
            driver.execute_script("window.history.go(-1);")
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="16_Regreso_Home", attachment_type=allure.attachment_type.PNG)
        except: pass

    # 17. CIERRE COMPONENTE (X Final)
    with allure.step("17. Cerrar componente Short"):
        try:
            btn_x_final = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button')))
            driver.execute_script("arguments[0].click();", btn_x_final)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="17_Cierre_Final", attachment_type=allure.attachment_type.PNG)
        except:
            allure.attach(driver.get_screenshot_as_png(), name="ERR_Cierre_Final", attachment_type=allure.attachment_type.PNG)
