import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Footer")
@allure.story("Validación de Redes Sociales")
def test_social_links_footer(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    # 1. NAVEGACIÓN Y SCROLL
    with allure.step("1. Navegar a la Home y scrollear al Footer"):
        driver.get(url_home)
        
        # Cierre de popup si existe
        try:
            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        xpath_footer_social = '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]'
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_footer_social)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        time.sleep(3) # Pausa para renderizado

        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Seccion_Footer", 
            attachment_type=allure.attachment_type.PNG
        )

    # 2. CONFIGURACIÓN DE REDES
    ventana_principal = driver.current_window_handle
    redes_footer = {
        "Facebook": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[1]',
        "Twitter": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[2]',
        "Instagram": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[3]',
        "YouTube": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[4]',
        "RSS": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[5]'
    }

    # 3. CICLO DE VALIDACIÓN CON CAPTURAS
    for nombre, xpath in redes_footer.items():
        with allure.step(f"Validar red social: {nombre}"):
            link_elemento = driver.find_element(By.XPATH, xpath)
            
            # Click con JS
            driver.execute_script("arguments[0].click();", link_elemento)
            
            # Esperar y cambiar a nueva pestaña
            wait.until(lambda d: len(d.window_handles) > 1)
            nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
            driver.switch_to.window(nueva_ventana)
            
            # Esperar a que la URL cambie de 'about:blank' a la red social
            time.sleep(4) 
            
            # CAPTURA DE LA RED SOCIAL ABIERTA
            allure.attach(
                driver.get_screenshot_as_png(), 
                name=f"Captura_Pestaña_{nombre}", 
                attachment_type=allure.attachment_type.PNG
            )
            
            # Cerrar y volver
            driver.close()
            driver.switch_to.window(ventana_principal)
            time.sleep(1)
