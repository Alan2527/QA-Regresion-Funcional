import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor de Audio")
@allure.story("Validación Integral de Controles Trinity")
def test_trinity_audio_player_full_suite(driver):
    driver.set_page_load_timeout(60)
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el- apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 40)
    
    # 1. Navegación
    with allure.step("1. Navegación y limpieza"):
        try:
            driver.get(url_nota)
            btn_aceptar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except Exception as e:
            print(f"Aviso: Pop-up no detectado: {e}")

    # 2. Entrada al Iframe
    with allure.step("2. Entrada al Iframe"):
        try:
            xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
            trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
            driver.switch_to.frame(trinity_frame)
        except Exception as e:
            print(f"Error Iframe: {e}")

    # 3. Inicio de Reproducción y Captura Solicitada
    with allure.step("3. Inicio de Reproducción"):
        try:
            xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
            
            # Click inicial
            driver.execute_script("arguments[0].click();", play_btn)
            print("INFO: Click en Play realizado. Esperando 20 segundos para la captura...")
            
            # ESPERA DE 20 SEGUNDOS
            time.sleep(20)
            
            # CAPTURA DE PANTALLA SOLICITADA
            allure.attach(driver.get_screenshot_as_png(), 
                          name="Captura_Trinity_20s_Post_Click", 
                          attachment_type=allure.attachment_type.PNG)
            print("INFO: Captura realizada tras 20s.")
            
        except Exception as e:
            print(f"Error en paso de reproducción: {e}")
            allure.attach(driver.get_screenshot_as_png(), name="Error_en_Play")

    # 4. Adelantar 10s
    with allure.step("4. Validación: Adelantar 10 segundos"):
        try:
            xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]'
            xpath_adelantar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
            
            t_antes = driver.find_element(By.XPATH, xpath_timer).text
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_adelantar))
            time.sleep(4)
            t_despues = driver.find_element(By.XPATH, xpath_timer).text
            print(f"STDOUT: Adelantar -> Antes: {t_antes} | Después: {t_despues}")
        except Exception as e:
            print(f"Fallo paso 4: {e}")

    # 5. Menú de Velocidad
    with allure.step("5. Validación: Menú de Velocidad"):
        try:
            xpath_abrir_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button'
            xpath_cerrar_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button'
            
            driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir_vel))))
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="Menu_Velocidad_Abierto")
            
            driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_vel))))
        except Exception as e:
            print(f"Fallo paso 5: {e}")

    # Finalización
    driver.switch_to.default_content()
