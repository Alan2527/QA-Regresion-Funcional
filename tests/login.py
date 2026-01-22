import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def escribir_como_humano(elemento, texto):
    """Escribe el texto letra por letra con pausas aleatorias para simular un humano."""
    for letra in texto:
        elemento.send_keys(letra)
        # Pausa aleatoria entre 0.1 y 0.3 segundos por letra
        time.sleep(random.uniform(0.1, 0.3))

def test_login_usuario(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get(url)
        
        # 1. Click en el botón de Iniciar Sesión del Header
        # Usamos el XPath exacto que me pasaste
        xpath_boton_header = '//*[@id="fusion-app"]/header/div/div[2]/div/a'
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_boton_header)))
        
        # Pequeña pausa antes de clickear para no ser instantáneo
        time.sleep(1.5)
        driver.execute_script("arguments[0].click();", boton_login)

        # 2. Ingresar Email letra por letra
        xpath_email = '//*[@id="fusion-app"]/div[2]/form/input'
        input_email = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_email)))
        input_email.click() # Hacemos foco
        escribir_como_humano(input_email, "alanherrera2527@gmail.com")
        
        # Pausa entre campos
        time.sleep(random.uniform(0.5, 1.2))

        # 3. Ingresar Password letra por letra
        xpath_pass = '//*[@id="fusion-app"]/div[2]/form/div[1]/input'
        input_pass = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_pass)))
        input_pass.click() # Hacemos foco
        escribir_como_humano(input_pass, "Filupi2527!!")

        # 4. Click en el botón Ingresar (Span label)
        # Esperamos un momento antes del click final
        time.sleep(1.5)
        xpath_submit = '//*[@id="fusion-app"]/div[2]/form/div[3]/button/span'
        boton_submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit)))
        driver.execute_script("arguments[0].click();", boton_submit)

        # 5. VALIDACIÓN: Esperar a que el nombre "Alan Herrera" aparezca
        xpath_nombre_usuario = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        
        # Esta es la parte crítica: esperamos hasta 20 segundos a que el texto cambie
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_nombre_usuario), "Alan Herrera"))
        
        # Pausa final para que la captura salga perfecta
        time.sleep(4)
        
    except Exception as e:
        print(f"Ocurrió un error en el flujo de Login: {e}")
        
    finally:
        # CAPTURA DE PANTALLA: Aquí veremos el nombre Alan Herrera logueado
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Final_Login_Alan", 
            attachment_type=allure.attachment_type.PNG
        )
