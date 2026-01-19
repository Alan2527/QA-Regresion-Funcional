import pytest
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

    # 1. Validar Contenedor Principal por XPath y Clase
    try:
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_principal))
        )
        
        # Validar que tenga la clase correcta
        assert "brick_most-read" in container.get_attribute("class"), "Clase principal no encontrada"
        assert "brick_menor" in container.get_attribute("class"), "Clase secundaria no encontrada"
        
        # 2. Validar el Título (h3)
        h3_title = container.find_element(By.CLASS_NAME, "section-title.font__display")
        assert h3_title.is_displayed(), "El título h3 no es visible"
        assert "Las más leídas" in h3_title.text, f"Texto del título inesperado: {h3_title.text}"

        # 3. Validar la Línea Divisoria (div)
        divider = container.find_element(By.CLASS_NAME, "section-divider.top")
        assert divider.is_displayed(), "La línea divisora no es visible"

        # 4. Validar el Contenedor de Noticias (body)
        news_body = container.find_element(By.CLASS_NAME, "brick_most-read__body")
        assert news_body.is_displayed(), "El contenedor de noticias no es visible"

        # 5. Validar la presencia de al menos una noticia (story)
        stories = news_body.find_elements(By.CLASS_NAME, "brick_most-read__story")
        assert len(stories) > 0, "No se encontraron noticias dentro del componente"
        print(f"Se encontraron {len(stories)} noticias en el ranking.")

    except TimeoutException:
        pytest.fail("El componente principal 'Más leídas' no cargó a tiempo.")
    except Exception as e:
        pytest.fail(f"Error durante la validación del componente: {str(e)}")
