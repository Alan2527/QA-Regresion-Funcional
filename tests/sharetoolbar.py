import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Social Share")
@allure.story("Validación de Toolbar de Compartir")
def test_share_toolbar_validation(driver):
    # BLOQUEO DE ADS (Imágenes habilitadas)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "*.googlesyndication.com", "*.doubleclick.net", "*.ads*", 
            "*.adnxs*", "*.analytics*", "*.taboola*"
        ]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url_nota = "https://tn.com.ar/turismo/2026/01/22/ni-chivilcoy-ni-chascomus-el-pueblo-a-1-hora-de-buenos-aires-con-una-laguna-parrillas-y-campings/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN Y LIMPIEZA
    with allure.step("1. Navegación, limpieza de popups y ads"):
        driver.get(url_nota)
        try:
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

    # 2. LOCALIZAR TOOLBAR
    with allure.step("2. Localizar Sharetoolbar"):
        xpath_abrir = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div/button'
        boton_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir)))
        
        # Centramos el componente
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_share)
        time.sleep(1)
        
        # CAPTURA ANTES DE ABRIR (Como pediste)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Sharetoolbar_Antes_de_Abrir", 
            attachment_type=allure.attachment_type.PNG
        )
        
        driver.execute_script("arguments[0].click();", boton_share)
        
        # Esperamos visibilidad de opciones
        xpath_opcion_1 = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_opcion_1)))
        time.sleep(2)

    # 3. CAPTURA TOOLBAR ABIERTO
    with allure.step("3. Sharetoolbar Abierto"):
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Sharetoolbar_Abierto", 
            attachment_type=allure.attachment_type.PNG
        )

    # 4. VALIDACIÓN DE REDES SOCIALES
    with allure.step("4. Validación de redes sociales (ventanas externas)"):
        opciones_share = [
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]', # FB
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]', # X
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]', # Copiar
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]', # WA
            '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]'  # Telegram
        ]
        ventana_principal = driver.current_window_handle

        for idx, xpath in enumerate(opciones_share, 1):
            try:
                boton_opcion = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click();", boton_opcion)
                time.sleep(2) # Espera para que la ventana cargue
                
                if len(driver.window_handles) > 1:
                    nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                    driver.switch_to.window(nueva_ventana)
                    
                    # CAPTURA DE LA VENTANA EXTERNA (Como pediste)
                    allure.attach(
                        driver.get_screenshot_as_png(), 
                        name=f"Ventana_Red_Social_Opcion_{idx}", 
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    driver.close()
                    driver.switch_to.window(ventana_principal)
                else:
                    # Captura para opciones que no abren ventana (como 'Copiar Link')
                    allure.attach(
                        driver.get_screenshot_as_png(), 
                        name=f"Accion_Interna_Opcion_{idx}", 
                        attachment_type=allure.attachment_type.PNG
                    )
            except:
                driver.switch_to.window(ventana_principal)
                continue

    # 5. CERRAR TOOLBAR
    with allure.step("5. Cerrar Toolbar y validación final"):
        xpath_cerrar = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[1]/div/button'
        boton_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar)))
        driver.execute_script("arguments[0].click();", boton_cerrar)
        time.sleep(1)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Toolbar_Final_Cerrado", 
            attachment_type=allure.attachment_type.PNG
        )
