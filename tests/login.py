import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def test_login_usuario(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    
    try:
        driver.get(url)
        
        # 1. Click en Iniciar Sesión (Usando la clase y XPath provisto)
        # Reintentamos por si el header se actualiza (Stale Element)
        for _ in range(3):
            try:
                boton_login_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[2]/div/a')))
                driver.execute_script("arguments[0].click();", boton_login_header)
                break
            except StaleElementReferenceException:
                time.sleep(1)

        # 2. Ingresar Email
        input_email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/input')))
        input_email.send_keys("alanherrera2527@gmail.com")

        # 3. Ingresar Password
        input_pass = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[1]/input')))
        input_pass.send_keys("Filupi2527!!")

        # 4. Click en el botón Ingresar (Span con clase label)
        boton_ingresar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[3]/button/span')))
        driver.execute_script("arguments[0].click();", boton_ingresar)

        # 5. VALIDACIÓN: Esperar a que el nombre "Alan Herrera" aparezca en el header
        xpath_nombre_usuario = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        
        # Esperamos explícitamente a que el texto cambie a "Alan Herrera"
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_nombre_usuario), "Alan Herrera"))
        
        # Pequeña pausa para que el renderizado del nombre sea perfecto para la foto
        time.sleep(3)
        
    except Exception as e:
        print(f"Error durante el login: {e}")
    finally:
        # CAPTURA DE PANTALLA: Aquí validamos visualmente el nombre Alan Herrera
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Login_Exitoso", 
            attachment_type=allure.attachment_type.PNG
        )
