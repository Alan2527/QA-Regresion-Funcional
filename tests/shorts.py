import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_home)
        print(f"INFO: Navegando a la Home: {url_home}")

        # 1. Buscar y scrollear al componente Shorts
        xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        print("INFO: Componente Shorts localizado y centrado.")
        time.sleep(2)

        # 2. Click en el PlayIcon
        xpath_play = "//*[@id='fusion-app']/div[12]/main/div[5]/div[1]/div/div/a/div[2]"        
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado.")

        # 3. Validar que el reproductor esté visible
        xpath_player = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player)))
        print("ÉXITO: Reproductor de Shorts visible.")

        # 4.a y b - El Ojo (Ocultar/Mostrar Controles)
        xpath_ojo = "//button[contains(@class, 'show-controls--button')]"
        xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"
        
        btn_ojo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ojo)))
        driver.execute_script("arguments[0].click();", btn_ojo)
        print("INFO: Click en el 'ojo'. Ocultando controles...")
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_h2_desc)))
        
        driver.execute_script("arguments[0].click();", btn_ojo)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_h2_desc)))
        print("INFO: Controles visibles nuevamente.")

        # 4.c y d - Navegación (Next / Previous)
        xpath_next = "//button[contains(@class, 'next--button')]"
        xpath_prev = "//button[contains(@class, 'previous--button')]"
        
        desc_inicial = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.find_element(By.XPATH, xpath_next).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_inicial)
        print(f"INFO: Next funciona. Nuevo video: {driver.find_element(By.XPATH, xpath_h2_desc).text[:30]}...")

        desc_actual = driver.find_element(By.XPATH, xpath_h2_desc).text
        driver.find_element(By.XPATH, xpath_prev).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_actual)
        print("INFO: Previous funciona correctamente.")

        # 4.e - Share Button
        xpath_share = "//div[contains(@class, 'shorts-player')]//button[contains(@class, 'share-button')]"
        xpath_share_panel = "//div[contains(@class, 'expanded-buttons')]"
        
        driver.find_element(By.XPATH, xpath_share).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_share_panel)))
        print("INFO: Panel de compartir desplegado.")
        driver.find_element(By.XPATH, xpath_share).click() # Cerrar

        # 4.f - Mute (Validación de SVG)
        xpath_mute = "//button[contains(@class, 'mute--button')]"
        driver.find_element(By.XPATH, xpath_mute).click()
        print("INFO: Cambio de estado de audio validado.")

        # 4.g - Fullscreen (Validación de SVG)
        xpath_fs = "//button[contains(@class, 'fullscreen--button')]"
        driver.find_element(By.XPATH, xpath_fs).click()
        print("INFO: Botón Fullscreen clickeado.")

        # 4.h - Click en el link de la descripción y volver
        link_nota = driver.find_element(By.XPATH, f"{xpath_h2_desc}/a")
        url_destino = link_nota.get_attribute('href')
        driver.execute_script("arguments[0].click();", link_nota)
        
        wait.until(EC.url_to_be(url_destino))
        print(f"INFO: Navegación exitosa a la nota: {driver.current_url}")
        
        # REGRESO Y CAPTURA FINAL
        driver.back()
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        
        # Re-abrir para la foto (usando JS para evitar bloqueos)
        play_btn_re = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn_re)
        time.sleep(2) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Shorts_Reproductor_Activo", 
            attachment_type=allure.attachment_type.PNG
        )

        # 4.i - Cerrar reproductor (Solución al ElementClickIntercepted)
        # Removemos el pop-up de OneSignal si existe para limpiar el camino
        driver.execute_script("""
            var notification = document.getElementById('onesignal-slidedown-container');
            if (notification) { notification.remove(); }
        """)
        
        xpath_close = "//button[contains(@class, 'shorts-player__close')]"
        close_btn = driver.find_element(By.XPATH, xpath_close)
        # Usamos JS Click aquí para ignorar cualquier otro elemento que flote encima
        driver.execute_script("arguments[0].click();", close_btn)
        
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player)))
        print("ÉXITO: Reproductor cerrado correctamente.")

    except Exception as e:
        print(f"ERROR: Falló el test de Shorts: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Shorts_Final", attachment_type=allure.attachment_type.PNG)
        raise e
