import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Social Share")
@allure.story("Validación de Toolbar de Compartir")
def test_share_toolbar_validation(driver):
    # BLOQUEO DE ADS
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
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath_popup_cancel))).click()
        except:
            pass

    # 1. NAVEGACIÓN Y LIMPIEZA
    with allure.step("1. Navegación, limpieza de popups y ads"):
        try:
            driver.get(url_nota)
            intentar_cerrar_popup()
            driver.execute_script("""
                document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
                document.body.classList.remove('tp-modal-open');
            """)
        except Exception as e:
            errores_acumulados.append(f"Paso 1: {e}")
            assert False, f"Fallo al cargar nota: {e}"
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="1_Navegacion", attachment_type=allure.attachment_type.PNG)

    # 2. LOCALIZAR TOOLBAR
    with allure.step("2. Localizar y abrir Sharetoolbar"):
        try:
            intentar_cerrar_popup()
            xpath_abrir = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div/button'
            boton_share = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_abrir)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_share)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", boton_share)
            # Esperar a que el menú se despliegue
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]')))
        except Exception as e:
            errores_acumulados.append(f"Paso 2: {e}")
            try: assert False, f"Fallo al abrir toolbar: {e}"
            except AssertionError: pass
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_Toolbar_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. VALIDACIÓN DE REDES SOCIALES
    with allure.step("3. Validación de URLs y capturas por red social"):
        redes = [
            {"nombre": "Facebook", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[1]', "esperado": "facebook.com"},
            {"nombre": "X (Twitter)", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[2]', "esperado": "x.com"},
            {"nombre": "Copiar Link", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[3]', "esperado": None},
            {"nombre": "WhatsApp", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[4]', "esperado": "whatsapp.com"},
            {"nombre": "Telegram", "xpath": '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/button[5]', "esperado": "telegram.me"}
        ]
        
        ventana_principal = driver.current_window_handle

        for red in redes:
            with allure.step(f"Probar {red['nombre']}"):
                try:
                    intentar_cerrar_popup()
                    boton = driver.find_element(By.XPATH, red['xpath'])
                    driver.execute_script("arguments[0].click();", boton)
                    time.sleep(3) # Tiempo para que abra la ventana

                    if len(driver.window_handles) > 1:
                        nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                        driver.switch_to.window(nueva_ventana)
                        
                        url_actual = driver.current_url
                        # Captura de la ventana externa
                        allure.attach(driver.get_screenshot_as_png(), name=f"Ventana_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                        
                        # Validación de URL
                        if red['esperado'] and red['esperado'] not in url_actual.lower():
                            errores_acumulados.append(f"URL incorrecta en {red['nombre']}: se esperaba {red['esperado']} pero se obtuvo {url_actual}")
                            assert False, f"URL de {red['nombre']} no contiene {red['esperado']}"
                        
                        driver.close()
                        driver.switch_to.window(ventana_principal)
                    else:
                        # Si no abre ventana (como Copiar Link)
                        allure.attach(driver.get_screenshot_as_png(), name=f"Accion_{red['nombre']}", attachment_type=allure.attachment_type.PNG)
                        if red['esperado']: # Si esperábamos ventana y no abrió
                             errores_acumulados.append(f"{red['nombre']} no abrió ventana externa.")
                             assert False, f"{red['nombre']} no abrió ventana externa."
                except Exception as e:
                    errores_acumulados.append(f"Error en {red['nombre']}: {str(e)}")
                    driver.switch_to.window(ventana_principal)
                    try: assert False, f"Error en {red['nombre']}: {e}"
                    except AssertionError: pass

    # 4. CERRAR TOOLBAR
    with allure.step("4. Cerrar Toolbar y validación final"):
        try:
            xpath_cerrar = '//*[@id="fusion-app"]/div[8]/div[1]/main/div[1]/div/div[3]/div/div[2]/div[1]/div/button'
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_cerrar))
            time.sleep(1)
        except Exception as e:
            errores_acumulados.append(f"Fallo al cerrar: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="4_Estado_Final", attachment_type=allure.attachment_type.PNG)

    if errores_acumulados:
        pytest.fail(f"Fallas detectadas en ShareToolbar: {len(errores_acumulados)}")
