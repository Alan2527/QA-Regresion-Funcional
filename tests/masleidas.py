import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_most_read_component(driver):
    url_inicial = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    try:
        driver.get(url_inicial)
        wait = WebDriverWait(driver, 25)
        print(f"INFO: Navegando a la nota principal: {url_inicial}")
        
        # 1. Localizar contenedor
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        print("INFO: Componente 'Más Leídas' localizado y centrado.")
        time.sleep(2)
        
        # 2. Obtener los enlaces de las noticias
        # Buscamos los tags 'a' dentro de las historias para obtener las URLs
        stories = container.find_elements(By.CSS_SELECTOR, ".brick_most-read__story a")
        urls_ranking = [story.get_attribute('href') for story in stories[:5]] # Tomamos las primeras 5
        print(f"INFO: Se detectaron {len(urls_ranking)} enlaces en el ranking para validar.")

        # 3. Validar navegación de cada nota
        for idx, url_target in enumerate(urls_ranking, 1):
            print(f"PROBANDO NOTA #{idx}:")
            driver.get(url_target)
            
            # Esperamos a que la URL cargue
            wait.until(lambda d: d.current_url == url_target)
            print(f"   - Redirección exitosa a: {driver.current_url}")
            
            # Volvemos a la nota principal para seguir con la siguiente (o podrías ir directo a la siguiente URL)
            # Para mayor velocidad en este test, simplemente imprimimos el éxito y seguimos
            time.sleep(1) 

        print("ÉXITO: Todas las notas del ranking redirigen correctamente.")
        
    except Exception as e:
        print(f"ERROR: Falló la validación de navegación en Más Leídas: {str(e)}")
        raise e
        
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_MasLeidas", 
            attachment_type=allure.attachment_type.PNG
        )
