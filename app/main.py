import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import folium

app = FastAPI()

# Obtener el directorio actual de la aplicación (carpeta /app)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Verificar y crear el directorio 'static' dentro de /app
static_dir = os.path.join(base_dir, "static")
os.makedirs(static_dir, exist_ok=True)

# Montar la carpeta de archivos estáticos en FastAPI
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Función para verificar la existencia de zona_inundable.geojson
def check_and_generate_geojson():
    geojson_path = os.path.join(static_dir, "zona_inundable.geojson")
    if not os.path.exists(geojson_path):
        print("GeoJSON file not found. Generating zona_inundable.geojson...")
        # Ruta al script convert_shapefile_to_geojson.py
        script_path = os.path.join(base_dir, "convert_shapefile_to_geojson.py")
        # Ejecutar el script para generar el archivo GeoJSON
        subprocess.run(["python3", script_path], check=True)
        print("GeoJSON file generated successfully.")
    else:
        print("GeoJSON file already exists.")

# Llamar a la función al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    check_and_generate_geojson()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(base_dir, "templates", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/generate_map", response_class=HTMLResponse)
async def generate_map():
    # Crear el mapa base de España
    m = folium.Map(location=[40.0, -3.7], zoom_start=6)

    # Cargar y añadir la capa GeoJSON de zonas inundables
    geojson_path = os.path.join(static_dir, "zona_inundable.geojson")
    folium.GeoJson(
        geojson_path,
        name="Zonas Inundables",
        style_function=lambda x: {
            "color": "blue",
            "weight": 2,
            "fillOpacity": 0.5
        }
    ).add_to(m)

    # Guardar el mapa en un archivo HTML en la carpeta static dentro de /app
    map_html = os.path.join(static_dir, "mapa_inundaciones.html")
    m.save(map_html)

    return HTMLResponse(content="<p>Mapa generado correctamente. Accede a la página principal para visualizarlo.</p>")
