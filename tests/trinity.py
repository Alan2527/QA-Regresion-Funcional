import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 40)
    
    try:
        driver.get(url_nota)
        
        # 1. Localizar y entrar al iframe
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(2) 
        driver.switch_to.frame(trinity_frame)

        # 2. Click en Play
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado.")

        # 3. SINCRONIZACIÓN PARA LA CAPTURA PERFECTA
        # Esperamos a que la clase del botón cambie a 'button-pause'
        # Esto confirma que el reproductor YA procesó el click y cambió el ícono
        wait.until(lambda d: "button-pause" in d.find_element(By.XPATH, xpath_play_btn).get_attribute("class"))
        
        # Esperamos a que el tiempo avance (evidencia de audio corriendo)
        xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div'
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != "00:00")
        
        # Pequeño margen para que el renderizado visual de la imagen se complete
        time.sleep(1.5)

        # CAPTURA: Ahora sí debe verse el botón de Pausa/Stop
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Trinity_REPRODUCIENDO_BOTON_PAUSA", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura realizada con el botón de Pausa visible.")

        # 4. Validar Forward (+10 seg)
        t_antes = driver.find_element(By.XPATH, xpath_timer).text
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        driver.execute_script("arguments[0].click();", btn_forward)
        
        # Esperamos que el texto del tiempo sea distinto al anterior
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != t_antes)
        print(f"INFO: Forward ok. Tiempo actual: {driver.find_element(By.XPATH, xpath_timer).text}")

        # 5. Salir y validar label externo
        driver.switch_to.default_content()
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_label), "Reproduciendo"))
        print("ÉXITO: Test finalizado con evidencias visuales correctas.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Debug", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        driver.switch_to.default_content()
