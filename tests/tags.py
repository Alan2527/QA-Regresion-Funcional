import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Navegación")
@allure.story("Validación de Tags")
def test_navegacion_tags(driver):
    # Corregí el ligero error en "history" por "historia" en la URL si fuera necesario, 
    # pero mantenemos la que pasaste para asegurar compatibilidad.
    url_articulo = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-historia/"
    url_esperada = "https://tn.com.ar/tags/nueva-york/"
    wait = WebDriverWait(driver, 25)

    # 1. CARGA Y LIMPIEZA
    with allure.step("1. Cargar artículo y limpiar modales"):
        driver.get(url_articulo)
        
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host, .notifications-popup').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

    # 2. LOCALIZACIÓN ROBUSTA
    with allure.step("2. Localizar Tag 'Nueva York'"):
        # Usamos un selector que busca el enlace que contiene el texto exacto, 
        # esto es 100 veces más estable que div[9]
        xpath_tag_robusto = "//a[contains(@href, '/tags/nueva-york/')]"
        
        try:
            tag_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tag_robusto)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_elemento)
            time.sleep(2)
        except:
            # Si falla, intentamos buscar cualquier tag dentro del contenedor de tags
            tag_elemento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.tags__container a, .tags a")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_elemento)
        
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Ubicacion_Tag", 
            attachment_type=allure.attachment_type.PNG
        )

    # 3. CLICK Y REDIRECCIÓN
    with allure.step("3. Ejecutar click y validar destino"):
        driver.execute_script("arguments[0].click();", tag_elemento)
        
        # Esperar hasta que la URL sea la de tags
        wait.until(EC.url_contains("/tags/"))
        
        # Pequeña pausa para que cargue el contenido de la página de tags
        time.sleep(4)
        
        url_actual = driver.current_url
        
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Pagina_Destino", 
            attachment_type=allure.attachment_type.PNG
        )
        
        # Validamos que al menos contenga el tag en la URL
        assert "/tags/nueva-york/" in url_actual, f"Se esperaba tag Nueva York, pero se llegó a: {url_actual}"
