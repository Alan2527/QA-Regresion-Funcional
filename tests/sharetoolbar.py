import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_share_toolbar_validation(driver):
    url_nota = "https://tn.com.ar/turismo/2026/01/22/ni-chivilcoy-ni-chascomus-el-pueblo-a-1-hora-de-buenos-aires-con-una-laguna-parrillas-y-campings/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_nota)
        print(f"INFO: Navegando a la nota de turismo: {url_nota}")

        # 1. Click en el botón principal de compartir
        xpath_abrir = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div/button'
        boton_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir)))
        driver.execute_script("arguments[0].click();", boton_share)
        print("INFO: Se hizo click en el botón principal de compartir.")
        time.sleep(2)

        # 2. Captura de pantalla con las opciones desplegadas
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Share_Toolbar_Desplegado", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura del toolbar desplegado adjuntada.")

        # Guardamos la ventana principal
        ventana_principal = driver.current_window_handle

        # 3. XPaths de las opciones de compartir
        opciones_share = [
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]'
        ]

        for idx, xpath in enumerate(opciones_share, 1):
            boton_opcion = driver.find_element(By.XPATH, xpath)
            
            # Click para abrir la red social
            driver.execute_script("arguments[0].click();", boton_opcion)
            print(f"PROBANDO OPCIÓN DE COMPARTIR #{idx}...")

            # Esperar a que se abra la nueva ventana/pestaña
            try:
                wait.until(lambda d: len(d.window_handles) > 1)
                nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                driver.switch_to.window(nueva_ventana)
                
                # Loguear la URL de la red social (Facebook, Twitter, etc.)
                print(f"   - Redirección exitosa. URL: {driver.current_url}")
                
                driver.close()
                driver.switch_to.window(ventana_principal)
            except:
                print(f"   - INFO: La opción #{idx} no abrió una ventana externa (puede ser Copiar Link o Email).")
            
            time.sleep(1)

        # 4. Cerrar el toolbar
        xpath_cerrar = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[1]/div/button'
        boton_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar)))
        driver.execute_script("arguments[0].click();", boton_cerrar)
        print("INFO: Toolbar de compartir cerrado correctamente.")

        print("ÉXITO: Test de sharetoolbar completado.")

    except Exception as e:
        print(f"ERROR: Falló el test de Share Toolbar: {str(e)}")
        raise e
