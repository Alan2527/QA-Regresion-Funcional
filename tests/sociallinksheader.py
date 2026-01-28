import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Header")
@allure.story("Validación de Redes Sociales")
def test_social_links_header(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN Y LOCALIZACIÓN
    with allure.step("1. Navegar a la Home y localizar redes sociales del Header"):
        driver.get(url_home)
        
        # Cierre de popup inicial si aparece
        try:
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        xpath_contenedor = '//*[@id="fusion-app"]/div[8]'
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_contenedor)))
        
        # Centrar el contenedor para la captura de contexto
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        time.sleep(2)

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Seccion_Header_Social", 
            attachment_type=allure.attachment_type.PNG
        )

    # 2. CONFIGURACIÓN DE REDES (Mismo orden que el sitio)
    ventana_principal = driver.current_window_handle
    redes_header = {
        "Instagram": '//*[@id="fusion-app"]/div[8]/a[1]',
        "Facebook": '//*[@id="fusion-app"]/div[8]/a[2]',
        "X": '//*[@id="fusion-app"]/div[8]/a[3]',
        "YouTube": '//*[@id="fusion-app"]/div[8]/a[4]',
        "TikTok": '//*[@id="fusion-app"]/div[8]/a[5]'
    }

    # 3. CICLO DE VALIDACIÓN CON CAPTURAS
    for nombre, xpath in redes_header.items():
        with allure.step(f"Validar red social header: {nombre}"):
            link_elemento = driver.find_element(By.XPATH, xpath)
            
            # Click con JS para evitar interrupciones de capas flotantes
            driver.execute_script("arguments[0].click();", link_elemento)
            
            # Esperar a que se abra la nueva ventana
            wait.until(lambda d: len(d.window_handles) > 1)
            
            # Cambiar a la pestaña recién abierta
            nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
            driver.switch_to.window(nueva_ventana)
            
            # Espera de cortesía para carga de contenido y evitar capturas blancas
            time.sleep(5) 
            
            allure.attach(
                driver.get_screenshot_as_png(), 
                name=f"Captura_Header_Pestaña_{nombre}", 
                attachment_type=allure.attachment_type.PNG
            )
            
            # Cerrar y volver a la Home
            driver.close()
            driver.switch_to.window(ventana_principal)
            time.sleep(1)
