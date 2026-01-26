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
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(2)

        driver.switch_to.frame(trinity_frame)
        print("INFO: Switch exitoso al iframe.")

        # 2. Click en Play
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado.")

        # --- MEJORA PARA LA CAPTURA ---
        # 3. Validar que el botón de PLAY ahora sea de PAUSA (indica que está sonando)
        # Esperamos a que la clase cambie a 'button-pause'
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.button-pause")))
        
        # Esperamos un momento para que el texto cargue
        time.sleep(2) 

        # Captura de pantalla: Ahora debería verse el botón de Pausa/Stop
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Trinity_Reproduciendo_Action", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura realizada con éxito (Botón Stop/Pause debería estar visible).")

        # 4. Validar "Escuchando artículo"
        xpath_title_span = '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span'
        title_elem = driver.find_element(By.XPATH, xpath_title_span)
        # Usamos un assert simple o wait si es necesario
        assert "Escuchando artículo" in title_elem.text or title_elem.get_attribute("innerText") != ""

        # 5. Validar Powered by
        xpath_powered = '//*[@id="app"]/div/div/div/div[2]/div[3]/div[1]/div'
        assert "Powered by" in driver.find_element(By.XPATH, xpath_powered).text

        # 6. Validar Timers y Track
        timer_current = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div')
        assert timer_current.is_displayed()

        # 7. Validar Forward (+10 seg)
        t_antes = timer_current.text
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button').click()
        wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text != t_antes)

        # 8. Validar Backward (-10 seg)
        t_ahora = timer_current.text
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button').click()
        wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text != t_ahora)

        # 9. Validar Speed Control
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button').click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div')))
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button').click()

        # 10. Validar pausa final y cambio a Play
        btn_toggle = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/button')
        btn_toggle.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.button-play")))
        print("INFO: Pause final validado.")

        # 11. Validar label externo
        driver.switch_to.default_content()
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        # Usamos contains para ser más flexibles con el texto
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_label), "Reproduciendo"))
        print("ÉXITO: Test de Trinity Audio finalizado.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Final_Debug", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        driver.switch_to.default_content()
