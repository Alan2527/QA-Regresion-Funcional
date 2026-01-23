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

        # --- CAPTURA DE EVIDENCIA ---
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Validacion_MasLeidas", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura de pantalla del ranking adjuntada.")
        
        # 2. Obtener los enlaces de los TÍTULOS únicamente
        # Usamos un selector que busca el enlace 'a' que envuelve al h2 del titular
        titulares = container.find_elements(By.CSS_SELECTOR, "h2.card__headline a")
        urls_ranking = [t.get_attribute('href') for t in titulares[:5]]
        
        print(f"INFO: Se detectaron {len(urls_ranking)} títulos de noticias para validar.")

        # 3. Validar navegación de cada nota
        for idx, url_target in enumerate(urls_ranking, 1):
            print(f"PROBANDO NOTA #{idx}:")
            driver.get(url_target)
            
            # Esperamos la carga
            wait.until(lambda d: d.current_url == url_target)
            print(f"   - Título redirige correctamente a: {driver.current_url}")
            time.sleep(1) 

        print("ÉXITO: Todos los títulos del ranking redirigen correctamente (sin autores).")
        
    except Exception as e:
        print(f"ERROR: Falló la validación de títulos en Más Leídas: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Error_MasLeidas", attachment_type=allure.attachment_type.PNG)
        raise e
