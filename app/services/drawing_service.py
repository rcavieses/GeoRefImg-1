import json
from shapely.geometry import shape, Polygon as ShapelyPolygon
from shapely import wkt
from app.utils.logger import logger
from app.utils.exceptions import ValidationException

class DrawingService:
    """Servicio para operaciones de dibujo y edicion de poligonos"""
    
    @staticmethod
    def geojson_to_wkt(geojson_feature: dict) -> str:
        """Convierte GeoJSON a WKT"""
        try:
            geometry = geojson_feature.get('geometry')
            if not geometry:
                raise ValidationException("Feature sin geometria")
            
            geom = shape(geometry)
            return wkt.dumps(geom)
        except Exception as e:
            logger.error(f"Error convirtiendo GeoJSON: {e}")
            raise ValidationException(f"Error: {str(e)}")
    
    @staticmethod
    def wkt_to_geojson(geom_wkt: str) -> dict:
        """Convierte WKT a GeoJSON"""
        try:
            geom = wkt.loads(geom_wkt)
            from shapely.geometry import mapping
            
            return {
                "type": "Feature",
                "geometry": mapping(geom),
                "properties": {}
            }
        except Exception as e:
            logger.error(f"Error convirtiendo WKT: {e}")
            raise ValidationException(f"Error: {str(e)}")
    
    @staticmethod
    def merge_polygons(polygon_wkts: list) -> str:
        """Fusiona multiples poligonos"""
        try:
            if not polygon_wkts or len(polygon_wkts) < 2:
                return None
            
            geometries = [wkt.loads(wkt_str) for wkt_str in polygon_wkts]
            from shapely.ops import unary_union
            
            merged = unary_union(geometries)
            return wkt.dumps(merged)
        except Exception as e:
            logger.error(f"Error fusionando: {e}")
            raise ValidationException(f"No se pueden fusionar: {str(e)}")
    
    @staticmethod
    def buffer_polygon(geom_wkt: str, buffer_distance: float) -> str:
        """Expande o contrae poligono"""
        try:
            geom = wkt.loads(geom_wkt)
            buffered = geom.buffer(buffer_distance)
            return wkt.dumps(buffered)
        except Exception as e:
            logger.error(f"Error en buffer: {e}")
            raise ValidationException(f"Error: {str(e)}")
    
    @staticmethod
    def simplify_polygon(geom_wkt: str, tolerance: float = 0.0001) -> str:
        """Simplifica poligono reduciendo vertices"""
        try:
            geom = wkt.loads(geom_wkt)
            simplified = geom.simplify(tolerance)
            return wkt.dumps(simplified)
        except Exception as e:
            raise ValidationException(f"Error: {str(e)}")
    
    @staticmethod
    def validate_drawn_polygon(coordinates: list) -> tuple:
        """Valida poligono dibujado"""
        try:
            if len(coordinates) < 3:
                return False, "Se necesitan al menos 3 puntos"
            
            if coordinates[0] != coordinates[-1]:
                coordinates = coordinates + [coordinates[0]]
            
            polygon = ShapelyPolygon(coordinates)
            
            if not polygon.is_valid:
                return False, "Poligono invalido"
            
            if polygon.area == 0:
                return False, "Poligono sin area"
            
            return True, "Valido"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def coordinates_to_wkt(coordinates: list) -> str:
        """Convierte coordenadas a WKT"""
        try:
            if coordinates[0] != coordinates[-1]:
                coordinates = coordinates + [coordinates[0]]
            
            coords = [(c[1], c[0]) for c in coordinates]
            polygon = ShapelyPolygon(coords)
            return wkt.dumps(polygon)
        except Exception as e:
            raise ValidationException(f"Coordenadas invalidas: {str(e)}")
    
    @staticmethod
    def get_polygon_vertices(geom_wkt: str) -> list:
        """Obtiene vertices de poligono"""
        try:
            geom = wkt.loads(geom_wkt)
            if geom.geom_type == "Polygon":
                coords = list(geom.exterior.coords)
                return [[c[1], c[0]] for c in coords]
            return []
        except Exception as e:
            logger.error(f"Error obteniendo vertices: {e}")
            return []
    
    @staticmethod
    def calculate_polygon_stats(geom_wkt: str) -> dict:
        """Calcula estadisticas del poligono"""
        try:
            geom = wkt.loads(geom_wkt)
            
            if geom.geom_type == "Polygon":
                vertices = list(geom.exterior.coords)
                
                return {
                    "num_vertices": len(vertices) - 1,
                    "area": float(geom.area),
                    "perimeter": float(geom.length),
                    "centroid": {
                        "lng": float(geom.centroid.x),
                        "lat": float(geom.centroid.y)
                    }
                }
            return {}
        except Exception as e:
            logger.error(f"Error calculando estadisticas: {e}")
            return {}
