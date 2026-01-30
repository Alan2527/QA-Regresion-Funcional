import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Videolab")
@allure.story("Validación Estricta con XPaths y Clases del Usuario")
def test_videolab_player_user_paths(driver):
    # --- 1. BLOQUEO DE ADS Y CONFIGURACIÓN ---
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*googleads*", "*doubleclick*", "*adnxs*", "*titago*", "*amazon-adsystem*", "*taboola*", "*interstitial*", "*norton*", "*2mdn*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 15)
    main_window = driver.current_window_handle

    # DICCIONARIO DE SELECTORES (COPIADOS EXACTAMENTE DE TU LISTA)
    SELECTORS = {
        "brick": (By.CLASS_NAME, "relative.width_full.videolab.desktop"),
        "play": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[2]/div[2]/div/div/div/div[1]/div/a'),
        "ocultar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[1]/button'),
        "mostrar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div/button'),
        "siguiente": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[2]/button[2]'),
        "anterior": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[2]/button[1]'),
        "share_btn": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div/div/button'),
        "facebook": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[2]/button[1]'),
        "x": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[2]/button[2]'),
        "copiar": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[2]/button[3]'),
        "whatsapp": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[2]/button[4]'),
        "telegram": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[2]/button[5]'),
        "cerrar_share": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/div[3]/div[1]/div/button'),
        "sonido": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/button[1]'),
        "fullscreen": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[2]/button[2]'),
        "h2_nota": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/div[1]/div[3]/div[1]/h2'),
        "cerrar_reproductor": (By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[18]/div/div[3]/button')
    }

    def clean_ui():
        driver.execute_script("""
            const elements = document.querySelectorAll('.ad-unit, [id*="google_ads"], .interstitial, #onesignal-slidedown-container');
            elements.forEach(el => el.remove());
        """)

    # 1. INICIO Y POPUP
    driver.get(url_home)
    with allure.step("1. Cerrar Popup y Bloquear Ads"):
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onesignal-slidedown-cancel-button"]'))).click()
        except: pass
        clean_ui()

    # 2. BRICK VIDEOLAB
    with allure.step("2. Buscar y Centrar Videolab"):
        # Usamos el selector de clase exacto que pasaste
        brick = wait.until(EC.presence_of_element_located(SELECTORS["brick"]))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", brick)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="2_Brick_Videolab", attachment_type=allure.attachment_type.PNG)

    # 3. PLAY
    with allure.step("3. Click Play Primer Video"):
        wait.until(EC.element_to_be_clickable(SELECTORS["play"])).click()
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="3_Video_Reproduciendo", attachment_type=allure.attachment_type.PNG)

    # 4 y 5. OCULTAR / MOSTRAR
    with allure.step("4-5. Controles Ocultar/Mostrar"):
        wait.until(EC.element_to_be_clickable(SELECTORS["ocultar"])).click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="4_Controles_Ocultos", attachment_type=allure.attachment_type.PNG)
        wait.until(EC.element_to_be_clickable(SELECTORS["mostrar"])).click()
        time.sleep(1)

    # 6. SIGUIENTE
    with allure.step("6. Siguiente Video"):
        wait.until(EC.element_to_be_clickable(SELECTORS["siguiente"])).click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="6_Siguiente", attachment_type=allure.attachment_type.PNG)

    # 7. ANTERIOR
    with allure.step("7. Anterior Video"):
        wait.until(EC.element_to_be_clickable(SELECTORS["anterior"])).click()
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="7_Anterior", attachment_type=allure.attachment_type.PNG)

    # 8-14. SHARE Y REDES (SUBPASOS)
    with allure.step("8. Menú Compartir"):
        wait.until(EC.element_to_be_clickable(SELECTORS["share_btn"])).click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="8_Menu_Share", attachment_type=allure.attachment_type.PNG)

        redes = [
            ("Facebook", SELECTORS["facebook"]),
            ("X", SELECTORS["x"]),
            ("Copiar", SELECTORS["copiar"]),
            ("WhatsApp", SELECTORS["whatsapp"]),
            ("Telegram", SELECTORS["telegram"])
        ]

        for nombre, xpath in redes:
            with allure.step(f"   > {nombre}"):
                btn = wait.until(EC.element_to_be_clickable(xpath))
                btn.click()
                if nombre == "Copiar":
                    allure.attach(driver.get_screenshot_as_png(), name="11_Tooltip_Copiado", attachment_type=allure.attachment_type.PNG)
                else:
                    time.sleep(4)
                    handles = driver.window_handles
                    if len(handles) > 1:
                        driver.switch_to.window(handles[-1])
                        allure.attach(driver.get_screenshot_as_png(), name=f"Ventana_{nombre}", attachment_type=allure.attachment_type.PNG)
                        driver.close()
                        driver.switch_to.window(main_window)
        
        wait.until(EC.element_to_be_clickable(SELECTORS["cerrar_share"])).click()

    # 15. SONIDO
    with allure.step("15. Activar Sonido"):
        wait.until(EC.element_to_be_clickable(SELECTORS["sonido"])).click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="15_Sonido_Activado", attachment_type=allure.attachment_type.PNG)

    # 16-17. FULLSCREEN
    with allure.step("16-17. Fullscreen"):
        btn_fs = wait.until(EC.element_to_be_clickable(SELECTORS["fullscreen"]))
        btn_fs.click() # Agrandar
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="16_Fullscreen_Activo", attachment_type=allure.attachment_type.PNG)
        btn_fs.click() # Achicar
        time.sleep(2)

    # 18. NAVEGAR A NOTA
    with allure.step("18. Navegar a la Nota"):
        xpath_h2 = SELECTORS["h2_nota"][1]
        link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_h2 + "/a")))
        driver.execute_script("arguments[0].click();", link)
        time.sleep(5)
        clean_ui()
        allure.attach(driver.get_screenshot_as_png(), name="18_Pagina_Nota", attachment_type=allure.attachment_type.PNG)

    # 19. VOLVER ATRÁS Y CIERRE INTELIGENTE
    with allure.step("19. Volver atrás y Cerrar"):
        driver.back()
        time.sleep(5)
        clean_ui()
        try:
            # Intento cerrar el reproductor si quedó abierto
            btn_close = wait.until(EC.element_to_be_clickable(SELECTORS["cerrar_reproductor"]))
            btn_close.click()
            time.sleep(1)
            status = "Cerrado_Manualmente"
        except:
            status = "Ya_estaba_en_Home"
        
        allure.attach(driver.get_screenshot_as_png(), name=f"19_Final_{status}", attachment_type=allure.attachment_type.PNG)
