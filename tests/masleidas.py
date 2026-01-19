import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_most_read_component(driver):
    """
    Test para validar la presencia y estructura del componente 'Más leídas'.
    """
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    driver.get(url)

    try:
        # 1. Validar Contenedor Principal
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_principal))
        )
        
        # Validar clases
        assert "brick_most-read" in container.get_attribute("class"), "Clase principal no encontrada"
        
        # 2. Validar el Título (h3)
        h3_title = container.find_element(By.CLASS_NAME, "section-title.font__display")
        assert h3_title.is_displayed(), "El título h3 no es visible"

        # 3. Validar el Contenedor de Noticias (body)
        news_body = container.find_element(By.CLASS_NAME, "brick_most-read__body")
        assert news_body.is_displayed(), "El contenedor de noticias no es visible"

        # 4. Validar presencia de noticias
        stories = news_body.find_elements(By.CLASS_NAME, "brick_most-read__story")
        assert len(stories) > 0, "No se encontraron noticias dentro del componente"

        # --- AJUSTE PARA ALLURE ---
        # Adjuntamos captura manual para asegurar que aparezca en el reporte unificado
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Componente Mas Leidas",
            attachment_type=allure.attachment_type.PNG
        )

    except TimeoutException:
        pytest.fail("El componente principal 'Más leídas' no cargó a tiempo.")
    except Exception as e:
        pytest.fail(f"Error durante la validación del componente: {str(e)}")
