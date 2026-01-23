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
        print(f"INFO: Cargando artículo: {url_articulo}")

        # 1. LIMPIEZA PREVENTIVA
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

        # 2. LOCALIZAR Y HACER SCROLL HASTA EL TAG
        xpath_tag = '//*[@id="fusion-app"]/div[9]/div[1]/div[2]/a[2]'
        
        tag_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tag)))
        print("INFO: Se encontró el tag 'Nueva York' en el DOM.")
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_elemento)
        print("INFO: Scrolleando hasta la posición del tag.")
        time.sleep(1.5)

        # 3. HACER CLICK
        driver.execute_script("arguments[0].click();", tag_elemento)
        print("INFO: Se hizo click en el tag.")

        # 4. VALIDAR REDIRECCIÓN
        wait.until(EC.url_contains("/tags/nueva-york/"))
        
        url_actual = driver.current_url
        if url_actual == url_esperada:
            print(f"ÉXITO: Se validó el cambio a la URL correcta: {url_actual}")
        
        assert url_actual == url_esperada, f"Error: Se esperaba {url_esperada} pero se obtuvo {url_actual}"

    except Exception as e:
        print(f"ERROR: Falló la navegación por tags: {str(e)}")
        pytest.fail(f"Error en el test de Tags: {e}")

    finally:
        time.sleep(2)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Tag_Nueva_York", 
            attachment_type=allure.attachment_type.PNG
        )
