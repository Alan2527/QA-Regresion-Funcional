import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Social Share")
@allure.story("Validación de Toolbar de Compartir")
def test_share_toolbar_validation(driver):
    # BLOQUEO DE ADS PARA ESTABILIDAD
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": ["*.googlesyndication.com", "*.doubleclick.net", "*.ads*", "*.adnxs*", "*.analytics*", "*.taboola*"]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url_nota = "https://tn.com.ar/turismo/2026/01/22/ni-chivilcoy-ni-chascomus-el-pueblo-a-1-hora-de-buenos-aires-con-una-laguna-parrillas-y-campings/"
    wait = WebDriverWait(driver, 25)
    errores_acumulados = []
    xpath_popup_cancel = '//*[@id="onesignal-slidedown-cancel-button"]'

    def intentar_cerrar_popup():
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath_popup_cancel))).click()
        except:
            pass

    # 1. NAVEGACIÓN Y LIMPIEZA
    with allure.step("1. Navegación y limpieza"):
        driver.get(url_nota)
        intentar_cerrar_popup()
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)
        allure.attach(driver.get_screenshot_as_png(), name="1_Navegacion", attachment_type=allure.attachment_type.PNG)

    # 2. LOCALIZAR Y ABRIR TOOLBAR
    with allure.step("2. Localizar y abrir Sharetoolbar"):
        try:
            xpath_abrir = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div/button'
            boton_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_share)
            
            driver.execute_script("arguments[0].click();", boton_share)
            time.sleep(3) # Espera necesaria solo para el despliegue inicial
            
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]')))
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="Error_Apertura_Toolbar", attachment_type=allure.attachment_type.PNG)
            assert False, f"No se pudo abrir el toolbar: {e}"
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_Toolbar_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. VALIDACIÓN DE REDES SOCIALES
    with allure.step("3. Validación de apertura de ventanas"):
        redes = [
            {"nombre": "Facebook", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]'},
            {"nombre": "X (Twitter)", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]'},
            {"nombre": "Copiar Link", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]', "is_tooltip": True},
            {"nombre": "WhatsApp", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]'},
            {"nombre": "Telegram", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]'}
        ]
        
        ventana_principal = driver.current_window_handle

        for red in redes:
            with allure.step(f"Probar {red['nombre']}"):
                try:
                    intentar_cerrar_popup()
                    boton = wait.until(EC.element_to_be_clickable((By.XPATH, red['xpath'])))
                    
                    if red.get("is_tooltip"):
                        # Acción inmediata: Click y captura sin sleeps
                        driver.execute_script("arguments[0].click();", boton)
                        allure.attach(driver.get_screenshot_as_png(), name=f"Captura_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                        continue

                    # Lógica para ventanas externas (Facebook, X, WhatsApp, Telegram)
                    ventana_abierta = False
                    for intento in range(2):
                        driver.execute_script("arguments[0].click();", boton)
                        try:
                            WebDriverWait(driver, 7).until(lambda d: len(d.window_handles) > 1)
                            ventana_abierta = True
                            break 
                        except:
                            continue
                    
                    if not ventana_abierta:
                        raise Exception(f"No se abrió la ventana de {red['nombre']}")

                    nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                    driver.switch_to.window(nueva_ventana)
                    
                    # Para las redes sociales sí esperamos a que cargue el contenido
                    time.sleep(4) 
                    allure.attach(driver.get_screenshot_as_png(), name=f"Ventana_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                    
                    driver.close()
                    driver.switch_to.window(ventana_principal)

                except Exception as e:
                    allure.attach(driver.get_screenshot_as_png(), name=f"ERROR_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                    errores_acumulados.append(f"Fallo en {red['nombre']}: {str(e)}")
                    if len(driver.window_handles) > 1:
                        driver.close()
                    driver.switch_to.window(ventana_principal)

    # 4. FINALIZACIÓN
    if errores_acumulados:
        pytest.fail(f"Se detectaron {len(errores_acumulados)} fallos en ShareToolbar")
