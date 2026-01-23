import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_social_links_footer(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_home)
        print(f"INFO: Navegando a la Home para validar footer: {url_home}")

        # 1. Buscar el contenedor del footer y hacer scroll
        xpath_footer_social = '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]'
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_footer_social)))
        
        # Scroll al footer
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        print("INFO: Scroll realizado hasta la sección social del Footer.")
        time.sleep(2) # Pausa para que el footer se renderice bien

        # --- CAPTURA DE PANTALLA ---
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Footer_Social_Links", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura del footer adjuntada a Allure.")

        # Guardamos la ventana principal
        ventana_principal = driver.current_window_handle

        # 2. XPaths exactos que me pasaste
        redes_footer = [
            '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[1]',
            '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[2]',
            '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[3]',
            '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[4]',
            '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[5]'
        ]

        # 3. Ciclo de clics y validación de pestañas
        for idx, xpath in enumerate(redes_footer, 1):
            link_elemento = driver.find_element(By.XPATH, xpath)
            href_previsto = link_elemento.get_attribute('href')
            
            # Click con JS para evitar bloqueos
            driver.execute_script("arguments[0].click();", link_elemento)
            print(f"PROBANDO RED SOCIAL FOOTER #{idx}: {href_previsto}")

            # Esperar nueva pestaña
            wait.until(lambda d: len(d.window_handles) > 1)
            
            # Cambiar a pestaña nueva
            nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
            driver.switch_to.window(nueva_ventana)
            
            # Validar y loguear URL final
            url_final = driver.current_url
            print(f"   - Pestaña abierta con éxito. URL actual: {url_final}")
            
            # Cerrar y volver
            driver.close()
            driver.switch_to.window(ventana_principal)
            time.sleep(0.5)

        print("ÉXITO: Todos los links del footer abren correctamente en pestañas nuevas.")

    except Exception as e:
        print(f"ERROR: Fallo en validación de redes del footer: {str(e)}")
        raise e
