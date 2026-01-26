import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    
    # Timeout de carga de página para evitar que el CI se cuelgue
    driver.set_page_load_timeout(60)
    wait = WebDriverWait(driver, 40)
    
    try:
        print(f"INFO: Navegando a {url_nota}")
        driver.get(url_nota)

        # 1. Limpieza de Pop-ups (Para que no tapen el iframe en el CI)
        try:
            btn_aceptar_notif = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]"))
            )
            btn_aceptar_notif.click()
            print("INFO: Pop-up de notificaciones cerrado.")
        except:
            print("INFO: No apareció pop-up de notificaciones.")

        # 2. Localizar el iframe de Trinity
        xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        
        # Scroll para asegurar que el iframe esté en el viewport
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        time.sleep(3)

        # 3. Entrar al iframe
        driver.switch_to.frame(trinity_frame)
        print("INFO: Dentro del iframe.")

        # 4. Encontrar el botón y hacer Click (Usando JS que es más robusto en CI)
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en el botón realizado. Iniciando espera de 30 segundos...")

        # 5. Espera solicitada para que el audio avance
        time.sleep(30)

        # 6. Captura de pantalla para Allure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Captura_Trinity_30s_Post_Click",
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura realizada con éxito.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Captura_Trinity")
        raise e
    finally:
        # Volver al contenido principal siempre
        driver.switch_to.default_content()
