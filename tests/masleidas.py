import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_most_read_component(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 25)
        print(f"INFO: Navegando a la nota: {url}")
        
        # Tu XPath exacto
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        print("INFO: Contenedor principal de 'Más Leídas' detectado en el DOM.")
        
        # Centrar elemento y esperar a que la UI se estabilice
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        print("INFO: Haciendo scroll hacia el componente 'Más Leídas'.")
        time.sleep(2)
        
        # Validar noticias
        stories = container.find_elements(By.CLASS_NAME, "brick_most-read__story")
        cantidad_detectada = len(stories)
        
        print(f"INFO: Se detectaron {cantidad_detectada} noticias en el ranking.")
        
        # Iterar brevemente para mostrar los títulos en el log (opcional pero muy útil)
        for idx, story in enumerate(stories[:5], 1):
             print(f"   - Noticia #{idx}: {story.text[:50]}...")

        assert cantidad_detectada > 0, "No se encontraron noticias en el componente 'Más Leídas'"
        print("ÉXITO: Validación de noticias completada correctamente.")
        
    except Exception as e:
        print(f"ERROR: Falló la validación del componente Más Leídas: {str(e)}")
        raise e
        
    finally:
        # La captura siempre se adjunta, incluso si falla el assert
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_MasLeidas", 
            attachment_type=allure.attachment_type.PNG
        )
