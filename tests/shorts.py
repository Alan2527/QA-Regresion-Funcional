import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_shorts_player_full_validation(driver):
    url_home = "https://tn.com.ar/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_home)
        print(f"INFO: Navegando a la Home: {url_home}")

        # 1. Scrollear hasta el componente Shorts
        xpath_container = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div'
        container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        print("INFO: Componente Shorts localizado.")
        time.sleep(1)

        # 2. Click en PlayIcon
        xpath_play = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/a/div[1]/svg/use'
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn)
        print("INFO: Click en Play realizado.")

        # 3. Validar reproductor visible
        xpath_player = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[1]/div[2]'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_player)))
        print("ÉXITO: Reproductor de Shorts visible.")

        # 4.a y b - El Ojo (Show/Hide Controls)
        xpath_ojo = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[1]/button'
        xpath_h2_desc = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[1]/div[10]/div[1]/h2'
        
        btn_ojo = driver.find_element(By.XPATH, xpath_ojo)
        driver.execute_script("arguments[0].click();", btn_ojo)
        print("INFO: Click en el 'ojo' para ocultar controles.")
        
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_h2_desc)))
        print("   - Contenido ocultado correctamente.")
        
        driver.execute_script("arguments[0].click();", btn_ojo)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_h2_desc)))
        print("   - Contenido restaurado correctamente.")

        # 4.c - Next Button
        xpath_next = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[2]/button[2]'
        desc_inicial = driver.find_element(By.XPATH, xpath_h2_desc).text
        
        driver.find_element(By.XPATH, xpath_next).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_inicial)
        print(f"INFO: Next funciona. Nuevo video: {driver.find_element(By.XPATH, xpath_h2_desc).text[:30]}...")

        # 4.d - Previous Button
        desc_antes_prev = driver.find_element(By.XPATH, xpath_h2_desc).text
        xpath_prev = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[2]/button[1]'
        
        driver.find_element(By.XPATH, xpath_prev).click()
        wait.until(lambda d: d.find_element(By.XPATH, xpath_h2_desc).text != desc_antes_prev)
        print("INFO: Previous funciona. Se cambió de video satisfactoriamente.")

        # 4.e - Share Button dentro del reproductor
        xpath_share = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div/div/button'
        xpath_share_panel = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/div[3]/div[2]'
        
        driver.find_element(By.XPATH, xpath_share).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_share_panel)))
        print("INFO: Panel de compartir visible.")
        driver.find_element(By.XPATH, xpath_share).click() # Cerrar

        # 4.f - Mute (SVG swap)
        xpath_mute = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[2]/button[1]'
        driver.find_element(By.XPATH, xpath_mute).click()
        print("INFO: Botón de Mute clickeado.")

        # 4.h - Click en el link de la nota y volver
        xpath_link_nota = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/div[1]/div[10]/div[1]/h2/a'
        link_elem = driver.find_element(By.XPATH, xpath_link_nota)
        url_nota_href = link_elem.get_attribute('href')
        
        driver.execute_script("arguments[0].click();", link_elem)
        wait.until(EC.url_to_be(url_nota_href))
        print(f"INFO: Navegación exitosa a la nota del Short: {driver.current_url}")
        
        # VOLVER Y TOMAR CAPTURA
        driver.back()
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        # Reabrir para la captura
        play_btn_re = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play)))
        driver.execute_script("arguments[0].click();", play_btn_re)
        time.sleep(2)
        
        allure.attach(driver.get_screenshot_as_png(), name="Captura_Shorts_Reproductor", attachment_type=allure.attachment_type.PNG)

        # 4.i - Cerrar reproductor
        xpath_close = '//*[@id="fusion-app"]/div[12]/main/div[5]/div[1]/div/div/div/button'
        driver.find_element(By.XPATH, xpath_close).click()
        wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_player)))
        print("ÉXITO: Reproductor cerrado correctamente.")

    except Exception as e:
        print(f"ERROR: Fallo en el test de Shorts: {str(e)}")
        raise e
