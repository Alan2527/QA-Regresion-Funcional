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

        # 1. Localizar el iframe y entrar
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(2) 

        driver.switch_to.frame(trinity_frame)
        print("INFO: Switch exitoso al iframe.")

        # 2. Click en el botón de Play que mencionas
        # Este botón inicia la reproducción y expande el reproductor
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        
        # Usamos click de JS para asegurar que se dispare la acción
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en botón Play de Trinity realizado.")

        # 3. ESPERA DE RENDERIZADO (Clave para la captura)
        # En lugar de buscar clases técnicas que fallan, esperamos a que el 
        # contenedor del reproductor sea visible y el texto aparezca.
        time.sleep(4) # Tiempo de gracia para que el reproductor se abra y empiece el audio

        # Validamos que el título aparezca (evidencia de que ya cargó la info)
        xpath_title_span = '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span'
        wait.until(lambda d: d.find_element(By.XPATH, xpath_title_span).text != "")

        # 4. CAPTURA: Aquí ya debería verse el botón de Pausa/Stop y el tiempo corriendo
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Captura_Trinity_Reproduciendo",
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura realizada. Debería verse el estado activo.")

        # 5. Validaciones de elementos internos
        timer_current = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div')
        assert timer_current.is_displayed()
        print(f"INFO: Tiempo actual detectado: {timer_current.text}")

        # 6. Validar Forward (+10 seg)
        t_antes = timer_current.text
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        btn_forward.click()
        wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text != t_antes)
        print("INFO: Forward validado.")

        # 7. Pausa Final
        driver.execute_script("arguments[0].click();", play_btn)
        time.sleep(1)
        print("INFO: Reproductor pausado.")

        # 8. Salir y validar label externo (Reproduciendo...)
        driver.switch_to.default_content()
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_label), "Reproduciendo"))
        print("ÉXITO: Test completado.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Captura", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        driver.switch_to.default_content()
