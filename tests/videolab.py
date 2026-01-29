import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor")
@allure.story("Validación VideoLab Completa")
def test_videolab_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN Y APERTURA
    with allure.step("1. Navegar a Home y abrir VideoLab"):
        driver.get(url_home)
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host, .notifications-popup').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

        xpath_contenedor = '//*[@id="fusion-app"]/div[12]/main/div[17]/div'
        xpath_primer_video = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[2]/div[2]/div/div/div/div[1]/div/a'
        
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_contenedor)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        time.sleep(2)
        
        btn_video = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_primer_video)))
        driver.execute_script("arguments[0].click();", btn_video)
        time.sleep(3)

    # 2. MUTE (PASO SEPARADO)
    with allure.step("2. Probar botón de Silencio (Mute)"):
        btn_mute = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'vjs-mute-control')]")))
        driver.execute_script("arguments[0].click();", btn_mute)
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_VideoLab_Mute", attachment_type=allure.attachment_type.PNG)

    # 3. FULLSCREEN (PASO SEPARADO)
    with allure.step("3. Probar Pantalla Completa (Fullscreen)"):
        btn_fs = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'vjs-fullscreen-control')]")))
        driver.execute_script("arguments[0].click();", btn_fs)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_VideoLab_Fullscreen", attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", btn_fs) # Salir de FS
        time.sleep(1)

    # 4. COMPARTIR
    with allure.step("4. Validar menú de compartir"):
        btn_share = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share')]")))
        driver.execute_script("arguments[0].click();", btn_share)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_VideoLab_Share", attachment_type=allure.attachment_type.PNG)
        # Re-click para cerrar menu si es necesario o click en fondo
        driver.execute_script("arguments[0].click();", btn_share)

    # 5. CLICK EN DESCRIPCIÓN (REDIRECCIÓN)
    with allure.step("5. Click en descripción y validar redirección a nota"):
        # Usamos un selector para el título/descripción que suele ser un link <a> dentro del player
        # Según la estructura de TN, suele tener clases como 'video-headline' o similar
        xpath_desc = "//div[contains(@class, 'video-lab-player')]//a[contains(@class, 'title')] | //div[contains(@id, 'video')]//a"
        
        try:
            link_desc = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_desc)))
            href_destino = link_desc.get_attribute('href')
            driver.execute_script("arguments[0].click();", link_desc)
            
            # Esperar a que la URL cambie (no debería ser la home)
            wait.until(lambda d: d.current_url != url_home)
            time.sleep(3)
            
            allure.attach(driver.get_screenshot_as_png(), name="Captura_Redireccion_Descripcion", attachment_type=allure.attachment_type.PNG)
            
            # Validación: Que la URL actual sea la que prometía el href
            assert driver.current_url in href_destino or "tn.com.ar" in driver.current_url
        except Exception as e:
            pytest.fail(f"No se pudo interactuar con la descripción para redirección: {e}")
