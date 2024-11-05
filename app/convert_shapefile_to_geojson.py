import geopandas as gpd
import os

# Obtener el directorio base de la aplicación (/app)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Definir el directorio de salida en /app/static
output_dir = os.path.join(base_dir, "static")
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

# Ruta del archivo ShapeFile en /app
shapefile_path = os.path.join(base_dir, "zona_inundable.shp")
gdf = gpd.read_file(shapefile_path)

# Aplicar simplificación para reducir la precisión de las coordenadas
print("Simplifying geometries to reduce file size...")
tolerance = 0.0001  # Ajusta el nivel de tolerancia según tus necesidades
gdf['geometry'] = gdf['geometry'].simplify(tolerance, preserve_topology=True)
print("Geometries simplified.")

# Convertir a GeoJSON y guardar en /app/static
geojson_path = os.path.join(output_dir, "zona_inundable.geojson")
gdf.to_file(geojson_path, driver="GeoJSON")
print(f"GeoJSON file saved at {geojson_path} with simplified geometries.")