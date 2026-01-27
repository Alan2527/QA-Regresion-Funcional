import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Componente Lateral")
@allure.story("Validación de Ranking Más Leídas")
def test_most_read_component(driver):
    # BLOQUEO DE ADS E IMÁGENES (Solo para este test)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        "urls": [
            "*.googlesyndication.com", "*.doubleclick.net", "*.ads*", 
            "*.image*", "*.jpg", "*.png", "*.gif", "*.jpeg", "*.webp"
        ]
    })
    driver.execute_cdp_cmd('Network.enable', {})

    url_inicial = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN
    with allure.step("1. Navegación a la nota principal"):
        driver.get(url_inicial)
        xpath_principal = '//*[@id="fusion-app"]/div[9]/aside/div[2]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_principal)))

    # 2. CENTRAR COMPONENTE (Paso pedido)
    with allure.step("2. Centrar el componente"):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(2)

    # 3. TOMAR LA CAPTURA (Paso pedido - Único con captura)
    with allure.step("3. Tomar la captura"):
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Ranking_MasLeidas", 
            attachment_type=allure.attachment_type.PNG
        )

    # 4. VALIDACIÓN FINAL
    with allure.step("4. Validar navegación de las notas"):
        titulares = container.find_elements(By.CSS_SELECTOR, "h2.card__headline a")
        urls_ranking = [t.get_attribute('href') for t in titulares[:5]]
        
        for url_target in urls_ranking:
            driver.get(url_target)
            wait.until(lambda d: d.current_url == url_target)
