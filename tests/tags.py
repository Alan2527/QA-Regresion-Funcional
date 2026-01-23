import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_navegacion_tags(driver):
    url_articulo = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-historia/"
    url_esperada = "https://tn.com.ar/tags/nueva-york/"
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url_articulo)

        # 1. LIMPIEZA PREVENTIVA
        # Eliminamos posibles pop-ups que bloqueen el scroll o el click
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

        # 2. LOCALIZAR Y HACER SCROLL HASTA EL TAG
        # Usamos el XPath exacto que pediste
        xpath_tag = '//*[@id="fusion-app"]/div[9]/div[1]/div[2]/a[2]'
        
        # Esperamos a que el elemento exista en el DOM
        tag_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tag)))
        
        # Scroll inteligente: lo centra en la pantalla
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_elemento)
        time.sleep(1.5) # Pausa para que el scroll se estabilice

        # 3. HACER CLICK
        # Usamos JS click para evitar que cualquier banner invisible intercepte el click
        driver.execute_script("arguments[0].click();", tag_elemento)

        # 4. VALIDAR REDIRECCIÓN
        # Esperamos hasta que la URL contenga '/tags/nueva-york/'
        wait.until(EC.url_contains("/tags/nueva-york/"))
        
        url_actual = driver.current_url
        print(f"Redirección exitosa a: {url_actual}")
        
        assert url_actual == url_esperada, f"Error: Se esperaba {url_esperada} pero se obtuvo {url_actual}"

    except Exception as e:
        pytest.fail(f"Error en el test de Tags: {e}")

    finally:
        # 5. CAPTURA DE PANTALLA EN LA URL DE DESTINO
        time.sleep(2) # Tiempo para que cargue la lista de noticias del tag
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Tag_Nueva_York", 
            attachment_type=allure.attachment_type.PNG
        )
