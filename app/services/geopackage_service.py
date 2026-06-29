import geopandas as gpd
import json
from pathlib import Path
from shapely.geometry import mapping
from app.utils.exceptions import ValidationException
from app.utils.logger import logger

class GeopackageService:
    """Servicio para cargar y procesar geopackage"""
    
    # Path al geopackage
    GEOPACKAGE_PATH = Path("data/poligonos.gpkg")
    
    @staticmethod
    def load_geopackage(layer: str = None) -> gpd.GeoDataFrame:
        """
        Carga un geopackage
        
        Args:
            layer: Nombre de la capa (si None, carga la primera)
            
        Returns:
            GeoDataFrame con los polígonos
            
        Raises:
            ValidationException si no existe el archivo
        """
        if not GeopackageService.GEOPACKAGE_PATH.exists():
            raise ValidationException(f"Geopackage no encontrado en {GeopackageService.GEOPACKAGE_PATH}")
        
        try:
            gdf = gpd.read_file(GeopackageService.GEOPACKAGE_PATH, layer=layer)
            logger.info(f"Geopackage cargado: {len(gdf)} polígonos")
            return gdf
        except Exception as e:
            raise ValidationException(f"Error cargando geopackage: {str(e)}")
    
    @staticmethod
    def get_layers() -> list:
        """Obtiene lista de capas disponibles"""
        try:
            import fiona
            return fiona.listlayers(str(GeopackageService.GEOPACKAGE_PATH))
        except Exception as e:
            logger.error(f"Error listando capas: {e}")
            return []
    
    @staticmethod
    def to_geojson(gdf: gpd.GeoDataFrame) -> dict:
        """
        Convierte GeoDataFrame a GeoJSON
        
        Args:
            gdf: GeoDataFrame
            
        Returns:
            dict con formato GeoJSON
        """
        try:
            features = []
            for idx, row in gdf.iterrows():
                feature = {
                    "type": "Feature",
                    "id": idx,
                    "geometry": mapping(row.geometry),
                    "properties": {
                        k: str(v) if v is not None else None 
                        for k, v in row.items() 
                        if k != "geometry"
                    }
                }
                features.append(feature)
            
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }
            
            return geojson
        except Exception as e:
            logger.error(f"Error convirtiendo a GeoJSON: {e}")
            raise ValidationException(f"Error en conversión GeoJSON: {str(e)}")
    
    @staticmethod
    def get_bounds(gdf: gpd.GeoDataFrame) -> dict:
        """
        Obtiene bounds del GeoDataFrame
        
        Args:
            gdf: GeoDataFrame
            
        Returns:
            dict con minx, miny, maxx, maxy
        """
        total_bounds = gdf.total_bounds
        return {
            "minx": float(total_bounds[0]),
            "miny": float(total_bounds[1]),
            "maxx": float(total_bounds[2]),
            "maxy": float(total_bounds[3]),
        }
    
    @staticmethod
    def get_center(bounds: dict) -> tuple:
        """
        Calcula center desde bounds
        
        Args:
            bounds: dict con minx, miny, maxx, maxy
            
        Returns:
            tuple (lat, lng)
        """
        lat = (bounds["miny"] + bounds["maxy"]) / 2
        lng = (bounds["minx"] + bounds["maxx"]) / 2
        return (lat, lng)
    
    @staticmethod
    def get_polygon_by_id(gdf: gpd.GeoDataFrame, polygon_id: int) -> dict | None:
        """
        Obtiene un polígono específico
        
        Args:
            gdf: GeoDataFrame
            polygon_id: ID del polígono
            
        Returns:
            dict con datos del polígono o None
        """
        try:
            row = gdf.iloc[polygon_id]
            return {
                "id": polygon_id,
                "geometry": mapping(row.geometry),
                "properties": {
                    k: str(v) if v is not None else None 
                    for k, v in row.items() 
                    if k != "geometry"
                }
            }
        except IndexError:
            return None
    
    @staticmethod
    def calculate_area(geometry) -> float:
        """
        Calcula área de geometría en metros cuadrados
        
        Args:
            geometry: Geometría Shapely
            
        Returns:
            float con área en m²
        """
        try:
            # Reproyectar a metros si es necesario
            from shapely.ops import transform
            import pyproj
            
            # Usar Web Mercator para cálculo aproximado
            proj = pyproj.Proj(proj='merc')
            
            def project(x, y, z=None):
                return pyproj.transform(
                    pyproj.Proj(proj='latlong'),
                    proj,
                    x,
                    y
                )
            
            projected = transform(project, geometry)
            return projected.area
        except Exception as e:
            logger.warning(f"Error calculando área: {e}")
            return 0.0
    
    @staticmethod
    def validate_geometries(gdf: gpd.GeoDataFrame) -> dict:
        """
        Valida geometrías en el GeoDataFrame
        
        Args:
            gdf: GeoDataFrame
            
        Returns:
            dict con resultado de validación
        """
        invalid = gdf[~gdf.geometry.is_valid]
        
        return {
            "total": len(gdf),
            "valid": len(gdf) - len(invalid),
            "invalid": len(invalid),
            "is_all_valid": len(invalid) == 0
        }
    
    @staticmethod
    def search_polygons(gdf: gpd.GeoDataFrame, search_term: str, search_fields: list = None) -> gpd.GeoDataFrame:
        """
        Busca polígonos por término
        
        Args:
            gdf: GeoDataFrame
            search_term: Término a buscar
            search_fields: Campos donde buscar (si None, busca en todos)
            
        Returns:
            GeoDataFrame filtrado
        """
        if not search_term:
            return gdf
        
        search_term = search_term.lower()
        
        if search_fields is None:
            search_fields = gdf.columns[gdf.columns != 'geometry']
        
        mask = False
        for field in search_fields:
            if field in gdf.columns:
                mask = mask | gdf[field].astype(str).str.lower().str.contains(search_term, na=False)
        
        return gdf[mask]
    
    @staticmethod
    def get_crs(gdf: gpd.GeoDataFrame) -> str:
        """Obtiene CRS del GeoDataFrame"""
        return str(gdf.crs) if gdf.crs else "Unknown"
