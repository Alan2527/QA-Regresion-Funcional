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
            time.sleep(1)
            driver.execute_script("arguments[0].click();", boton_share)
            # Esperar a que el menú se despliegue (validando el primer botón interno)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]')))
        except Exception as e:
            assert False, f"No se pudo abrir el toolbar: {e}"
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_Toolbar_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. VALIDACIÓN DE REDES SOCIALES
    with allure.step("3. Validación de URLs y ventanas externas"):
        redes = [
            {"nombre": "Facebook", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]', "esperado": "facebook.com"},
            {"nombre": "X (Twitter)", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]', "esperado": "x.com"},
            {"nombre": "Copiar Link", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]', "esperado": "TOOLTIP"},
            {"nombre": "WhatsApp", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]', "esperado": "whatsapp.com"},
            {"nombre": "Telegram", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]', "esperado": "telegram.me"}
        ]
        
        ventana_principal = driver.current_window_handle

        for red in redes:
            with allure.step(f"Probar {red['nombre']}"):
                try:
                    intentar_cerrar_popup()
                    boton = driver.find_element(By.XPATH, red['xpath'])
                    
                    if red['esperado'] == "TOOLTIP":
                        driver.execute_script("arguments[0].click();", boton)
                        # CAPTURA RELÁMPAGO: Inmediata para atrapar el tooltip antes que desaparezca
                        allure.attach(driver.get_screenshot_as_png(), name="Captura_Tooltip_Copiado", attachment_type=allure.attachment_type.PNG)
                        continue

                    # Click para redes sociales
                    driver.execute_script("arguments[0].click();", boton)
                    
                    # ESPERA DINÁMICA A LA NUEVA VENTANA (Máximo 10 seg)
                    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
                    
                    nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                    driver.switch_to.window(nueva_ventana)
                    
                    # ESPERA A QUE LA URL SEA LA CORRECTA (Evita el about:blank o redirecciones de TN)
                    dominio = red['esperado'].split('.')[0]
                    WebDriverWait(driver, 10).until(EC.url_contains(dominio))
                    
                    url_actual = driver.current_url
                    allure.attach(driver.get_screenshot_as_png(), name=f"Ventana_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                    
                    if red['esperado'] not in url_actual.lower():
                        errores_acumulados.append(f"URL incorrecta en {red['nombre']}: {url_actual}")
                    
                    driver.close()
                    driver.switch_to.window(ventana_principal)

                except Exception as e:
                    errores_acumulados.append(f"Fallo en {red['nombre']}: {str(e)}")
                    # Asegurar volver a la principal si algo falla dentro de la ventana nueva
                    if len(driver.window_handles) > 1:
                        driver.close()
                    driver.switch_to.window(ventana_principal)

    # 4. CERRAR TOOLBAR
    with allure.step("4. Cerrar Toolbar y validación final"):
        try:
            xpath_cerrar = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[1]/div/button'
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_cerrar))
        except:
            pass
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="4_Resultado_Final", attachment_type=allure.attachment_type.PNG)

    if errores_acumulados:
        pytest.fail(f"Se detectaron {len(errores_acumulados)} fallos en ShareToolbar: {errores_acumulados}")
