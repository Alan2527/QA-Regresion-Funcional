import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    url = "https://tn.com.ar/"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        # Usamos la clase "font__action" que me pasaste
        # También podrías usar el XPath: '//*[@id="fusion-app"]/header/div/div[1]/div/button'
        selector_campana = ".font__action"
        boton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_campana)))

        # Forzamos el clic por JS para que sea infalible contra anuncios
        driver.execute_script("arguments[0].click();", boton)

        # Espera necesaria para que la animación del dropdown termine antes de la foto
        time.sleep(2) 

        # CAPTURA FINAL: Ahora sí con el menú desplegado
        allure.attach(driver.get_screenshot_as_png(), name="Dropdown_Notif_Abierto", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Error_Notificaciones", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"No se pudo abrir el dropdown: {e}")
