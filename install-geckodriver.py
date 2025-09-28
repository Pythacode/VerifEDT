from selenium import webdriver
try :
  from webdriver_manager.firefox import GeckoDriverManager
except :
  import os
  os.systeme('pip install webdriver_manager')
  from webdriver_manager.firefox import GeckoDriverManager
  
from selenium.webdriver.firefox.service import Service as FirefoxService

# Configuration du service Firefox avec GeckoDriverManager
service = FirefoxService(GeckoDriverManager().install())

# Initialisation du navigateur Firefox
driver = webdriver.Firefox(service=service)

# Exemple : ouverture d'une page web
driver.get("https://github.com/Pythacode/VerfifEDT")

# N'oubliez pas de fermer le navigateur après utilisation
driver.quit()
