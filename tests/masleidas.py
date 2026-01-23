import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ranking_mas_leidas(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("https://tn.com.ar/")
    
    try:
        # 1. Localizar el ranking
        seccion_mas_leidas = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "most-read")))
        print("INFO: Sección 'Más Leídas' detectada en la Home.")

        # 2. Click en la segunda noticia del ranking
        xpath_noticia_2 = '//*[@id="fusion-app"]/main/div[1]/div/div[2]/div[1]/section/article[2]/div/a/h2'
        noticia = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_noticia_2)))
        titulo = noticia.text
        
        noticia.click()
        print(f"ÉXITO: Se navegó a la nota: '{titulo}' desde Más Leídas")

    except Exception as e:
        print(f"ERROR: No se pudo interactuar con Maás Leídas {e}")
        pytest.fail(f"Error en Más Leidas: {e}")
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="MasLeidas_Final", attachment_type=allure.attachment_type.PNG)
