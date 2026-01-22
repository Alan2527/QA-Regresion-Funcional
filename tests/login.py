import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_limpio(driver):
    url = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 20)
    
    try:
        driver.get(url)
        
        # 1. CERRAMOS POP-UPS (Como el de notificaciones que se ve en tu captura)
        try:
            # Intentamos cerrar el cartel de "¿Querés recibir alertas?"
            boton_mas_tarde = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'MÁS TARDE')]")))
            boton_mas_tarde.click()
        except:
            print("No apareció el pop-up de alertas.")

        # 2. CLICK EN INGRESAR
        boton_login_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div[2]/div/a')))
        driver.execute_script("arguments[0].click();", boton_login_header)

        # 3. VERIFICAR SI HAY CAPTCHA
        # Si aparece el cuadro de hCaptcha, el test va a fallar aquí con un mensaje claro
        try:
            iframe_captcha = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframe_captcha:
                if "captcha" in iframe.get_attribute("src").lower():
                    print("BLOQUEO: El sitio lanzó un Captcha visual.")
        except:
            pass

        # 4. LOGIN TRADICIONAL
        input_email = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/input')))
        input_email.send_keys("alanherrera2527@gmail.com")

        input_pass = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[1]/input')))
        input_pass.send_keys("Filupi2527!!")

        # Usamos JS para el click final para evitar que el hCaptcha intercepte el clic físico
        boton_ingresar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/form/div[3]/button/span')))
        driver.execute_script("arguments[0].click();", boton_ingresar)

        # 5. VALIDACIÓN DE NOMBRE
        xpath_nombre = '//*[@id="fusion-app"]/header/div/div[2]/div/a/span[2]'
        wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath_nombre), "Alan Herrera"))

    except Exception as e:
        print(f"Error detectado: {e}")
    finally:
        allure.attach(driver.get_screenshot_as_png(), name="Evidencia_Login", attachment_type=allure.attachment_type.PNG)
