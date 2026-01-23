import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ranking_mas_leidas(driver):
    # URL específica de la nota de Colapinto
    url_colapinto = "https://tn.com.ar/deportes/automovilismo/2026/01/23/colapinto-expreso-su-entusiasmo-con-el-nuevo-modelo-de-alpine-los-autos-lindos-siempre-van-rapido/"
    wait = WebDriverWait(driver, 25)
    
    try:
        driver.get(url_colapinto)
        print(f"INFO: Iniciando test de busqueda y funcionamiento de Más Leídas")

        # 1. LIMPIEZA DE MODALES
        # Borramos cualquier pop-up que pueda tapar el ranking
        driver.execute_script("""
            document.querySelectorAll('.tp-modal, .tp-backdrop, #didomi-host').forEach(el => el.remove());
            document.body.classList.remove('tp-modal-open');
        """)

        # 2. LOCALIZAR LA SECCIÓN "LO MÁS LEÍDO"
        # Usamos un selector que busca el contenedor por su clase característica
        xpath_seccion = "//section[contains(@class, 'most-read')]"
        seccion = wait.until(EC.presence_of_element_located((By.XPATH, xpath_seccion)))
        
        # Hacemos scroll hasta la sección
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seccion)
        print("INFO: Sección 'Lo más leído' localizada y centrada en pantalla.")
        time.sleep(1) # Breve pausa para estabilidad

        # 3. CLICK EN LA SEGUNDA NOTICIA DEL RANKING
        # Seleccionamos el segundo encabezado (h2) dentro del widget de más leídas
        xpath_nota_2 = "(//section[contains(@class, 'most-read')]//h2)[2]"
        noticia_click = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_nota_2)))
        
        titulo_nota = noticia_click.text
        print(f"INFO: Nota detectada en ranking #2: '{titulo_nota}'")
        
        # Ejecutamos el click
        driver.execute_script("arguments[0].click();", noticia_click)
        print("ÉXITO: Se realizó el clic correctamente.")

        # 4. VALIDACIÓN DE NAVEGACIÓN
        # Esperamos a que la URL cambie (ya no debe ser la de Colapinto)
        wait.until(lambda d: d.current_url != url_colapinto)
        print(f"INFO: Redirección completada a: {driver.current_url}")

    except Exception as e:
        print(f"ERROR: Falló la interacción con el ranking: {e}")
        pytest.fail(f"Fallo en Mas Leidas: {e}")
        
    finally:
        # Captura de pantalla para Allure
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Evidencia_Mas_Leidas_Colapinto", 
            attachment_type=allure.attachment_type.PNG
        )
