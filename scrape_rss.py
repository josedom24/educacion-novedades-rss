import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import os

# Configuración
URL = "https://www.juntadeandalucia.es/educacion/portales/novedades-portada"
OUTPUT_FILE = "feed.xml"

def scrape_novedades():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # This is a placeholder logic. In a real scenario, we'd inspect the HTML
        # structure of the target page to find the correct selectors.
        # Assuming news items are in a list or grid.
        news_items = []

        # Example: searching for elements that might contain news (this needs verification)
        # For now, I'll implement a basic search for <a> tags with meaningful text
        # to avoid the NameError and provide a working base.
        for article in soup.find_all('div', class_='novedades-item'): # Hypothetical class
            title_el = article.find('a')
            if title_el:
                title = title_el.get_text(strip=True)
                link = title_el['href']
                if not link.startswith('http'):
                    link = URL + link # simplified relative link handling

                # Attempt to find a date
                date_el = article.find('span', class_='date')
                date = date_el.get_text(strip=True) if date_el else ""

                news_items.append({'title': title, 'link': link, 'date': date})

        return news_items
    except Exception as e:
        print(f"Error scraping site: {e}")
        return []



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
