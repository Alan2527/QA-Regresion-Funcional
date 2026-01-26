import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    # Aumentamos el tiempo de espera por lentitud del CI
    wait = WebDriverWait(driver, 60)
    
    try:
        # Cargamos la página con un tiempo de espera robusto
        driver.get(url_nota)
        print("INFO: Nota cargada.")

        # 1. Localizar y entrar al iframe (Aseguramos scroll)
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(3) 
        driver.switch_to.frame(trinity_frame)

        # 2. Click en Play
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Play clickeado.")

        # 3. ESPERA CRÍTICA: Que el cronómetro avance
        xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div'
        # Esperamos a que pase de 00:00 a cualquier otra cosa (evidencia de que está sonando)
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != "00:00")
        
        # DAMOS UN SEGUNDO EXTRA para que el icono de Play se convierta en Pausa en la pantalla
        time.sleep(2)

        # CAPTURA DE PANTALLA
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Evidencia_Reproduccion_Activa",
            attachment_type=allure.attachment_type.PNG
        )

        # 4. Validar que el tiempo actual ya no es 00:00
        t_actual = driver.find_element(By.XPATH, xpath_timer).text
        assert t_actual != "00:00"
        print(f"INFO: El audio está sonando. Tiempo: {t_actual}")

        # 5. Validar Forward (+10s)
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        driver.execute_script("arguments[0].click();", btn_forward)
        wait.until(lambda d: d.find_element(By.XPATH, xpath_timer).text != t_actual)
        print("INFO: Forward validado.")

        driver.switch_to.default_content()
        print("ÉXITO: Trinity validado correctamente.")

    except Exception as e:
        print(f"ERROR en Trinity: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Trinity", attachment_type=allure.attachment_type.PNG)
        raise e
