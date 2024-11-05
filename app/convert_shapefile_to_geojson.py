# Contenido del script convert_shapefile_to_geojson.py
import geopandas as gpd

# Cargar el archivo ShapeFile
shapefile_path = "zona_inundable.shp"
gdf = gpd.read_file(shapefile_path)

# Convertir a GeoJSON
geojson_path = "zona_inundable.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")
