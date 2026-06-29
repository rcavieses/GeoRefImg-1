from shapely.geometry import shape
from shapely.validation import make_valid
import logging

logger = logging.getLogger(__name__)

class GeometryService:
    """Servicio para validación y procesamiento de geometrías"""
    
    @staticmethod
    def validate_geometry(geom_wkt: str) -> dict:
        """
        Valida una geometría en formato WKT
        
        Args:
            geom_wkt: Geometría en WKT
            
        Returns:
            dict con resultado de validación
        """
        try:
            from shapely import wkt
            
            geom = wkt.loads(geom_wkt)
            
            result = {
                "is_valid": geom.is_valid,
                "geom_type": geom.geom_type,
                "is_empty": geom.is_empty,
                "is_ring": hasattr(geom, 'is_ring') and geom.is_ring,
                "errors": []
            }
            
            # Validaciones específicas
            if geom.is_empty:
                result["errors"].append("Geometría vacía")
            
            if not geom.is_valid:
                result["errors"].append(f"Geometría inválida: {geom.is_valid}")
            
            # Para polígonos
            if geom.geom_type == "Polygon":
                if geom.exterior is None:
                    result["errors"].append("Polígono sin anillo exterior")
                
                if len(geom.interiors) > 0:
                    result["num_holes"] = len(geom.interiors)
            
            return result
        
        except Exception as e:
            logger.error(f"Error validando geometría: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)]
            }
    
    @staticmethod
    def validate_topology(geom_wkt: str) -> dict:
        """
        Valida topología de una geometría
        
        Args:
            geom_wkt: Geometría en WKT
            
        Returns:
            dict con validaciones topológicas
        """
        try:
            from shapely import wkt
            
            geom = wkt.loads(geom_wkt)
            
            result = {
                "is_valid": True,
                "warnings": [],
                "errors": []
            }
            
            # Verificar si es cerrado
            if geom.geom_type == "Polygon":
                if not geom.exterior.is_ring:
                    result["errors"].append("Anillo exterior no está cerrado")
                    result["is_valid"] = False
                
                # Verificar orientación
                if geom.exterior.is_ccw:
                    result["warnings"].append("Anillo orientado en sentido contrario")
            
            # Verificar auto-intersecciones
            if not geom.is_valid:
                result["errors"].append("Tiene auto-intersecciones")
                result["is_valid"] = False
            
            # Mínimo número de vértices
            if geom.geom_type == "Polygon":
                coords_count = len(list(geom.exterior.coords))
                if coords_count < 4:  # 3 puntos + cierre
                    result["errors"].append(f"Muy pocos vértices ({coords_count})")
                    result["is_valid"] = False
            
            return result
        
        except Exception as e:
            logger.error(f"Error validando topología: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)]
            }
    
    @staticmethod
    def check_geometry_overlap(geom1_wkt: str, geom2_wkt: str) -> dict:
        """
        Verifica si dos geometrías se superponen
        
        Args:
            geom1_wkt: Primera geometría
            geom2_wkt: Segunda geometría
            
        Returns:
            dict con resultado
        """
        try:
            from shapely import wkt
            
            geom1 = wkt.loads(geom1_wkt)
            geom2 = wkt.loads(geom2_wkt)
            
            overlaps = geom1.overlaps(geom2)
            intersects = geom1.intersects(geom2)
            
            return {
                "overlaps": overlaps,
                "intersects": intersects,
                "intersection_area": float(geom1.intersection(geom2).area) if intersects else 0
            }
        
        except Exception as e:
            logger.error(f"Error verificando overlaps: {e}")
            return {
                "overlaps": False,
                "intersects": False,
                "error": str(e)
            }
    
    @staticmethod
    def fix_geometry(geom_wkt: str) -> str | None:
        """
        Intenta arreglar una geometría inválida
        
        Args:
            geom_wkt: Geometría inválida en WKT
            
        Returns:
            Geometría arreglada en WKT o None
        """
        try:
            from shapely import wkt
            
            geom = wkt.loads(geom_wkt)
            
            if not geom.is_valid:
                fixed = make_valid(geom)
                return wkt.dumps(fixed)
            
            return geom_wkt
        
        except Exception as e:
            logger.error(f"Error arreglando geometría: {e}")
            return None
    
    @staticmethod
    def calculate_quality_score(geom_wkt: str) -> float:
        """
        Calcula un score de calidad de la geometría (0-100)
        
        Args:
            geom_wkt: Geometría en WKT
            
        Returns:
            float entre 0 y 100
        """
        score = 100.0
        
        try:
            # Validación básica
            validation = GeometryService.validate_geometry(geom_wkt)
            if not validation["is_valid"]:
                score -= 30
            
            # Validación topológica
            topology = GeometryService.validate_topology(geom_wkt)
            if not topology["is_valid"]:
                score -= 20
            
            # Warnings
            if topology.get("warnings"):
                score -= 10 * len(topology["warnings"])
            
            # Clamping
            return max(0, min(100, score))
        
        except Exception as e:
            logger.error(f"Error calculando score: {e}")
            return 0.0
