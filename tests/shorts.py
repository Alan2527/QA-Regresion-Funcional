import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Estricta con XPaths de Usuario y Bloqueo de Ads")
def test_shorts_player_user_paths(driver):
    # --- BLOQUEO DE ADS (CRÍTICO PARA QUE NO FALLE EL RETURN) ---
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*googleads*", "*doubleclick*", "*adnxs*", "*titago*", "*amazon-adsystem*", "*taboola*", "*interstitial*", "*norton*", "*2mdn*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 15)
    main_window = driver.current_window_handle

    # DICCIONARIO DE SELECTORES DEL USUARIO (NO TOCAR)
    SELECTORS = {
        "brick": (By.CLASS_NAME, "aspect_ratio__container"),
        "play": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/a'),
        "ocultar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[1]/button'),
        "mostrar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div/button'),
        "siguiente": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[2]/button[2]'),
        "anterior": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[2]/button[1]'),
        "mute": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/button[1]'),
        "fullscreen": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/button[2]'),
        "share_open": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div/div/button'),
        "share_close": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/button'),
        "h2_nota": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[1]/div[3]/div[1]/h2'),
        "close_player": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button'),
        # Redes
        "facebook": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'),
        "x": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'),
        "copiar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]'),
        "whatsapp": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]'),
        "telegram": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]')
    }

    def clean_ui():
        """Elimina basura que pueda tapar clicks"""
        driver.execute_script("""
            const elements = document.querySelectorAll('.ad-unit, [id*="google_ads"], .interstitial, #onesignal-slidedown-container, [class*="AppBanner"]');
            elements.forEach(el => el.remove());
        """)

    # 0. INICIO
    driver.get(url_home)
    with allure.step("0. Cerrar OneSignal y Preparar"):
        try:
            # Botón OneSignal
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onesignal-slidedown-cancel-button"]'))).click()
        except:
            pass
        clean_ui()

    # 1. SCROLL AL BRICK
    with allure.step("1. Buscar Brick Videolab"):
        # Usamos CLASS_NAME exacto como pediste
        brick = wait.until(EC.presence_of_element_located(SELECTORS["brick"]))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", brick)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="1_Brick_Encontrado", attachment_type=allure.attachment_type.PNG)

    # 2. PLAY
    with allure.step("2. Click Play"):
        wait.until(EC.element_to_be_clickable(SELECTORS["play"])).click()
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="2_Video_Reproduciendo", attachment_type=allure.attachment_type.PNG)

    # 3. OCULTAR / MOSTRAR
    with allure.step("3. Controles Ocultar/Mostrar"):
        wait.until(EC.element_to_be_clickable(SELECTORS["ocultar"])).click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="3_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        wait.until(EC.element_to_be_clickable(SELECTORS["mostrar"])).click() # Volver a mostrar
        time.sleep(1)

    # 4. SIGUIENTE
    with allure.step("4. Video Siguiente"):
        wait.until(EC.element_to_be_clickable(SELECTORS["siguiente"])).click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente", attachment_type=allure.attachment_type.PNG)

    # 5. ANTERIOR
    with allure.step("5. Video Anterior"):
        wait.until(EC.element_to_be_clickable(SELECTORS["anterior"])).click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="5_Anterior", attachment_type=allure.attachment_type.PNG)

    # 6. MUTE / UNMUTE
    with allure.step("6. Sonido"):
        btn_mute = wait.until(EC.element_to_be_clickable(SELECTORS["mute"]))
        btn_mute.click() # Activar
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="6_Sonido_Activado", attachment_type=allure.attachment_type.PNG)
        btn_mute.click() # Desactivar

    # 7. FULLSCREEN (NUEVO PASO)
    with allure.step("7. Fullscreen"):
        btn_full = wait.until(EC.element_to_be_clickable(SELECTORS["fullscreen"]))
        btn_full.click() # Activar
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="7_Pantalla_Completa", attachment_type=allure.attachment_type.PNG)
        btn_full.click() # Salir
        time.sleep(2)

    # 8. SHARE Y REDES (SUBPASOS)
    with allure.step("8. Menú Compartir"):
        wait.until(EC.element_to_be_clickable(SELECTORS["share_open"])).click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="8_Menu_Share_Abierto", attachment_type=allure.attachment_type.PNG)

        # Subpasos Redes
        redes_data = [
            ("Facebook", SELECTORS["facebook"]),
            ("X", SELECTORS["x"]),
            ("Copiar", SELECTORS["copiar"]),
            ("WhatsApp", SELECTORS["whatsapp"]),
            ("Telegram", SELECTORS["telegram"])
        ]

        for nombre, selector in redes_data:
            with allure.step(f"   > Red Social: {nombre}"):
                btn = wait.until(EC.element_to_be_clickable(selector))
                btn.click()
                
                if nombre == "Copiar":
                    # CAPTURA INMEDIATA PARA EL TOOLTIP
                    allure.attach(driver.get_screenshot_as_png(), name=f"8_{nombre}_Tooltip", attachment_type=allure.attachment_type.PNG)
                else:
                    time.sleep(4)
                    handles = driver.window_handles
                    if len(handles) > 1:
                        driver.switch_to.window(handles[-1])
                        allure.attach(driver.get_screenshot_as_png(), name=f"8_Ventana_{nombre}", attachment_type=allure.attachment_type.PNG)
                        driver.close()
                        driver.switch_to.window(main_window)
                    else:
                        pytest.fail(f"Fallo al abrir ventana de {nombre}")

        # Cerrar Share
        wait.until(EC.element_to_be_clickable(SELECTORS["share_close"])).click()

    # 9. IR A LA NOTA
    with allure.step("9. Navegar a la Nota"):
        # Concatenamos /a al H2 para clickear el enlace
        xpath_h2 = SELECTORS["h2_nota"][1]
        link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_h2 + "/a")))
        driver.execute_script("arguments[0].click();", link)
        
        time.sleep(5)
        clean_ui()
        allure.attach(driver.get_screenshot_as_png(), name="9_Pagina_Nota", attachment_type=allure.attachment_type.PNG)

    # 10. VOLVER ATRAS
    with allure.step("10. Volver al Home"):
        driver.back()
        time.sleep(5)
        clean_ui() # LIMPIEZA CRITICA AQUI
        allure.attach(driver.get_screenshot_as_png(), name="10_Home_Retorno", attachment_type=allure.attachment_type.PNG)

# 11. CERRAR REPRODUCTOR (LÓGICA INTELIGENTE)
    with allure.step("11. Cerrar Short (Si corresponde)"):
        clean_ui()
        try:
            # Intentamos encontrar el botón
            btn_close = wait.until(EC.element_to_be_clickable(SELECTORS["close_player"]))
            btn_close.click()
            time.sleep(1)
            msg = "11_Cerrado_Manualmente"
        except:
            # Si no se encuentra (TimeoutException), asumimos que ya estamos en Home
            # NO fallamos el test, solo informamos en la captura
            msg = "11_Player_No_Estaba_Presente_(Ya_en_Home)"
        
        # Tomamos la captura sea cual sea el resultado para validar estado final
        allure.attach(driver.get_screenshot_as_png(), name=msg, attachment_type=allure.attachment_type.PNG)
