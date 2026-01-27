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
    
    # 1. NAVEGACIÓN (Sin captura)
    with allure.step("1. Navegación y limpieza"):
        driver.get(url_nota)
        try:
            btn_aceptar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

    # 2. ENTRADA AL IFRAME (Sin captura)
    with allure.step("2. Entrada al Iframe"):
        xpath_iframe = '//trinity-player-icon-player-layout-wrapper/div/iframe'
        trinity_frame = wait.until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trinity_frame)
        driver.switch_to.frame(trinity_frame)

    # 3. INICIO DE REPRODUCCIÓN (Con captura tras 20s)
    with allure.step("3. Inicio de Reproducción"):
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].click();", play_btn)
        time.sleep(20)
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Evidencia_Reproduccion_20s", 
                      attachment_type=allure.attachment_type.PNG)

    # 4. ADELANTAR 10 SEGUNDOS (Con captura)
    with allure.step("4. Validación: Adelantar 10 segundos"):
        xpath_adelantar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_adelantar))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Evidencia_Adelantar_10s", 
                      attachment_type=allure.attachment_type.PNG)

    # 5. ATRASAR 10 SEGUNDOS (Con captura)
    with allure.step("5. Validación: Atrasar 10 segundos"):
        xpath_atrasar = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button'
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_atrasar))
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Evidencia_Atrasar_10s", 
                      attachment_type=allure.attachment_type.PNG)

    # 6. MENÚ DE VELOCIDAD (Con captura)
    with allure.step("6. Validación: Menú de Velocidad"):
        xpath_abrir_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/button'
        xpath_cerrar_vel = '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button'
        
        # Abrir menú
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir_vel))))
        time.sleep(2)
        
        # Captura con el menú desplegado
        allure.attach(driver.get_screenshot_as_png(), 
                      name="Evidencia_Menu_Velocidad", 
                      attachment_type=allure.attachment_type.PNG)
        
        # Cerrar menú
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_vel))))

    driver.switch_to.default_content()
