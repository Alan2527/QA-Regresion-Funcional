import pytest
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extiende el reporte de Pytest para incluir capturas de pantalla.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # Accedemos al driver desde el test
        driver = item.funcargs.get("driver")
        if driver:
            # Creamos la carpeta de capturas si no existe
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # Nombre del archivo basado en el nombre del test y hora
            file_name = f"screenshots/{item.name}_{datetime.now().strftime('%H%M%S')}.png"
            driver.save_screenshot(file_name)
            
            # Si usas pytest-html, esto embebe la imagen en el reporte
            import pytest_html
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
