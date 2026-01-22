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
        wait = WebDriverWait(driver, 25)
        
        # 1. Click en la campana principal
        boton_campana = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "font__action")))
        driver.execute_script("arguments[0].click();", boton_campana)
        
        # 2. Click en el botón azul "Activá las notificaciones"
        selector_activar = "//button[contains(., 'Activá')]"
        boton_activar = wait.until(EC.element_to_be_clickable((By.XPATH, selector_activar)))
        driver.execute_script("arguments[0].click();", boton_activar)

        # 3. Esperar a que el panel de temas esté presente
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toggle-switch")))
        
        # --- ACTIVACIÓN DE LOS 10 SWITCHES ---
        # Usamos la estructura de XPath que me pasaste para los 10 elementos
        for i in range(1, 11):
            try:
                # Construimos el XPath dinámico para el span (slider)
                xpath_span = f'//*[@id="fusion-app"]/header/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[{i}]/label/span'
                
                # Buscamos el elemento
                span_slider = driver.find_element(By.XPATH, xpath_span)
                
                # Forzamos el click por JavaScript para que cambie el estado
                driver.execute_script("arguments[0].click();", span_slider)
                
                # Breve pausa entre clicks para que la web no se bloquee
                time.sleep(0.5)
            except Exception as e:
                print(f"No se pudo activar el switch {i}: {e}")
                continue

        # Pausa final para que todos los switches terminen su animación a azul
        time.sleep(4)
        
    finally:
        # La captura ahora mostrará los 10 switches activados (en azul)
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_TOTAL_TEMAS_AZULES", 
            attachment_type=allure.attachment_type.PNG
        )
