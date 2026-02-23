from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# ------------------ Configuración ------------------
# Asegúrate que chromedriver.exe esté aquí
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
URL = "https://fctv33.monster"
OUTPUT_TXT = "partidos_explicativo.txt"

# Opciones de Chrome headless
options = Options()
options.headless = True
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")

# ------------------ Abrir navegador ------------------
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
driver.get(URL)
time.sleep(5)  # Espera que cargue la página

# ------------------ Extraer links ------------------
enlaces = driver.find_elements(By.TAG_NAME, "a")
raw_links = []

for a in enlaces:
    href = a.get_attribute("href")
    text = a.text.strip()
    if href and "fctv33.monster" in href:
        raw_links.append((text, href))

driver.quit()

# ------------------ Generar TXT bonito ------------------


def limpiar_link(href):
    return href.replace("\n", "").strip()  # eliminar saltos de línea


with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    for texto, href in raw_links:
        href = limpiar_link(href)
        # Intentamos separar categoría, partido y hora si el texto lo tiene
        partes = texto.split(" - ")  # si la web usa este separador
        if len(partes) == 3:
            categoria, partido, hora = partes
        elif len(partes) == 2:
            categoria, partido = partes
            hora = "Desconocida"
        else:
            categoria = "Desconocida"
            partido = texto
            hora = "Desconocida"

        f.write(
            f"Categoría: {categoria}\nPartido: {partido}\nHora: {hora}\nLink: {href}\n\n")

print(f"✅ Se han extraído {len(raw_links)} links y guardado en {OUTPUT_TXT}")
