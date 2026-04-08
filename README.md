# Educación Novedades RSS

Este repositorio genera automáticamente un feed RSS/Atom a partir de la página de novedades del portal de educación de la Junta de Andalucía.

## 🚀 Cómo funciona

Dado que la página de novedades ya no ofrece un feed nativo, este proyecto utiliza un script de Python para realizar web scraping y convertir el contenido HTML en un formato XML estándar.

### Componentes:
- **`scrape_rss.py`**: Script en Python que extrae los títulos, enlaces y fechas de las novedades y genera el archivo `feed.xml`.
- **GitHub Actions**: Un flujo de trabajo automatizado que ejecuta el script cada 6 horas y actualiza el feed automáticamente.

## 🛠️ Instalación y Uso Local

Si quieres ejecutarlo en tu propia máquina:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/josedom24/educacion-novedades-rss.git
   cd educacion-novedades-rss
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Ejecuta el generador:
   ```bash
   python3 scrape_rss.py
   ```

El resultado será un archivo `feed.xml` en el directorio raíz.

## 🌐 Acceso al Feed

Si tienes activado GitHub Pages en este repositorio, puedes acceder al feed en:
`https://josedom24.github.io/educacion-novedades-rss/feed.xml`

Sigue esa URL en tu lector de RSS favorito (Feedly, Inoreader, etc.) para mantenerte al día con las novedades educativas.
