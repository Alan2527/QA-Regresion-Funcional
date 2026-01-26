import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 60)
    
    try:
        driver.get(url_nota)
        print("INFO: Navegando a la nota.")

        # 1. Entrar al Iframe
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(2)
        driver.switch_to.frame(trinity_frame)

        # 2. Click en Play e inicio de reproducción
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)

        # 3. SINCRONIZACIÓN CRÍTICA PARA CAPTURA Y UI
        # Esperamos que el timer se mueva de 00:00. Esto garantiza que el audio suena 
        # y que el botón visualmente YA cambió a PAUSA/STOP.
        xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div'
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != "00:00")
        time.sleep(2) # Respiro para renderizado de íconos

        allure.attach(
            driver.get_screenshot_as_png(),
            name="Evidencia_UI_Completa_Reproduciendo",
            attachment_type=allure.attachment_type.PNG
        )

        # 4. VALIDACIONES DE COMPONENTES DE INTERFAZ
        # Título "Escuchando artículo"
        xpath_title = '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span'
        assert "Escuchando artículo" in driver.find_element(By.XPATH, xpath_title).text
        
        # Powered by
        xpath_powered = '//*[@id="app"]/div/div/div/div[2]/div[3]/div[1]/div'
        assert "Powered by" in driver.find_element(By.XPATH, xpath_powered).text
        print("INFO: Títulos y créditos validados.")

        # 5. VALIDAR CONTROLES (Forward / Backward)
        t_antes = driver.find_element(By.XPATH, xpath_timer).text
        
        # Forward +10s
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        driver.execute_script("arguments[0].click();", btn_forward)
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != t_antes)
        
        # Backward -10s
        t_despues_fwd = driver.find_element(By.XPATH, xpath_timer).text
        btn_back = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button')
        driver.execute_script("arguments[0].click();", btn_back)
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != t_despues_fwd)
        print("INFO: Controles de tiempo validados.")

        # 6. VALIDAR CONTROL DE VELOCIDAD
        btn_speed = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button')
        btn_speed.click()
        # Verificar que el menú de velocidades se despliegue
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Velocidad")] or //div[contains(@class, "speed")]')))
        print("INFO: Menú de velocidad validado.")

        # 7. VALIDAR PAUSA FINAL Y ESTADO EXTERNO
        driver.execute_script("arguments[0].click();", play_btn)
        driver.switch_to.default_content()
        
        # Label externo "Reproduciendo..."
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_label), "Reproduciendo"))
        
        print("ÉXITO: Todos los componentes del reproductor validados.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Completo_Debug")
        raise e
    finally:
        driver.switch_to.default_content()
