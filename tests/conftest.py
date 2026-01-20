import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    """
    Configuración optimizada de Selenium para GitHub Actions.
    Ejecuta una instancia limpia por cada test y libera memoria al finalizar.
    """
    chrome_options = Options()
    
    # --- MODO CI (Headless y Optimización de Recursos) ---
    chrome_options.add_argument("--headless=new") # Modo headless moderno
    chrome_options.add_argument("--no-sandbox") # Requerido para entornos Linux/Docker
    chrome_options.add_argument("--disable-dev-shm-usage") # Usa /tmp en lugar de RAM compartida
    chrome_options.add_argument("--disable-gpu") # Desactiva aceleración de hardware
    
    # --- OPTIMIZACIÓN DE CARGA Y MEMORIA ---
    # Desactivamos la carga de imágenes para que los tests sean mucho más rápidos
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Evita que Chrome consuma CPU innecesaria en extensiones o logs
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_argument("--silent")

    # Definir tamaño de ventana estándar
    chrome_options.add_argument("--window-size=1920,1080")

    # Inicializar el Driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Timeouts de seguridad para evitar que el test se cuelgue infinitamente
    driver.set_page_load_timeout(30) # Máximo 30 seg para cargar la página
    driver.implicitly_wait(5)        # Espera implícita corta

    yield driver

    # --- CIERRE Y LIMPIEZA TOTAL (Tu consejo clave) ---
    try:
        driver.close() # Cierra la pestaña actual
        driver.quit()  # Cierra el proceso del navegador y el ChromeDriver
    except Exception as e:
        print(f"Error al cerrar el driver: {e}")
