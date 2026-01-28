import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Navegación")
@allure.story("Validación de Tags")
def test_navegacion_tags(driver):
    url_articulo = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-history/"
    url_esperada = "https://tn.com.ar/tags/nueva-york/"
    wait = WebDriverWait(driver, 25)

    # 1. CARGA Y LIMPIEZA
    with allure.step("1. Cargar artículo y limpiar modales"):
        driver.get(url_articulo)
        
        # Limpieza de posibles bloqueos (intersticiales o banners)
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

    # 2. LOCALIZACIÓN Y SCROLL
    with allure.step("2. Localizar y scrollear hasta el Tag 'Nueva York'"):
        # XPath según tu estructura
        xpath_tag = '//*[@id="fusion-app"]/div[9]/div[1]/div[2]/a[2]'
        
        tag_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tag)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_elemento)
        time.sleep(2)

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Posicion_Tag", 
            attachment_type=allure.attachment_type.PNG
        )

    # 3. CLICK Y REDIRECCIÓN
    with allure.step("3. Hacer click en el tag y validar redirección"):
        driver.execute_script("arguments[0].click();", tag_elemento)
        
        # Esperar a que la URL cambie a la del tag
        wait.until(EC.url_contains("/tags/nueva-york/"))
        
        url_actual = driver.current_url
        
        # Captura de la página de destino (Tag page)
        time.sleep(3) 
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Pagina_Tag_Destino", 
            attachment_type=allure.attachment_type.PNG
        )
        
        assert url_actual == url_esperada, f"Se esperaba {url_esperada} pero se obtuvo {url_actual}"
