import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Shorts")
@allure.story("Validación Completa del Reproductor")
def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30)
    
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_card_short = "//a[contains(@class, 'shortsList__card')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    xpath_h2_desc = "//h2[contains(@class, 'shorts-player__description')]"

    # 1. NAVEGACIÓN
    with allure.step("1. Buscar y scrollear al Brick de Shorts"):
        driver.get(url_home)
        try:
            btn_aceptar = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(3)

    # 2. APERTURA
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card_short)))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player_active)))
        time.sleep(4) 

    # 3. EL OJO, 4. NAVEGACIÓN (Se mantienen igual para no perder cobertura)
    # ... (omitidos en este snippet para brevedad, pero mantenelos en tu archivo)

    # 5. SHARE BUTTON Y REDES (DETALLADO)
    with allure.step("5. Validar Botón Share y sus Redes"):
        xpath_share_principal = "//button[contains(@class, 'share-button')]"
        btn_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_share_principal)))
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(2) # Espera a que despliegue el panel

        redes_shorts = [
            {"nombre": "Facebook", "xpath": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[1]'},
            {"nombre": "X", "xpath": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[2]'},
            {"nombre": "Copiar", "xpath": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[3]', "instantanea": True},
            {"nombre": "WhatsApp", "xpath": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[4]'},
            {"nombre": "Telegram", "xpath": '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]/button[5]'}
        ]

        ventana_home = driver.current_window_handle

        for red in redes_shorts:
            with allure.step(f"Probar {red['nombre']}"):
                btn_red = driver.find_element(By.XPATH, red['xpath'])
                driver.execute_script("arguments[0].click();", btn_red)
                
                if red.get("instantanea"):
                    # Captura inmediata para el tooltip de "Copiado"
                    allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                else:
                    # Lógica para redes que abren ventana nueva
                    time.sleep(2)
                    handles = driver.window_handles
                    if len(handles) > 1:
                        nueva_ventana = [h for h in handles if h != ventana_home][0]
                        driver.switch_to.window(nueva_ventana)
                        time.sleep(2)
                        allure.attach(driver.get_screenshot_as_png(), name=f"Ventana_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                        driver.close()
                        driver.switch_to.window(ventana_home)
                    else:
                        allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{red['nombre']}", attachment_type=allure.attachment_type.PNG)

        # Cerrar el panel de share
        driver.execute_script("arguments[0].click();", btn_share)

    # 6. MUTE Y 7. FULLSCREEN (Separados como pediste)
    with allure.step("6. Validar Mute"):
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@class, 'mute--button')]"))
        allure.attach(driver.get_screenshot_as_png(), name="6_Mute", attachment_type=allure.attachment_type.PNG)

    with allure.step("7. Validar Fullscreen"):
        btn_fs = driver.find_element(By.XPATH, "//button[contains(@class, 'fullscreen--button')]")
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs)

    # 8. LINK NOTA Y RE-CENTRADO (EL FIX DEL FALLO)
    with allure.step("8. Click en nota, volver y re-centrar"):
        link_nota = driver.find_element(By.XPATH, f"{xpath_h2_desc}/a")
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        driver.back()
        
        # Volvemos a buscar el componente y nos centramos
        time.sleep(3)
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="8_Home_Recentrada", attachment_type=allure.attachment_type.PNG)

    # 9. CERRAR
    with allure.step("9. Cerrar reproductor"):
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'shorts-player__close')]")))
        driver.execute_script("arguments[0].click();", close_btn)
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player_active)))
