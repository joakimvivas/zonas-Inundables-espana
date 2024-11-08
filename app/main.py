import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import folium
import geopandas as gpd

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

# Función para validar que el archivo GeoJSON contiene datos
def validate_geojson_data(geojson_path):
    print("Validating GeoJSON data...")
    try:
        gdf = gpd.read_file(geojson_path)
        if gdf.empty:
            print("Error: GeoJSON file is empty.")
            return False
        else:
            print(f"GeoJSON data loaded successfully with {len(gdf)} entries.")
            return True
    except Exception as e:
        print(f"Error validating GeoJSON data: {e}")
        return False

# Función para generar el archivo del mapa completo si no existe
def generate_map_file():
    map_html_path = os.path.join(static_dir, "mapa_inundaciones.html")
    geojson_path = os.path.join(static_dir, "zona_inundable.geojson")

    if not os.path.exists(map_html_path):
        print("Map HTML file not found. Attempting to generate mapa_inundaciones.html...")

        # Crear el mapa base
        print("Creating base map...")
        m = folium.Map(location=[40.0, -3.7], zoom_start=6)
        print("Base map created.")

        # Intentar agregar la capa GeoJSON si el archivo es válido y no está vacío
        if os.path.exists(geojson_path) and validate_geojson_data(geojson_path):
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
                print("Generating simple map without GeoJSON layer.")
                generate_map_file_simple()
                return
        else:
            print("GeoJSON file is either missing or invalid. Generating simple map without GeoJSON.")
            generate_map_file_simple()
            return

        # Guardar el mapa completo en HTML
        try:
            print("Saving the complete map to HTML...")
            m.save(map_html_path)
            print(f"Map HTML file saved at {map_html_path}")
            
            # Verificar si el archivo HTML no está vacío
            if os.path.getsize(map_html_path) > 0:
                print("Map HTML file generated successfully and is not empty.")
            else:
                print("Warning: Map HTML file is empty after saving. Generating simple map as fallback.")
                generate_map_file_simple()
        except Exception as e:
            print(f"Error saving the complete map to HTML: {e}")
            print("Generating simple map without GeoJSON layer as fallback.")
            generate_map_file_simple()
    else:
        print("Map HTML file already exists.")

# Función para generar un mapa simple sin la capa GeoJSON
def generate_map_file_simple():
    print("Creating and saving a simple map without GeoJSON...")
    map_html_path = os.path.join(static_dir, "mapa_inundaciones.html")
    m = folium.Map(location=[40.0, -3.7], zoom_start=6)
    try:
        m.save(map_html_path)
        print("Simple map HTML file saved successfully as mapa_inundaciones.html.")
    except Exception as e:
        print(f"Error saving simple map: {e}")

# Llamar a la función al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    check_and_generate_geojson()  # Verificar y generar GeoJSON si es necesario
    generate_map_file()  # Generar el archivo HTML del mapa si no existe

# Cargar index.html desde templates
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
