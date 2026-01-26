import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor de Audio")
@allure.story("Validación Integral de Controles Trinity con XPaths Específicos")
def test_trinity_audio_player_full_suite(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 40)
    
    try:
        with allure.step("1. Navegación y limpieza"):
            print(f"INFO: Navegando a {url_nota}")
            driver.get(url_nota)
            try:
                btn_aceptar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]"))
                )
                btn_aceptar.click()
                print("STDOUT: Pop-up de notificaciones cerrado.")
            except:
                print("STDOUT: No se detectó pop-up de notificaciones.")

        with allure.step("2. Entrada al Iframe"):
            xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
            trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
            time.sleep(2)
            driver.switch_to.frame(trinity_frame)
            print("STDOUT: Dentro del iframe de Trinity.")

        with allure.step("3. Inicio de Reproducción"):
            xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
            driver.execute_script("arguments[0].click();", play_btn)
            print("STDOUT: Click en Play realizado. Esperando 15s para estabilizar reproducción...")
            time.sleep(15)

        with allure.step("4. Validación: Adelantar 10 segundos"):
            xpath_adelantar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
            xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div'
            
            tiempo_antes = driver.find_element(By.XPATH, xpath_timer).text
            btn_adelantar = driver.find_element(By.XPATH, xpath_adelantar)
            driver.execute_script("arguments[0].click();", btn_adelantar)
            
            time.sleep(2)
            tiempo_despues = driver.find_element(By.XPATH, xpath_timer).text
            print(f"STDOUT: Adelantar 10s -> Antes: {tiempo_antes} | Después: {tiempo_despues}")
            assert tiempo_despues > tiempo_antes, "ERROR: El tiempo no avanzó al adelantar."

        with allure.step("5. Validación: Atrasar 10 segundos"):
            xpath_atrasar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button'
            btn_atrasar = driver.find_element(By.XPATH, xpath_atrasar)
            
            driver.execute_script("arguments[0].click();", btn_atrasar)
            time.sleep(2)
            tiempo_final = driver.find_element(By.XPATH, xpath_timer).text
            print(f"STDOUT: Atrasar 10s -> Tiempo actual: {tiempo_final}")

        with allure.step("6. Validación: Cambio de Velocidad"):
            xpath_vel = '//*[contains(@class, "trinity-player-playback-rate")]'
            btn_vel = driver.find_element(By.XPATH, xpath_vel)
            
            vel_inicial = btn_vel.text
            driver.execute_script("arguments[0].click();", btn_vel)
            time.sleep(2)
            vel_nueva = btn_vel.text
            print(f"STDOUT: Cambio Velocidad -> Inicial: {vel_inicial} | Nueva: {vel_nueva}")
            assert vel_inicial != vel_nueva, "ERROR: La velocidad no cambió."

        with allure.step("7. Captura Final"):
            status_text = driver.find_element(By.ID, "trinity-player-status-text").text
            print(f"STDOUT: Estado final: {status_text} | Cronómetro final: {tiempo_final}")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Trinity_Full_Test_Success",
                attachment_type=allure.attachment_type.PNG
            )
            assert "Escuchando" in status_text or "Reproduciendo" in status_text

    except Exception as e:
        print(f"STDOUT ERROR: Fallo detectado -> {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Step_Detail")
        raise e
    finally:
        driver.switch_to.default_content()
        print("STDOUT: Proceso finalizado.")
