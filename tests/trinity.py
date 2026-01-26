import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor de Audio")
@allure.story("Validación Integral de Controles Trinity")
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
                print("INFO: Pop-up de notificaciones cerrado.")
            except:
                print("INFO: No se detectó pop-up de notificaciones.")

        with allure.step("2. Entrada al Iframe"):
            xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
            trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
            time.sleep(2)
            driver.switch_to.frame(trinity_frame)
            print("INFO: Dentro del iframe de Trinity.")

        with allure.step("3. Inicio de Reproducción"):
            xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
            driver.execute_script("arguments[0].click();", play_btn)
            print("INFO: Click en Play realizado. Esperando carga inicial...")
            time.sleep(10) # Espera necesaria para que el timer salga de 00:00

        with allure.step("4. Validación: Adelantar 10 segundos"):
            btn_adelantar = driver.find_element(By.XPATH, '//button[@aria-label="Seek forward 10 seconds"]')
            tiempo_antes = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text
            driver.execute_script("arguments[0].click();", btn_adelantar)
            time.sleep(2)
            tiempo_despues = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text
            print(f"INFO: Adelantar 10s -> Antes: {tiempo_antes} | Después: {tiempo_despues}")
            assert tiempo_despues > tiempo_antes, "El tiempo no avanzó tras adelantar."

        with allure.step("5. Validación: Atrasar 10 segundos"):
            btn_atrasar = driver.find_element(By.XPATH, '//button[@aria-label="Seek backward 10 seconds"]')
            driver.execute_script("arguments[0].click();", btn_atrasar)
            time.sleep(2)
            tiempo_final = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div').text
            print(f"INFO: Atrasar 10s -> Tiempo actual: {tiempo_final}")

        with allure.step("6. Validación: Cambio de Velocidad"):
            # Localizamos por la clase que contiene la tasa de velocidad
            btn_vel = driver.find_element(By.XPATH, '//*[contains(@class, "trinity-player-playback-rate")]')
            vel_inicial = btn_vel.text
            driver.execute_script("arguments[0].click();", btn_vel)
            time.sleep(2)
            vel_nueva = btn_vel.text
            print(f"INFO: Cambio Velocidad -> Inicial: {vel_inicial} | Nueva: {vel_nueva}")
            assert vel_inicial != vel_nueva, "La velocidad de reproducción no cambió."

        with allure.step("7. Captura Final y Verificación de Estado"):
            status_text = driver.find_element(By.ID, "trinity-player-status-text").text
            print(f"INFO: Estado final del reproductor: {status_text}")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Trinity_Full_Test_Success",
                attachment_type=allure.attachment_type.PNG
            )
            assert "Escuchando" in status_text or "Reproduciendo" in status_text

    except Exception as e:
        print(f"ERROR: Falló el test en algún paso. Detalle: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Step_Detail")
        raise e
    finally:
        driver.switch_to.default_content()
        print("INFO: Test finalizado y driver reseteado al contenido principal.")
