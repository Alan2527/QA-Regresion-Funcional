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
        
        # Hacemos scroll y centramos el botón antes de abrirlo
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_share)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", boton_share)
        print("INFO: Se hizo click en el botón principal de compartir.")

        # --- AJUSTE PARA LA CAPTURA ---
        # Esperamos a que el primer botón de las opciones (Facebook/X) sea visible
        xpath_opcion_1 = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_opcion_1)))
        
        # Pequeña pausa extra para que la animación termine de abrirse
        time.sleep(2) 

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Share_Toolbar_Abierto", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura con el toolbar ABIERTO adjuntada.")

        # 2. XPaths de las opciones
        opciones_share = [
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]',
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]'
        ]

        ventana_principal = driver.current_window_handle

        # 3. Validar cada opción
        for idx, xpath in enumerate(opciones_share, 1):
            boton_opcion = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", boton_opcion)
            
            try:
                # Esperamos un momento para ver si abre ventana
                time.sleep(1.5)
                if len(driver.window_handles) > 1:
                    nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                    driver.switch_to.window(nueva_ventana)
                    print(f"OPCIÓN #{idx}: URL detectada -> {driver.current_url}")
                    driver.close()
                    driver.switch_to.window(ventana_principal)
                else:
                    print(f"OPCIÓN #{idx}: Se procesó internamente (Copiar link/otros).")
            except:
                driver.switch_to.window(ventana_principal)
                continue

        # 4. Cerrar
        xpath_cerrar = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[1]/div/button'
        boton_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar)))
        driver.execute_script("arguments[0].click();", boton_cerrar)
        print("INFO: Test finalizado y toolbar cerrado.")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise e
