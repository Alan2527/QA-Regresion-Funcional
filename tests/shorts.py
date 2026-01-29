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
    
    # Selectores base
    xpath_container = "//div[contains(@class, 'brick-shorts__container')]"
    xpath_card_short = "//a[contains(@class, 'shortsList__card')]"
    xpath_player_active = "//div[contains(@class, 'shorts-player__video') and contains(@class, 'active')]"
    
    # XPaths específicos solicitados
    xpath_link_nota = "//h2[contains(@class, 'shorts-player__description') and contains(@class, 'active')]/a"
    xpath_btn_cerrar = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button'

    # 1. NAVEGACIÓN INICIAL
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
        time.sleep(2)

    # 2. APERTURA
    with allure.step("2. Abrir reproductor"):
        short_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card_short)))
        driver.execute_script("arguments[0].click();", short_card)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player_active)))
        time.sleep(3)

    # ... (Pasos de Share, Mute y Fullscreen se mantienen igual que la versión anterior)

    # 8. CLICK EN NOTA
    with allure.step("8. Click en el link de la nota"):
        link_nota = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_link_nota)))
        allure.attach(driver.get_screenshot_as_png(), name="8_Antes_Click_Nota", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", link_nota)
        time.sleep(4)
        # Verificamos que no estemos en la home
        assert url_home != driver.current_url, "No se navegó a la nota"

    # 9. VOLVER ATRÁS Y RE-CENTRAR
    with allure.step("9. Volver atrás y buscar componente Shorts"):
        driver.back()
        time.sleep(3)
        # Volvemos a buscar el contenedor para asegurar que el DOM está listo
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="9_Home_Recentrada", attachment_type=allure.attachment_type.PNG)

    # 10. CERRAR REPRODUCTOR
    with allure.step("10. Cerrar reproductor"):
        btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_btn_cerrar)))
        driver.execute_script("arguments[0].click();", btn_cerrar)
        # Esperamos que el elemento del reproductor activo desaparezca
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player_active)))
        allure.attach(driver.get_screenshot_as_png(), name="10_Reproductor_Cerrado", attachment_type=allure.attachment_type.PNG)
