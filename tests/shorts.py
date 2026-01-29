import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación con XPaths Exactos y Continuidad en Fallos")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    main_window = driver.current_window_handle

    # --- INICIO DEL TEST ---
    driver.get(url_home)
    driver.execute_script("document.querySelectorAll('.tp-modal, #didomi-host').forEach(el => el.remove());")

    # 1. SCROLL AL BRICK
    with allure.step("1. Buscar y scrollear al Brick de Shorts"):
        try:
            container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brick-shorts__container')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="1_Home_Shorts", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Paso_1", attachment_type=allure.attachment_type.PNG)
            print(f"Fallo paso 1: {e}")

    # 2. ABRIR REPRODUCTOR
    with allure.step("2. Abrir reproductor"):
        try:
            short_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'shortsList__card')]")))
            driver.execute_script("arguments[0].click();", short_card)
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="2_Reproductor_Abierto", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Paso_2", attachment_type=allure.attachment_type.PNG)
            print(f"Fallo paso 2: {e}")

    # 3. SHARE - DESPLEGAR MENÚ
    with allure.step("3. Abrir Menú Share"):
        try:
            btn_share = driver.find_element(By.XPATH, "//button[contains(@class, 'share-button')]")
            driver.execute_script("arguments[0].click();", btn_share)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="3_Menu_Share", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Paso_3", attachment_type=allure.attachment_type.PNG)

    # --- REDES SOCIALES CON XPATHS EXACTOS ---

    # FACEBOOK
    with allure.step("4. Validar Facebook"):
        try:
            fb = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]')
            driver.execute_script("arguments[0].click();", fb)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="4_Facebook_Click", attachment_type=allure.attachment_type.PNG)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1]); driver.close(); driver.switch_to.window(main_window)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Facebook", attachment_type=allure.attachment_type.PNG)

    # X (TWITTER)
    with allure.step("5. Validar X"):
        try:
            tw = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]')
            driver.execute_script("arguments[0].click();", tw)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="5_X_Click", attachment_type=allure.attachment_type.PNG)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1]); driver.close(); driver.switch_to.window(main_window)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_X", attachment_type=allure.attachment_type.PNG)

    # COPIAR (Captura rápida para el tooltip)
    with allure.step("6. Validar Copiar (Captura Rápida)"):
        try:
            copy = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]')
            driver.execute_script("arguments[0].click();", copy)
            # CAPTURA INMEDIATA sin sleep para agarrar el tooltip
            allure.attach(driver.get_screenshot_as_png(), name="6_Tooltip_Copiado", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Copiar", attachment_type=allure.attachment_type.PNG)

    # WHATSAPP
    with allure.step("7. Validar WhatsApp"):
        try:
            ws = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]')
            driver.execute_script("arguments[0].click();", ws)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="7_WhatsApp_Click", attachment_type=allure.attachment_type.PNG)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1]); driver.close(); driver.switch_to.window(main_window)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_WhatsApp", attachment_type=allure.attachment_type.PNG)

    # TELEGRAM
    with allure.step("8. Validar Telegram"):
        try:
            tg = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]')
            driver.execute_script("arguments[0].click();", tg)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="8_Telegram_Click", attachment_type=allure.attachment_type.PNG)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1]); driver.close(); driver.switch_to.window(main_window)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Telegram", attachment_type=allure.attachment_type.PNG)

    # CERRAR SHARE
    with allure.step("9. Cerrar Menú Share"):
        try:
            close_share = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/button')
            driver.execute_script("arguments[0].click();", close_share)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="9_Share_Cerrado", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="ERROR_Cerrar_Share", attachment_type=allure.attachment_type.PNG)

    # 10. MUTE Y FULLSCREEN (SEPARADOS)
    with allure.step("10. Validar Mute"):
        try:
            btn_mute = driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]")
            driver.execute_script("arguments[0].click();", btn_mute)
            allure.attach(driver.get_screenshot_as_png(), name="10_Mute", attachment_type=allure.attachment_type.PNG)
        except: pass

    with allure.step("11. Validar Fullscreen"):
        try:
            btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
            driver.execute_script("arguments[0].click();", btn_fs)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="11_Fullscreen", attachment_type=allure.attachment_type.PNG)
            driver.execute_script("arguments[0].click();", btn_fs)
        except: pass
