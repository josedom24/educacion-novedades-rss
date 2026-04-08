import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import os

# Configuración
URL = "https://www.juntadeandalucia.es/educacion/portales/novedades-portada"
OUTPUT_FILE = "feed.xml"

def scrape_novedades():
    print(f"Fetching content from {URL}...")
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = []

    # Buscamos todos los elementos que contienen el título de la noticia
    # Basado en el análisis previo: clase .adt-novedades-ceps__item-data__title
    title_elements = soup.find_all(class_="adt-novedades-ceps__item-data__title")

    for element in title_elements:
        link_tag = element.find('a')
        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        link = link_tag.get('href')

        # Asegurar que el enlace sea absoluto
        if link and not link.startswith('http'):
            link = "https://www.juntadeandalucia.es" + link

        # La fecha suele estar en un elemento anterior o cercano
        # Buscamos el texto que parece una fecha justo antes del título
        date_text = "No disponible"
        # Intentamos buscar el elemento padre y luego el hermano anterior que contenga texto de fecha
        parent = element.find_parent()
        if parent:
            # Buscamos cualquier texto que coincida con el patrón de fecha (ej. "30 mar 2026")
            # Como es texto plano, buscamos en el contenido del contenedor
            # El análisis indica que la fecha está justo encima.
            # Buscamos el primer elemento con texto que no sea el título.
            prev_elements = parent.find_all(string=True)
            for text in prev_elements:
                text = text.strip()
                if text and any(month in text.lower() for month in ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']):
                    date_text = text
                    break

        news_items.append({
            'title': title,
            'link': link,
            'date': date_text
        })

    return news_items

def generate_rss(news_items):
    fg = FeedGenerator()
    fg.title('Novedades Educación - Junta de Andalucía')
    fg.description('Feed automático de novedades del portal de educación de la Junta de Andalucía')
    fg.link(href=URL)
    fg.updated(datetime.now(timezone.utc))

    for item in news_items:
        fe = fg.add_entry()
        fe.title(item['title'])
        fe.link(href=item['link'])
        # Intentamos parsear la fecha si es posible, si no, ponemos la actual
        # El formato es "30 mar 2026"
        try:
            # Mapeo simple de meses españoles a inglés para datetime
            months = {
                'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'may': 'May', 'jun': 'Jun',
                'jul': 'Jul', 'ago': 'Aug', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
            }
            parts = item['date'].split()
            if len(parts) == 3:
                day = parts[0]
                month = months.get(parts[1].lower(), 'Jan')
                year = parts[2]
                date_str = f"{day} {month} {year}"
                dt = datetime.strptime(date_str, "%d %b %Y").replace(tzinfo=timezone.utc)
                fe.published(dt)
            else:
                fe.published(datetime.now(timezone.utc))
        except Exception as e:
            print(f"Could not parse date {item['date']}: {e}")
            fe.published(datetime.now(timezone.utc))

    fg.rss_file(OUTPUT_FILE)
    print(f"RSS feed generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    items = scrape_novedades()
    if items:
        print(f"Found {len(items)} news items.")
        generate_rss(items)
    else:
        print("No news items found.")
