import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Componente Lateral")
@allure.story("Validación de Ranking Más Leídas")
def test_most_read_component(driver):
    # BLOQUEO DE ADS E IMÁGENES (Optimización)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "*.googlesyndication.com", "*.doubleclick.net", "*.ads*", 
            "*.image*", "*.jpg", "*.png", "*.gif", "*.jpeg", "*.webp"
        ]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url_inicial = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    wait = WebDriverWait(driver, 25)
    errores_acumulados = []
    xpath_popup_cancel = '//*[@id="onesignal-slidedown-cancel-button"]'

    def intentar_cerrar_popup():
        try:
            wait_p = WebDriverWait(driver, 2)
            wait_p.until(EC.element_to_be_clickable((By.XPATH, xpath_popup_cancel))).click()
        except:
            pass

    # 1. NAVEGACIÓN
    with allure.step("1. Navegación a la nota principal"):
        try:
            driver.get(url_inicial)
            intentar_cerrar_popup()
            driver.execute_script("document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());")
            xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
            container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        except Exception as e:
            errores_acumulados.append(f"Error inicial: {e}")
            assert False, f"No se pudo cargar la nota principal: {e}"
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="1_Nota_Principal", attachment_type=allure.attachment_type.PNG)

    # 2. CENTRAR COMPONENTE
    with allure.step("2. Centrar el componente Más Leídas"):
        try:
            xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
            container = driver.find_element(By.XPATH, xpath_principal)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
            time.sleep(2)
        except Exception as e:
            errores_acumulados.append(f"Error al centrar: {e}")
            try: assert False, f"Error al centrar: {e}"
            except AssertionError: pass
        finally:
            allure.attach(driver.get_screenshot_as_png(), name="2_Componente_Centrado", attachment_type=allure.attachment_type.PNG)

    # 3. OBTENER URLS DEL RANKING
    titulares = container.find_elements(By.CSS_SELECTOR, "h2.card__headline a")
    urls_ranking = [t.get_attribute('href') for t in titulares[:5]]

    # 4. PRUEBA DINÁMICA DE CADA ENLACE
    for i, url_target in enumerate(urls_ranking, start=1):
        with allure.step(f"Validar nota ranking #{i}"):
            try:
                intentar_cerrar_popup()
                driver.get(url_target)
                # Validamos que la URL actual coincida o contenga parte de la esperada
                wait.until(lambda d: url_target in d.current_url)
                time.sleep(1)
            except Exception as e:
                errores_acumulados.append(f"Error en nota {i} ({url_target}): {e}")
                try: assert False, f"Fallo al navegar a la nota {i}: {e}"
                except AssertionError: pass
            finally:
                allure.attach(driver.get_screenshot_as_png(), name=f"Captura_Nota_{i}", attachment_type=allure.attachment_type.PNG)

    # VALIDACIÓN FINAL DEL TEST
    if errores_acumulados:
        pytest.fail(f"Se detectaron {len(errores_acumulados)} fallos en Más Leídas.")
