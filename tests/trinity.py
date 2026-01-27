import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor de Audio")
@allure.story("Validación de Controles Trinity")
def test_trinity_audio_player_full_suite(driver):
    driver.set_page_load_timeout(60)
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 40)
    
    # 1. NAVEGACIÓN
    with allure.step("1. Navegación y limpieza"):
        driver.get(url_nota)
        try:
            btn_aceptar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

    # 2. ENTRADA AL IFRAME
    with allure.step("2. Entrada al Iframe"):
        xpath_iframe = '//trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        driver.switch_to.frame(trinity_frame)

    # 3. CLICK EN PLAY Y ESPERA DE 20 SEGUNDOS
    with allure.step("3. Inicio de Reproducción"):
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado. Esperando 20 segundos...")
        time.sleep(20)

    # --- ESTA ES LA CAPTURA QUE ME PEDÍS (PUESTA FUERA PARA QUE SE VEA SI O SI) ---
    allure.attach(driver.get_screenshot_as_png(), 
                  name="EVIDENCIA_REPRODUCCION_20_SEGUNDOS", 
                  attachment_type=allure.attachment_type.PNG)
    # -----------------------------------------------------------------------------

    # 4. ADELANTAR 10 SEGUNDOS
    with allure.step("4. Validación: Adelantar 10 segundos"):
        xpath_adelantar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_adelantar))
        time.sleep(2)

    # 5. ATRASAR 10 SEGUNDOS
    with allure.step("5. Validación: Atrasar 10 segundos"):
        xpath_atrasar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button'
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_atrasar))
        time.sleep(2)

    # 6. MENÚ DE VELOCIDAD
    with allure.step("6. Validación: Menú de Velocidad"):
        xpath_abrir_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button'
        xpath_cerrar_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button'
        
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir_vel))))
        time.sleep(2)
        # Captura adicional del menú abierto
        allure.attach(driver.get_screenshot_as_png(), name="Menu_Velocidad_Abierto")
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_vel))))

    driver.switch_to.default_content()
