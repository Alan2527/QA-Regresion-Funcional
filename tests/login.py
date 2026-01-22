import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_usuario(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.delete_all_cookies() # Empezamos sesión limpia
        driver.get(url)
        
        # 1. Click en Iniciar Sesión
        # Usamos wait.until directamente sobre el elemento
        boton_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[2]/div/a')))
        driver.execute_script("arguments[0].click();", boton_login)

        # 2. Ingresar Email - Usamos send_keys directo sin clics previos
        email = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/input')))
        email.send_keys("alanherrera2527@gmail.com")

        # 3. Ingresar Password
        password = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[1]/input')))
        password.send_keys("Filupi2527!!")
        
        # 4. Click en Ingresar (Span label)
        # Esperamos un segundo para no parecer un bot ultra rápido
        time.sleep(1)
        boton_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[3]/button/span')))
        driver.execute_script("arguments[0].click();", boton_submit)

        # 5. VALIDACIÓN DEL NOMBRE
        # Esperamos a que el texto cambie en el header
        target_nombre = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, target_nombre), "Alan Herrera"))
        
        time.sleep(3) # Tiempo para la captura final
        
    except Exception as e:
        print(f"Fallo en login: {e}")
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Login", 
            attachment_type=allure.attachment_type.PNG
        )
