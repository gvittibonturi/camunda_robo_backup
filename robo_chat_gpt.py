from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

# Configure o caminho do ChromeDriver
driver_path = '/path/to/chromedriver'  # Altere para o caminho do seu ChromeDriver
download_directory = '/path/to/download'  # Altere para o diretório onde deseja salvar os arquivos

# Crie um navegador
options = webdriver.ChromeOptions()
preferences = {"download.default_directory": download_directory}
options.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(executable_path=driver_path, options=options)

def download_file(file_url):
    response = requests.get(file_url)
    file_name = os.path.join(download_directory, file_url.split("/")[-1])
    with open(file_name, 'wb') as file:
        file.write(response.content)

def visit_folder(url):
    driver.get(url)
    time.sleep(2)  # Pause para garantir que a página carregou

    # Encontrar links de arquivos e baixar
    files = driver.find_elements(By.TAG_NAME, 'a')  # Obtendo todos os links na página
    for file_link in files:
        href = file_link.get_attribute('href')
        
        # Verificar se é um link de arquivo (ou pasta)
        if href and 'file' in href:  # Insira suas condições para identificar arquivos
            print(f'Downloading file: {href}')
            download_file(href)

    # Encontrar links de pastas e navegar
    for folder_link in files:
        href = folder_link.get_attribute('href')
        
        # Verificar se é um link de pasta
        if href and 'folder' in href:  # Insira suas condições para identificar pastas
            print(f'Visiting folder: {href}')
            visit_folder(href)  # Recursão para visitar a nova pasta

try:
    start_url = 'https://exemplo.camunda.com/repository'  # URL de exemplo
    visit_folder(start_url)
finally:
    driver.quit()  # Fecha o navegador
