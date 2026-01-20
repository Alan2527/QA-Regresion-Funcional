import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Componente Más Leídas")
@allure.story("Visualización de noticias populares")
def test_most_read_component(driver):
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        
        # Esperamos al contenedor principal del componente
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "brick_most-read")))
        
        # Validamos que existan artículos dentro
        stories = container.find_elements(By.CSS_SELECTOR, "article, .brick_most-read__story")
        assert len(stories) > 0, "No se encontraron noticias en el ranking de lo más leído"
        
    finally:
        # Captura de pantalla: se verá el CSS (estilos) pero cuadros vacíos donde van las imágenes
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_MasLeidas", 
            attachment_type=allure.attachment_type.PNG
        )
