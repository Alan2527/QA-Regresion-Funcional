import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Completa del Reproductor")
def test_shorts_player_full_validation(driver):
    # BLOQUEO DE ADS (Imágenes habilitadas para que no se vea roto)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": ["*.googlesyndication.com", "*.doubleclick.net", "*.ads*", "*.adnxs*", "*.taboola*"]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # 1. BUSCAR Y SCROLLEAR
    with allure.step("1. Buscar y scrollear al Brick 1 Short"):
        driver.get(url_home)
        # Cierre de popup inicial para limpiar la vista
        try:
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(4) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Brick_1_Short", 
            attachment_type=allure.attachment_type.PNG
        )

    # 2. CLICK EN PLAY ICON
    with allure.step("2. Click en el PlayIcon"):
        xpath_play = "//*[@id='fusion-app']/div[12]/main/div[5]/div[1]/div/div/a/div[2]"        
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn)

    # 3. VALIDAR REPRODUCTOR VISIBLE
    with allure.step("3. Validar que el reproductor esté visible"):
        xpath_player = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player)))
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Reproductor_Activo", 
            attachment_type=allure.attachment_type.PNG
        )

    # 4. EL OJO (OCULTAR/MOSTRAR)
    with allure.step("4.a y b - El Ojo (Ocultar/Mostrar Controles)"):
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"
        
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo) # Ocultar
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_h2_desc)))

        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Ocultar", 
            attachment_type=allure.attachment_type.PNG
        )
        
        driver.execute_script("arguments[0].click();", btn_ojo) # Mostrar
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_h2_desc)))


    # 5. NAVEGACIÓN (NEXT / PREVIOUS)
    with allure.step("5.c y d - Navegación (Next / Previous)"):
        xpath_next = "//button[contains(@class, 'next--button')]"
        xpath_prev = "//button[contains(@class, 'previous--button')]"
        
        desc_inicial = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.find_element(By.XPATH, xpath_next).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_inicial)

        desc_actual = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.find_element(By.XPATH, xpath_prev).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_actual)
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Siguiente_Short", 
            attachment_type=allure.attachment_type.PNG
        )

    # 6. SHARE BUTTON
    with allure.step("6.e - Share Button"):
        xpath_share = "//div[contains(@class, 'shorts-player')]//button[contains(@class, 'share-button')]"
        xpath_share_panel = "//div[contains(@class, 'expanded-buttons')]"
        
        driver.find_element(By.XPATH, xpath_share).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_share_panel)))
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Share", 
            attachment_type=allure.attachment_type.PNG
        )
        
        driver.find_element(By.XPATH, xpath_share).click() # Cerrar

    # 7. MUTE Y FULLSCREEN
    with allure.step("7.f y g - Mute y Fullscreen"):
        xpath_mute = "//button[contains(@class, 'mute--button')]"
        xpath_fs = "//button[contains(@class, 'fullscreen--button')]"
        driver.find_element(By.XPATH, xpath_mute).click()
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Mute", 
            attachment_type=allure.attachment_type.PNG
        )
        driver.find_element(By.XPATH, xpath_fs).click()
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Fs", 
            attachment_type=allure.attachment_type.PNG
        )

    # 8. LINK DESCRIPCIÓN Y VOLVER
    with allure.step("8.h - Click en el link de la descripción y volver"):
        link_nota = driver.find_element(By.XPATH, f"{xpath_h2_desc}/a")
        url_destino = link_nota.get_attribute('href')
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Nota_Short", 
            attachment_type=allure.attachment_type.PNG
        )
        
        wait.until(EC.url_to_be(url_destino))
        
        # REGRESO Y CAPTURA FINAL (Tal cual tu script)
        driver.back()
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        
        # Re-abrir para la foto
        play_btn_re = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn_re)
        time.sleep(5) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Shorts_Reproductor_Activo", 
            attachment_type=allure.attachment_type.PNG
        )

    # 9. CERRAR REPRODUCTOR
    with allure.step("9.i - Cerrar reproductor"):
        # Limpieza de OneSignal
        driver.execute_script("""
            var notification = document.getElementById('onesignal-slidedown-container');
            if (notification) { notification.remove(); }
        """)
        
        xpath_close = "//button[contains(@class, 'shorts-player__close')]"
        close_btn = driver.find_element(By.XPATH, xpath_close)
        driver.execute_script("arguments[0].click();", close_btn)
        
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player)))
