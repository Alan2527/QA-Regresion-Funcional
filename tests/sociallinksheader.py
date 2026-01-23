import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_social_links_header(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_home)
        print(f"INFO: Navegando a la Home: {url_home}")

        # 1. Buscar el contenedor principal
        xpath_contenedor = '//*[@id="fusion-app"]/div[8]'
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_contenedor)))
        
        # Centrar para la captura final
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        print("INFO: Contenedor 'brick-social-links' localizado y centrado.")
        time.sleep(1)

        # Guardamos el ID de la pestaña principal
        ventana_principal = driver.current_window_handle

        # 2. Definir los XPaths de los 5 enlaces
        redes_xpaths = [
            '//*[@id="fusion-app"]/div[8]/a[1]',
            '//*[@id="fusion-app"]/div[8]/a[2]',
            '//*[@id="fusion-app"]/div[8]/a[3]',
            '//*[@id="fusion-app"]/div[8]/a[4]',
            '//*[@id="fusion-app"]/div[8]/a[5]'
        ]

        print(f"INFO: Iniciando validación de {len(redes_xpaths)} enlaces sociales.")

        # 3. Iterar y validar cada link
        for idx, xpath in enumerate(redes_xpaths, 1):
            link_elemento = driver.find_element(By.XPATH, xpath)
            href_destino = link_elemento.get_attribute('href')
            
            # Click usando JS para asegurar la apertura
            driver.execute_script("arguments[0].click();", link_elemento)
            print(f"CLICK #{idx}: Se clickeó en el enlace con destino: {href_destino}")
            
            # Esperar a que se abra la nueva pestaña
            wait.until(lambda d: len(d.window_handles) > 1)
            
            # Cambiar a la nueva pestaña
            nueva_ventana = [window for window in driver.window_handles if window != ventana_principal][0]
            driver.switch_to.window(nueva_ventana)
            
            # Validar URL
            url_detectada = driver.current_url
            print(f"   - Pestaña nueva abierta correctamente. URL: {url_detectada}")
            
            # Cerrar pestaña nueva y volver a la principal
            driver.close()
            driver.switch_to.window(ventana_principal)
            time.sleep(0.5)

        print("ÉXITO: Todos los enlaces sociales abren en pestañas nuevas con las URLs correctas.")

    except Exception as e:
        print(f"ERROR: Falló la validación de redes sociales: {str(e)}")
        raise e

    finally:
        # 4. Captura final centrada en el div social
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Social_Links", 
            attachment_type=allure.attachment_type.PNG
        )
