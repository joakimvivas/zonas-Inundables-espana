import geopandas as gpd
import os

# Definir el directorio de salida
output_dir = "static"
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

# Cargar el archivo ShapeFile
shapefile_path = "zona_inundable.shp"
gdf = gpd.read_file(shapefile_path)

# Convertir a GeoJSON y guardar en el directorio static
geojson_path = os.path.join(output_dir, "zona_inundable.geojson")
gdf.to_file(geojson_path, driver="GeoJSON")
print(f"GeoJSON file saved at {geojson_path}")