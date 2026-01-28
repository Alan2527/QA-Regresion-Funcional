import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Footer")
@allure.story("Validación de Redes Sociales")
def test_social_links_footer(driver):
    # TIP: Para Instagram, a veces ayuda cambiar el User-Agent en la configuración del driver
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 30)
    ventana_principal = driver.current_window_handle
    
    with allure.step("1. Navegar a la Home y scrollear al Footer"):
        driver.get(url_home)
        # Cierre de popup (basado en tu imagen_22d02d.png)
        try:
            btn_aceptar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ACEPTAR')]")))
            driver.execute_script("arguments[0].click();", btn_aceptar)
        except:
            pass

        xpath_footer_social = '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]'
        contenedor = wait.until(EC.presence_of_element_located((By.XPATH, xpath_footer_social)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Seccion_Footer", attachment_type=allure.attachment_type.PNG)

    redes_footer = {
        "Instagram": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[1]',
        "Facebook": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[2]',
        "X": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[3]',
        "YouTube": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[4]',
        "TikTok": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[5]',
        "Telegram": '//*[@id="fusion-app"]/footer/div[2]/div[1]/div[1]/div[1]/a[6]'
    }

    for nombre, xpath in redes_footer.items():
        with allure.step(f"Validar red social: {nombre}"):
            link_elemento = driver.find_element(By.XPATH, xpath)
            href_destino = link_elemento.get_attribute('href')
            
            # Click y cambio de ventana
            driver.execute_script("arguments[0].click();", link_elemento)
            
            try:
                wait.until(lambda d: len(d.window_handles) > 1)
                nueva_ventana = [w for w in driver.window_handles if w != ventana_principal][0]
                driver.switch_to.window(nueva_ventana)
                
                # Para Instagram/TikTok damos tiempo extra pero no fallamos si sale el login
                time.sleep(6) 
                
                allure.attach(
                    driver.get_screenshot_as_png(), 
                    name=f"Captura_Pestaña_{nombre}", 
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Validación lógica: ¿Estamos en el dominio correcto?
                assert nombre.lower() in driver.current_url.lower() or "login" in driver.current_url, \
                    f"La URL final {driver.current_url} no parece ser de {nombre}"
                
            finally:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(ventana_principal)
                time.sleep(1)
