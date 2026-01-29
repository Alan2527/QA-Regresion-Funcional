import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Integral con Bloqueo de Ads y Fallo Estricto")
def test_shorts_player_full_validation(driver):
    # --- BLOQUEO DE ADS A NIVEL RED (Para que no cargue el anuncio de Norton) ---
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            "*googleads*", "*doubleclick*", "*adnxs*", "*titago*", 
            "*amazon-adsystem*", "*smartadserver*", "*taboola*", 
            "*interstitial*", "*outbrain*", "*criteo*"
        ]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 15)
    main_window = driver.current_window_handle

    def force_clean_ads():
        """Elimina manualmente cualquier banner o popup que bloquee la pantalla"""
        driver.execute_script("""
            const elements = document.querySelectorAll('.ad-unit, [id*="google_ads"], .interstitial, #onesignal-slidedown-container, [class*="AppBanner"], [id*="norton"]');
            elements.forEach(el => el.remove());
            document.body.style.overflow = 'auto';
        """)

    # 0. INICIO
    driver.get(url_home)
    force_clean_ads()
    
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

    # 4. BOTÓN SIGUIENTE
    with allure.step("4. Validar botón Siguiente"):
        btn_next = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'next')]")))
        driver.execute_script("arguments[0].click();", btn_next)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="4_Siguiente_Short", attachment_type=allure.attachment_type.PNG)

    # 5. BOTÓN ANTERIOR
    with allure.step("5. Validar botón Anterior"):
        btn_prev = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'prev')]")))
        driver.execute_script("arguments[0].click();", btn_prev)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="5_Anterior_Short", attachment_type=allure.attachment_type.PNG)

    # 6. MUTE / UNMUTE
    with allure.step("6. Validar Mute"):
        btn_mute = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'mute-button')]")))
        driver.execute_script("arguments[0].click();", btn_mute)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute_Activo", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_mute)

    # 7. ABRIR SHARE Y REDES (CON CAMBIO DE VENTANA)
    with allure.step("7. Validar Share y Ventanas de Redes"):
        btn_share = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-button')]")))
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(1)
        
        redes = [
            ("Facebook", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'),
            ("X", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'),
            ("WhatsApp", '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]')
        ]

        for nombre, xpath in redes:
            btn_red = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", btn_red)
            time.sleep(4)
            
            handles = driver.window_handles
            if len(handles) > 1:
                driver.switch_to.window(handles[-1])
                allure.attach(driver.get_screenshot_as_png(), name=f"Captura_Real_{nombre}", attachment_type=allure.attachment_type.PNG)
                driver.close()
                driver.switch_to.window(main_window)
            else:
                pytest.fail(f"ERROR: La red {nombre} no abrió una ventana nueva.")

    # 12. CERRAR SHARE
    with allure.step("12. Cerrar Menú Share"):
        close_share = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/button')))
        driver.execute_script("arguments[0].click();", close_share)

    # 15. IR A LA NOTA
    with allure.step("15. Ir a la Nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.shorts-player__description.active a")))
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(5)
        force_clean_ads()
        allure.attach(driver.get_screenshot_as_png(), name="15_Pagina_Nota", attachment_type=allure.attachment_type.PNG)

    # 16. VOLVER ATRÁS (FORZADO Y SIN BUSQUEDA)
    with allure.step("16. Volver atrás al Home"):
        driver.back() 
        time.sleep(6) # Tiempo extra para que cargue el Home
        force_clean_ads() # LIMPIAR EL ANUNCIO QUE APARECIÓ EN TU CAPTURA
        # Captura directa de lo que hay en pantalla sin buscar elementos
        allure.attach(driver.get_screenshot_as_png(), name="16_Regreso_Home_Captura_Limpia", attachment_type=allure.attachment_type.PNG)

    # 17. CIERRE FINAL
    with allure.step("17. Cerrar componente Short"):
        force_clean_ads()
        # XPath exacto del botón de cierre
        btn_x_final = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button')))
        driver.execute_script("arguments[0].click();", btn_x_final)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="17_Pantalla_Final_Sin_Reproductor", attachment_type=allure.attachment_type.PNG)
