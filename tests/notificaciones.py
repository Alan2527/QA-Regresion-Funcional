import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_configuracion_notificaciones(driver):
    """
    Test para validar la configuración de temas y la recepción de notificaciones.
    """
    url = "https://tn.com.ar/"
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # 1. Hacer clic en el botón de la campana para abrir el dropdown
    btn_campana_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div/button'
    btn_campana = wait.until(EC.element_to_be_clickable((By.XPATH, btn_campana_xpath)))
    btn_campana.click()

    # 2. Hacer clic en el botón de Settings dentro del dropdown
    btn_settings_xpath = '//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/button'
    btn_settings = wait.until(EC.element_to_be_clickable((By.XPATH, btn_settings_xpath)))
    btn_settings.click()

    # 3. Interactuar con los 10 switches de temas
    # Como requiere scroll, localizamos el contenedor de los temas
    for i in range(1, 11):
        switch_xpath = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
        switch_element = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
        
        # Realizar scroll hasta el elemento para asegurar que sea visible y clickeable
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch_element)
        time.sleep(0.5) # Breve pausa para estabilidad del scroll
        
        # Clic mediante JavaScript para evitar problemas de interceptación por el header
        driver.execute_script("arguments[0].click();", switch_element)

    # 4. Volver a clickear la campana para cerrar el dropdown
    btn_campana.click()
    
    # Esperar un momento para que el DOM se actualice tras cerrar
    time.sleep(2)

    # 5. Volver a abrir la campana para validar el contenido
    btn_campana.click()

    # 6. Validación Final: Verificar si hay notificaciones o el mensaje de 'No tenés nuevas'
    try:
        # Opción A: Buscar el mensaje de "No tenés notificaciones nuevas"
        # Basado en tus capturas, este texto aparece cuando no hay contenido
        mensaje_vacio = driver.find_elements(By.XPATH, "//*[contains(text(), 'No tenés notificaciones nuevas')]")
        
        # Opción B: Buscar estructura de notificaciones (h3 y p)
        elementos_noticia = driver.find_elements(By.CLASS_NAME, "segment.font__subtitle")
        descripciones_noticia = driver.find_elements(By.CLASS_NAME, "item-title.font__subtitle-regular")

        if mensaje_vacio:
            print("Validación exitosa: Se visualiza el mensaje de 'No tenés notificaciones nuevas'.")
            assert True
        elif len(elementos_noticia) > 0 and len(descripciones_noticia) > 0:
            print(f"Validación exitosa: Se visualizaron {len(elementos_noticia)} notificaciones.")
            assert True
        else:
            pytest.fail("No se encontró ni el mensaje de vacío ni las notificaciones esperadas.")
            
    except Exception as e:
        pytest.fail(f"Error durante la validación final: {str(e)}")
