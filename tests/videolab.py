import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Reproductor")
@allure.story("Validación VideoLab Completa")
def test_videolab_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    errores_acumulados = []

    # 1. NAVEGACIÓN Y LOCALIZACIÓN
    with allure.step("1. Navegar a Home y localizar VideoLab"):
        try:
            driver.get(url_home)
            # Limpieza de modales y cierre explícito del popup de notificaciones
            driver.execute_script("""
                const selectors = ['.tp-modal', '.tp-backdrop', '#didomi-host', '.notifications-popup', '.fc-ab-root'];
                selectors.forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
                document.body.classList.remove('tp-modal-open');
                
                // Intento cerrar el popup de alertas si existe por texto de botón
                const botones = Array.from(document.querySelectorAll('button'));
                const btnCerrar = botones.find(b => b.textContent.includes('MÁS TARDE') || b.textContent.includes('ACEPTAR'));
                if (btnCerrar) btnCerrar.click();
            """)
            
            xpath_contenedor = '//*[@id="fusion-app"]/div[12]/main/div[17]/div'
            contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_contenedor)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
            time.sleep(2)
        except Exception as e:
            errores_acumulados.append(f"Paso 1: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="1_Localizar_VideoLab", attachment_type=allure.attachment_type.PNG)

    # 2. APERTURA
    with allure.step("2. Abrir VideoLab"):
        try:
            xpath_primer_video = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[2]/div[2]/div/div/div/div[1]/div/a'
            btn_video = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_primer_video)))
            driver.execute_script("arguments[0].click();", btn_video)
            time.sleep(3)
        except Exception as e:
            errores_acumulados.append(f"Paso 2: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_VideoLab_Abierto", attachment_type=allure.attachment_type.PNG)

    # 3. OCULTAR
    with allure.step("3. Click en botón Ocultar"):
        try:
            xpath_ocultar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[1]/button'
            btn_ocultar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ocultar)))
            btn_ocultar.click()
            time.sleep(1)
        except Exception as e:
            errores_acumulados.append(f"Paso 3: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="3_Ocultar_Controles", attachment_type=allure.attachment_type.PNG)

    # 4. REACTIVAR (INDISPENSABLE PARA LOS DEMÁS)
    with allure.step("4. Re-activar controles para interactuar"):
        try:
            xpath_ocultar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[1]/button'
            btn_reactivar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ocultar)))
            btn_reactivar.click()
            time.sleep(1)
        except Exception as e:
            errores_acumulados.append(f"Paso 4: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="4_Controles_Visibles", attachment_type=allure.attachment_type.PNG)

    # 5. ACTIVAR SONIDO
    with allure.step("5. Probar botón Activar Sonido"):
        try:
            xpath_sonido = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/button[1]'
            btn_sonido = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sonido)))
            btn_sonido.click()
            time.sleep(1)
        except Exception as e:
            errores_acumulados.append(f"Paso 5: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="5_Activar_Sonido", attachment_type=allure.attachment_type.PNG)

    # 6. SIGUIENTE VIDEO
    with allure.step("6. Probar botón Siguiente Video"):
        try:
            xpath_sig = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[2]/button[2]'
            btn_sig = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sig)))
            btn_sig.click()
            time.sleep(2)
        except Exception as e:
            errores_acumulados.append(f"Paso 6: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="6_Siguiente_Video", attachment_type=allure.attachment_type.PNG)

    # 7. ANTERIOR VIDEO
    with allure.step("7. Probar botón Anterior Video"):
        try:
            xpath_ant = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[2]/button[1]'
            btn_ant = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ant)))
            btn_ant.click()
            time.sleep(2)
        except Exception as e:
            errores_acumulados.append(f"Paso 7: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="7_Anterior_Video", attachment_type=allure.attachment_type.PNG)

    # 8. FULLSCREEN
    with allure.step("8. Probar botón Fullscreen"):
        try:
            xpath_fs = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/button[2]'
            btn_fs = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fs)))
            btn_fs.click()
            time.sleep(2)
        except Exception as e:
            errores_acumulados.append(f"Paso 8: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="8_Fullscreen", attachment_type=allure.attachment_type.PNG)

    # 9. CERRAR VIDEOLAB
    with allure.step("9. Cerrar VideoLab"):
        try:
            xpath_cerrar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/button'
            btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar)))
            btn_cerrar.click()
            time.sleep(1)
        except Exception as e:
            errores_acumulados.append(f"Paso 9: {str(e)}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="9_Cerrar_VideoLab", attachment_type=allure.attachment_type.PNG)

    if errores_acumulados:
        pytest.fail(f"Fallos en VideoLab: {len(errores_acumulados)} pasos fallidos.")
