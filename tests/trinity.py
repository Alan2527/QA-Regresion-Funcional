import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_trinity_audio_player(driver):
    url_nota = "https://tn.com.ar/politica/2026/01/26/milei-viaja-a-mar-del-plata-para-reactivar-su-agenda-partidaria-y-busca-retener-el-apoyo-en-distritos-clave/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_nota)
        print(f"INFO: Navegando a la nota para probar Trinity Audio: {url_nota}")

        # 1. Buscar y clickear el botón Play
        xpath_play_btn = '//*[@id="app"]/div/div/div/div[1]/button'
        # Trinity a veces tarda en cargar, esperamos presencia
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_play_btn)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play_btn)
        time.sleep(1)
        play_btn.click()
        print("INFO: Click en el botón Play de Trinity Audio.")

        # 2. Validar layout-top-wrapper y tomar captura
        xpath_layout = '//*[@id="app"]/div/div/div'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_layout)))
        
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Captura_Trinity_Reproduciendo", 
            attachment_type=allure.attachment_type.PNG
        )
        print("INFO: Captura de Trinity Audio adjuntada.")

        # 3. Validar span "Reproduciendo..."
        xpath_label = '//*[@id="fusion-app"]/div[9]/div[1]/main/div[1]/div/div[3]/div/div[1]/span'
        label_elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath_label)))
        assert "Reproduciendo..." in label_elem.text
        print(f"INFO: Label validado: {label_elem.text}")

        # 4. Validar "Escuchando artículo"
        xpath_title_span = '//*[@id="app"]/div/div/div/div[2]/div[1]/div/span'
        title_elem = driver.find_element(By.XPATH, xpath_title_span)
        assert "Escuchando artículo" in title_elem.text
        print("INFO: Título 'Escuchando artículo' validado.")

        # 5. Validar Powered by y enlace
        xpath_powered = '//*[@id="app"]/div/div/div/div[2]/div[3]/div[1]/div'
        powered_div = driver.find_element(By.XPATH, xpath_powered)
        assert "Powered by" in powered_div.text
        link_trinity = powered_div.find_element(By.TAG_NAME, "a").get_attribute("href")
        assert "trinityaudio.ai" in link_trinity
        print("INFO: Créditos de Trinity Audio validados.")

        # 6 y 7. Validar timers y track
        timer_current = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[1]/div')
        timer_total = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[3]/div')
        track_bar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/div[2]/div/div')
        assert timer_current.is_displayed() and timer_total.is_displayed() and track_bar.is_displayed()
        print("INFO: Elementos de tiempo y barra de progreso visibles.")

        # 8. Validar Forward (+10 seg)
        tiempo_antes = timer_current.text
        btn_forward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[2]/button')
        btn_forward.click()
        time.sleep(1)
        assert timer_current.text != tiempo_antes
        print(f"INFO: Forward funciona. Tiempo cambió de {tiempo_antes} a {timer_current.text}")

        # 9. Validar Backward (-10 seg)
        tiempo_antes_back = timer_current.text
        btn_backward = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[1]/button')
        btn_backward.click()
        time.sleep(1)
        assert timer_current.text != tiempo_antes_back
        print(f"INFO: Backward funciona. Tiempo cambió de {tiempo_antes_back} a {timer_current.text}")

        # 10. Validar Speed Control
        btn_speed = driver.find_element(By.XPATH, '//button[@aria-label="Current speed: 1.0x"]')
        btn_speed.click()
        container_speed = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div')))
        btn_cancel = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/button')
        print("INFO: Selector de velocidad abierto.")
        btn_cancel.click()
        print("INFO: Selector de velocidad cerrado.")

        # 11. Validar Pause y Play final
        btn_toggle = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/button')
        # Pausar
        btn_toggle.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-play")))
        print("INFO: El reproductor se pausó correctamente.")
        
        # Volver a Play
        btn_toggle.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-pause")))
        print("ÉXITO: Ciclo de Pause/Play completado.")

    except Exception as e:
        print(f"ERROR en Trinity Audio: {str(e)}")
        allure.attach(driver.get_screenshot_as_png(), name="Error_Trinity", attachment_type=allure.attachment_type.PNG)
        raise e
