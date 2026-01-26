import pytest
import allure
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    
    # Configuramos un tiempo límite para la carga de la página
    driver.set_page_load_timeout(50)
    wait = WebDriverWait(driver, 60)
    
    try:
        try:
            print(f"INFO: Intentando cargar {url_nota}")
            driver.get(url_nota)
        except TimeoutException:
            print("WARN: La página tardó demasiado. Forzando detención y continuando con el test...")
            driver.execute_script("window.stop();")

        # 1. Localizar el iframe con scroll forzado
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        
        # Esperamos a que el iframe esté presente en el DOM
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", trinity_frame)
        time.sleep(3) 

        driver.switch_to.frame(trinity_frame)
        print("INFO: Dentro del iframe de Trinity.")

        # 2. Play y validación de interfaz
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)

        # Esperamos a que el cronómetro avance (Prueba de vida)
        xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div'
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != "00:00")
        
        # Respiro para que los elementos visuales carguen
        time.sleep(3)

        # CAPTURA DE PANTALLA (Debería mostrar pausa y UI completa)
        allure.attach(driver.get_screenshot_as_png(), name="Trinity_Full_UI", attachment_type=allure.attachment_type.PNG)

        # 3. Validar componentes de texto
        assert "Escuchando artículo" in driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span').text
        assert "Powered by" in driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[3]/div[1]/div').text

        # 4. Validar Forward (+10s)
        t_antes = driver.find_element(By.XPATH, xpath_timer).text
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        driver.execute_script("arguments[0].click();", btn_forward)
        
        # Esperamos cambio de tiempo
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != t_antes)
        print(f"INFO: Forward ok. Tiempo: {driver.find_element(By.XPATH, xpath_timer).text}")

        # 5. Validar Menú de Velocidad
        btn_speed = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button')
        btn_speed.click()
        time.sleep(1)
        # Tomamos captura del menú abierto si es posible
        allure.attach(driver.get_screenshot_as_png(), name="Trinity_Speed_Menu")

        print("ÉXITO: Test de reproductor completado con todas las piezas.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Final_Debug")
        raise e
    finally:
        driver.switch_to.default_content()
