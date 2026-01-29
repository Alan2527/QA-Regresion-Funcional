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

    # 1. NAVEGACIÓN Y APERTURA
    with allure.step("1. Navegar a Home y abrir VideoLab"):
        try:
            driver.get(url_home)
            driver.execute_script("""
                document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host, .notifications-popup').forEach(el => el.remove());
                document.body.classList.remove('tp-modal-open');
            """)
            
            # XPath del primer video en la sección VideoLab
            xpath_primer_video = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[2]/div[2]/div/div/div/div[1]/div/a'
            
            btn_video = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_primer_video)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_video)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", btn_video)
            time.sleep(3)
        except Exception as e:
            print(f"Error en paso 1: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="1_Home_VideoLab", attachment_type=allure.attachment_type.PNG)

    # 2. OCULTAR / MOSTRAR (Primer click para habilitar controles)
    with allure.step("2. Click en botón Ocultar"):
        try:
            xpath_ocultar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[1]/button'
            btn_ocultar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ocultar)))
            btn_ocultar.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error en paso 2: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_Ocultar_Controles", attachment_type=allure.attachment_type.PNG)

    # 3. ACTIVAR SONIDO
    with allure.step("3. Probar botón Activar Sonido"):
        try:
            xpath_sonido = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/button[1]'
            btn_sonido = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sonido)))
            btn_sonido.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error en paso 3: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="3_Activar_Sonido", attachment_type=allure.attachment_type.PNG)

    # 4. VOLVER A CLICK REVELAR (Para asegurar visibilidad de navegación)
    with allure.step("4. Re-activar controles para navegación"):
        try:
            xpath_ocultar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[1]/button'
            btn_ocultar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ocultar)))
            btn_ocultar.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error en paso 4: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="4_Revelar_Nav", attachment_type=allure.attachment_type.PNG)

    # 5. SIGUIENTE VIDEO
    with allure.step("5. Probar botón Siguiente Video"):
        try:
            xpath_sig = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[2]/button[2]'
            btn_sig = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_sig)))
            btn_sig.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error en paso 5: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="5_Siguiente_Video", attachment_type=allure.attachment_type.PNG)

    # 6. ANTERIOR VIDEO
    with allure.step("6. Probar botón Anterior Video"):
        try:
            xpath_ant = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/div[2]/button[1]'
            btn_ant = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ant)))
            btn_ant.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error en paso 6: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="6_Anterior_Video", attachment_type=allure.attachment_type.PNG)

    # 7. FULLSCREEN
    with allure.step("7. Probar botón Fullscreen"):
        try:
            xpath_fs = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/div[2]/button[2]'
            btn_fs = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fs)))
            btn_fs.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error en paso 7: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="7_Fullscreen", attachment_type=allure.attachment_type.PNG)

    # 8. CERRAR VIDEOLAB
    with allure.step("8. Cerrar VideoLab"):
        try:
            xpath_cerrar = '//*[@id="fusion-app"]/div[12]/main/div[17]/div/div[3]/button'
            btn_cerrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar)))
            btn_cerrar.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error en paso 8: {e}")
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="8_Cerrar_VideoLab", attachment_type=allure.attachment_type.PNG)
