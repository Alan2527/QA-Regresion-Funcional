import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_configuracion_notificaciones(driver):
    """
    Test para validar la configuración de temas y la recepción de notificaciones.
    """
    # URL del artículo proporcionado
    url = "https://tn.com.ar/politica/2026/01/19/el-gobierno-anuncio-que-tv-publica-transmitira-los-partidos-de-la-seleccion-argentina-durante-el-mundial-2026/"
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # 1. Hacer clic en el botón de la campana (Xpath proporcionado)
    btn_campana_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div/button'
    btn_campana = wait.until(EC.element_to_be_clickable((By.XPATH, btn_campana_xpath)))
    btn_campana.click()

    # 2. Hacer clic en el botón de settings (Xpath proporcionado)
    btn_settings_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/button'
    btn_settings = wait.until(EC.element_to_be_clickable((By.XPATH, btn_settings_xpath)))
    btn_settings.click()

    # 3. Bucle para marcar/desmarcar los 10 temas con Scroll
    for i in range(1, 11):
        switch_xpath = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
        # Localizamos el switch
        switch_element = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
        
        # Realizar scroll para que el elemento esté centrado y visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch_element)
        time.sleep(0.4) # Breve pausa para que el scroll se estabilice
        
        # Clic mediante JavaScript para evitar bloqueos del header sticky
        driver.execute_script("arguments[0].click();", switch_element)

    # 4. Volver a clickear en la campana para cerrar el dropdown
    btn_campana.click()
    time.sleep(1.5) # Espera a que la animación de cierre termine

    # 5. Volver a abrir para validar contenido final
    btn_campana.click()

    # 6. Captura de pantalla manual para Allure (Asegura que se vea el dropdown abierto)
    allure.attach(
        driver.get_screenshot_as_png(),
        name="Estado Dropdown Notificaciones",
        attachment_type=allure.attachment_type.PNG
    )

    # 7. Validación Final: Notificaciones presentes o mensaje de "No tenés nuevas"
    try:
        # Buscamos mensaje de vacío basado en tus capturas
        vacio = driver.find_elements(By.XPATH, "//*[contains(text(), 'No tenés notificaciones nuevas')]")
        
        # Buscamos clases h3 y p especificadas para cuando hay noticias
        noticias_h3 = driver.find_elements(By.CLASS_NAME, "segment.font__subtitle")
        noticias_p = driver.find_elements(By.CLASS_NAME, "item-title.font__subtitle-regular")

        if vacio:
            print("Validación exitosa: Se muestra el mensaje 'No tenés notificaciones nuevas'.")
            assert True
        elif len(noticias_h3) > 0:
            print(f"Validación exitosa: Se visualizaron {len(noticias_h3)} notificaciones activas.")
            assert True
        else:
            pytest.fail("No se encontró el contenido esperado en el dropdown de notificaciones.")
            
    except Exception as e:
        pytest.fail(f"Error en la validación: {str(e)}")
