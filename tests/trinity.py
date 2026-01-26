import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get(url_nota)
        print(f"INFO: Navegando a la nota: {url_nota}")

        # 1. Localizar el iframe de Trinity
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        
        # Esperar a que el contenedor exista y scrollear
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", trinity_frame)
        time.sleep(2) # Tiempo para que el iframe cargue su contenido interno

        # Cambiar el contexto al iframe
        driver.switch_to.frame(trinity_frame)
        print("INFO: Switch exitoso al iframe de Trinity Audio.")

        # 2. Click en Play (Usamos JS para evitar que cualquier overlay invisible moleste)
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado.")

        # 3. Sincronización Crítica para la Captura
        # Esperamos que aparezca el título para saber que el reproductor ya cargó los datos
        xpath_title_span = '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_title_span), "Escuchando artículo"))
        
        # Pausa de seguridad para que termine la animación de expansión
        time.sleep(1.5)

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Trinity_Reproduciendo", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura de Trinity Audio adjuntada con contenido visible.")

        # 4. Validar Powered by y enlace
        xpath_powered = '//*[@id="app"]/div/div/div/div[2]/div[3]/div[1]/div'
        powered_div = driver.find_element(By.XPATH, xpath_powered)
        assert "Powered by" in powered_div.text
        link_trinity = powered_div.find_element(By.TAG_NAME, "a").get_attribute("href")
        assert "trinityaudio.ai" in link_trinity

        # 5. Validar timers y track
        timer_current = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div')
        timer_total = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[3]/div')
        track_bar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[2]/div/div')
        assert timer_current.is_displayed() and timer_total.is_displayed() and track_bar.is_displayed()

        # 6. Validar Forward (+10 seg)
        t_antes = timer_current.text
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button').click()
        # Esperamos a que el texto del timer cambie tras el click
        wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text != t_antes)
        print(f"INFO: Forward ok. Tiempo: {timer_current.text}")

        # 7. Validar Backward (-10 seg)
        t_ahora = timer_current.text
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button').click()
        wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text != t_ahora)
        print("INFO: Backward ok.")

        # 8. Validar Speed Control
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button').click()
        container_speed = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div')))
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button').click()
        print("INFO: Control de velocidad validado.")

        # 9. Validar Pause y cambio de clase
        btn_toggle = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/button')
        btn_toggle.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-play")))
        print("INFO: Pause validado.")

        # 10. Salir del iframe para validar el label externo
        driver.switch_to.default_content()
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        label_elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath_label)))
        assert "Reproduciendo..." in label_elem.text
        print("ÉXITO: Test de Trinity Audio completado al 100%.")

    except Exception as e:
        print(f"ERROR: Falló Trinity: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Trinity_Capture", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        # Siempre volver al contenido principal para no romper otros tests
        driver.switch_to.default_content()
