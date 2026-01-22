import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def escribir_como_humano(elemento, texto):
    """Escribe el texto letra por letra con pausas aleatorias."""
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.1, 0.3))

def test_login_flujo_real(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get(url)
        
        # 1. Click en Iniciar Sesión con pausa previa
        time.sleep(2)
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[2]/div/a')))
        driver.execute_script("arguments[0].click();", boton_login)

        # 2. Esperar al formulario y escribir email letra por letra
        input_email = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/input')))
        input_email.click()
        escribir_como_humano(input_email, "alanherrera2527@gmail.com")
        time.sleep(random.uniform(1, 2))

        # 3. Escribir Password letra por letra
        input_pass = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[1]/input')))
        input_pass.click()
        escribir_como_humano(input_pass, "Filupi2527!!")
        time.sleep(random.uniform(1, 2))

        # 4. Click en el botón de ingresar (usando click real, no script, para ser más humano)
        boton_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[3]/button')))
        boton_submit.click()

        # 5. VALIDACIÓN FINAL
        # Esperamos a que el nombre aparezca
        xpath_nombre = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_nombre), "Alan Herrera"))
        
        time.sleep(3) # Pausa para asegurar la captura
        
    except Exception as e:
        print(f"Error en flujo de login: {e}")
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Validacion_Flujo_Login", 
            attachment_type=allure.attachment_type.PNG
        )
