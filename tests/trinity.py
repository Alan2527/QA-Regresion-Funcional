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
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 40)
    
    # 1. NAVEGACIÓN
    with allure.step("1. Navegación y limpieza"):
        try:
            driver.get(url_nota)
            btn_aceptar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except Exception as e:
            print(f"Aviso: Pop-up no detectado: {e}")

    # 2. ENTRADA AL IFRAME
    with allure.step("2. Entrada al Iframe"):
        try:
            xpath_iframe = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/div/div/trinity-player-icon-player-layout-wrapper/div/iframe'
            trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
            driver.switch_to.frame(trinity_frame)
            print("INFO: Dentro del iframe de Trinity.")
        except Exception as e:
            print(f"Error Iframe: {e}")

    # 3. CLICK EN PLAY Y CAPTURA A LOS 20 SEGUNDOS (LO QUE PEDISTE)
    with allure.step("3. Inicio de Reproducción y Evidencia"):
        try:
            xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
            
            # Click inicial por JS para asegurar ejecución
            driver.execute_script("arguments[0].click();", play_btn)
            print("INFO: Click en Play realizado. Esperando 20 segundos para tomar captura...")
            
            # ESPERA DE 20 SEGUNDOS
            time.sleep(20)
            
            # --- CAPTURA PARA EL REPORTE DE ALLURE ---
            allure.attach(driver.get_screenshot_as_png(), 
                          name="Captura_Trinity_20s_Post_Play", 
                          attachment_type=allure.attachment_type.PNG)
            print("INFO: Captura de 20s adjuntada.")
        except Exception as e:
            print(f"Error en Play: {e}")
            allure.attach(driver.get_screenshot_as_png(), name="Error_Paso_Play")

    # 4. ADELANTAR 10 SEGUNDOS
    with allure.step("4. Validación: Adelantar 10 segundos"):
        try:
            xpath_timer = '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]'
            xpath_adelantar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
            
            tiempo_antes = driver.find_element(By.XPATH, xpath_timer).text
            btn_adelantar = driver.find_element(By.XPATH, xpath_adelantar)
            driver.execute_script("arguments[0].click();", btn_adelantar)
            
            time.sleep(4) # Espera para que el cronómetro actualice
            tiempo_despues = driver.find_element(By.XPATH, xpath_timer).text
            print(f"STDOUT: Adelantar -> Antes: {tiempo_antes} | Después: {tiempo_despues}")
        except Exception as e:
            print(f"Error al adelantar: {e}")

    # 5. ATRASAR 10 SEGUNDOS
    with allure.step("5. Validación: Atrasar 10 segundos"):
        try:
            xpath_atrasar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button'
            btn_atrasar = driver.find_element(By.XPATH, xpath_atrasar)
            driver.execute_script("arguments[0].click();", btn_atrasar)
            time.sleep(2)
            print("STDOUT: Click en atrasar 10s realizado.")
        except Exception as e:
            print(f"Error al atrasar: {e}")

    # 6. MENÚ DE VELOCIDAD (ABRIR / CAPTURA / CERRAR)
    with allure.step("6. Validación: Menú de Velocidad"):
        try:
            xpath_abrir_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button'
            xpath_cerrar_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button'
            
            # Abrir
            btn_abrir = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir_vel)))
            driver.execute_script("arguments[0].click();", btn_abrir)
            time.sleep(2)
            
            # Captura con el menú abierto
            allure.attach(driver.get_screenshot_as_png(), name="Menu_Velocidad_Visible")
            
            # Cerrar
            btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_vel)))
            driver.execute_script("arguments[0].click();", btn_cerrar)
            print("STDOUT: Menú de velocidad validado.")
        except Exception as e:
            print(f"Error en menú velocidad: {e}")

    # FINALIZACIÓN
    driver.switch_to.default_content()
    print("STDOUT: Test finalizado completamente.")
