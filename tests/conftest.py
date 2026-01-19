import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """
    Configuración del WebDriver para Chrome.
    """
    chrome_options = Options()
    # Configuraciones obligatorias para correr en GitHub Actions (sin interfaz gráfica)
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    
    yield driver
    
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar pantalla automáticamente en Allure tras la ejecución.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        # Buscamos el driver dentro de los argumentos del test
        driver_fixture = item.funcargs.get('driver')
        if driver_fixture:
            allure.attach(
                driver_fixture.get_screenshot_as_png(),
                name="screenshot_final",
                attachment_type=allure.attachment_type.PNG
            )
