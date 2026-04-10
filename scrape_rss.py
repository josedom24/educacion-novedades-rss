import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import os

# Configuración
URL = "https://www.juntadeandalucia.es/educacion/portales/novedades-portada"
OUTPUT_FILE = "feed.xml"

def parse_date(date_str):
    months = {
        'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'may': 'May', 'jun': 'Jun',
        'jul': 'Jul', 'ago': 'Aug', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
    }
    try:
        parts = date_str.split()
        if len(parts) == 3:
            day = parts[0]
            month = months.get(parts[1].lower(), 'Jan')
            year = parts[2]
            date_str_en = f"{day} {month} {year}"
            return datetime.strptime(date_str_en, "%d %b %Y").replace(tzinfo=timezone.utc)
    except:
        pass
    return datetime.now(timezone.utc)

def scrape_novedades():

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
        fe.guid(item['link'], permalink=True)

        # Usamos la misma lógica de parseo para la publicación
        dt = parse_date(item['date'])
        fe.published(dt)

    fg.rss_file(OUTPUT_FILE)
    print(f"RSS feed generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    items = scrape_novedades()
    if items:
        print(f"Found {len(items)} news items.")
        generate_rss(items)
    else:
        print("No news items found.")
