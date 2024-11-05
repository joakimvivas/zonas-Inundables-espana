# Contenido del script main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import folium

app = FastAPI()

@app.get("/map", response_class=HTMLResponse)
async def generate_map():
    # Crear el mapa base de España
    m = folium.Map(location=[40.0, -3.7], zoom_start=6)

    # Cargar y añadir la capa GeoJSON de zonas inundables
    geojson_path = "zona_inundable.geojson"
    folium.GeoJson(
        geojson_path,
        name="Zonas Inundables",
        style_function=lambda x: {
            "color": "blue",
            "weight": 2,
            "fillOpacity": 0.5
        }
    ).add_to(m)

    # Guardar el mapa en un archivo HTML temporal
    map_html = "mapa_inundaciones.html"
    m.save(map_html)

    # Leer el archivo HTML para enviarlo como respuesta
    with open(map_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)
