import requests
from bs4 import BeautifulSoup

URL = "https://fctv33.monster"
OUTPUT_TXT = "partidos_explicativo.txt"

# Hacer request a la web
resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

# Buscar todos los enlaces
enlaces = soup.find_all("a")
raw_links = []

for a in enlaces:
    href = a.get("href")
    text = a.get_text(strip=True)
    if href and "fctv33.monster" in href:
        raw_links.append((text, href))

# Guardar TXT bonito
def limpiar_link(href):
    return href.replace("\n", "").strip()

with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    for texto, href in raw_links:
        href = limpiar_link(href)
        partes = texto.split(" - ")
        if len(partes) == 3:
            categoria, partido, hora = partes
        elif len(partes) == 2:
            categoria, partido = partes
            hora = "Desconocida"
        else:
            categoria = "Desconocida"
            partido = texto
            hora = "Desconocida"

        f.write(f"Categoría: {categoria}\nPartido: {partido}\nHora: {hora}\nLink: {href}\n\n")

print(f"✅ Se han extraído {len(raw_links)} links y guardado en {OUTPUT_TXT}")
