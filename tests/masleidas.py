import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ranking_mas_leidas(driver):
    url_nota = "https://tn.com.ar/internacional/2026/01/23/nueva-york-declaro-el-estado-de-emergencia-ante-una-de-las-tormentas-de-nieve-mas-grandes-de-su-historia/"
    wait = WebDriverWait(driver, 20)
    
    driver.get(url_nota)
    
    # XPath original para la segunda noticia del ranking
    xpath_noticia_2 = '//*[@id="fusion-app"]/main/div[1]/div/div[2]/div[1]/section/article[2]/div/a/h2'
    
    noticia = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_noticia_2)))
    noticia.click()
    
    # Captura de evidencia
    allure.attach(driver.get_screenshot_as_png(), name="MasLeidas_OK", attachment_type=allure.attachment_type.PNG)
