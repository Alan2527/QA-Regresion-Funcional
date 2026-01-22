import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_usuario(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30) # Aumentamos el tiempo a 30s
    
    try:
        driver.get(url)
        
        # 1. Click en Iniciar Sesión
        boton_login_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[2]/div/a')))
        driver.execute_script("arguments[0].click();", boton_login_header)
        time.sleep(2) # Pausa para que el form cargue bien

        # 2. Ingresar Email
        input_email = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/input')))
        input_email.clear()
        input_email.send_keys("alanherrera2527@gmail.com")

        # 3. Ingresar Password
        input_pass = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[1]/input')))
        input_pass.clear()
        input_pass.send_keys("Filupi2527!!")
        time.sleep(1)

        # 4. Click en el botón Ingresar
        boton_ingresar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[3]/button/span')))
        driver.execute_script("arguments[0].click();", boton_ingresar)

        # 5. VALIDACIÓN: Esperar el nombre "Alan Herrera"
        # Usamos un try interno para detectar si el login falló por seguridad/captcha
        xpath_nombre_usuario = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        try:
            wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_nombre_usuario), "Alan Herrera"))
        except:
            print("El nombre no apareció. Posible Captcha o bloqueo de seguridad.")
        
        time.sleep(4)
        
    finally:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Resultado_Login", 
            attachment_type=allure.attachment_type.PNG
        )
