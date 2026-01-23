import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ranking_mas_leidas(driver):
    # Usamos la URL válida de la nota
    url_nota = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-historia/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_nota)
        print(f"INFO: Cargando la nota para buscar el ranking...")

        # 1. Buscamos el contenedor de Más Leídas (usamos un selector más flexible)
        # Buscamos por el texto del encabezado del widget
        seccion = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Lo más leído')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seccion)
        print("INFO: Sección 'Lo más leído' encontrada en la nota.")

        # 2. Click en la segunda noticia del ranking
        # El XPath //article[2] es más directo para el segundo elemento del ranking
        xpath_nota_2 = "(//section[contains(@class, 'most-read')]//article)[2]//h2"
        noticia_click = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_nota_2)))
        
        titulo_detectado = noticia_click.text
        driver.execute_script("arguments[0].click();", noticia_click)
        print(f"ÉXITO: Se hizo clic en la nota ranking #2: '{titulo_detectado}'")

    except Exception as e:
        print(f"ERROR: No se encontró el ranking en esta URL: {e}")
        pytest.fail(f"Fallo en Mas Leidas: {e}")
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="MasLeidas_Final", attachment_type=allure.attachment_type.PNG)
