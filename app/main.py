import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import folium

app = FastAPI()

# Obtener el directorio actual de la aplicación (carpeta /app)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Verificar y crear el directorio 'static' dentro de /app
static_dir = os.path.join(base_dir, "static")
os.makedirs(static_dir, exist_ok=True)

# Montar la carpeta de archivos estáticos en FastAPI
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configurar Jinja2Templates para usar la carpeta templates
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

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

# Función para generar el archivo del mapa si no existe
def generate_map_file():
    map_html_path = os.path.join(static_dir, "mapa_inundaciones.html")
    if not os.path.exists(map_html_path):
        print("Map HTML file not found. Generating mapa_inundaciones.html...")

        # Crear el mapa base
        print("Creating base map...")
        m = folium.Map(location=[40.0, -3.7], zoom_start=6)
        print("Base map created.")

        # Añadir la capa GeoJSON de zonas inundables
        geojson_path = os.path.join(static_dir, "zona_inundable.geojson")
        if os.path.exists(geojson_path):
            print("Loading GeoJSON layer...")
            try:
                folium.GeoJson(
                    geojson_path,
                    name="Zonas Inundables",
                    style_function=lambda x: {
                        "color": "blue",
                        "weight": 2,
                        "fillOpacity": 0.5
                    }
                ).add_to(m)
                print("GeoJSON layer added to the map.")
            except Exception as e:
                print(f"Error loading GeoJSON layer: {e}")
        else:
            print(f"GeoJSON file not found at {geojson_path}")

        # Guardar el mapa en un archivo HTML
        try:
            print("Saving the map to HTML...")
            m.save(map_html_path)
            print(f"Map HTML file saved at {map_html_path}")
        except Exception as e:
            print(f"Error saving the map to HTML: {e}")
    else:
        print("Map HTML file already exists.")

# Llamar a la función al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    check_and_generate_geojson()  # Verificar y generar GeoJSON si es necesario
    generate_map_file()  # Generar el archivo HTML del mapa si no existe

# Cargar index.html desde templates
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
