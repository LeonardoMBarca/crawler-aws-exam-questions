from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from scrapper import connext_button
import time

def setup_browser(profile_path, tor_browser_path, geckodriver_path):
    """Configura e retorna o navegador Firefox para ser usado com o Selenium."""
    profile = webdriver.FirefoxProfile(profile_path)
    options = Options()
    options.profile = profile
    options.binary_location = tor_browser_path
    options.add_argument("window-size:800,1000")
    # options.add_argument("--headless")
    
    service = Service(executable_path=geckodriver_path)
    return webdriver.Firefox(service=service, options=options)

def restart_browser_if_needed(browser, search_count, max_searches_per_session, profile_path, tor_browser_path, geckodriver_path):
    # Reinicia o navegador se o limite de pesquisas for atingido
    if search_count >= max_searches_per_session:
        try:
            # Tenta encerrar o navegador atual
            print("Encerrando o navegador Tor.")
            browser.quit()
            time.sleep(2)  # Aguarda o encerramento completo
        except Exception as e:
            print(f"Erro ao fechar o navegador: {e}")
        
        print("Reiniciando o navegador Tor.")
        # Inicializa um novo navegador
        browser = setup_browser(profile_path, tor_browser_path, geckodriver_path)
        connext_button(browser)
    return browser
