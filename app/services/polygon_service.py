from sqlalchemy.orm import Session
from app.models.polygon import Polygon
from app.utils.exceptions import NotFoundException

class PolygonService:
    @staticmethod
    def get_all_polygons(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Obtiene todos los polígonos"""
        return db.query(Polygon).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_polygon(db: Session, polygon_id: int) -> Polygon:
        """Obtiene un polígono por ID"""
        polygon = db.query(Polygon).filter(Polygon.id == polygon_id).first()
        if not polygon:
            raise NotFoundException("Polígono")
        return polygon
    
    @staticmethod
    def get_polygons_by_source(db: Session, source_type: str) -> list:
        """Obtiene polígonos por tipo de fuente"""
        return db.query(Polygon).filter(Polygon.source_type == source_type).all()
    
    @staticmethod
    def create_polygon(db: Session, name: str, geom_wkt: str, created_by: int, source_type: str = "drawn", **kwargs) -> Polygon:
        """Crea un nuevo polígono"""
        polygon = Polygon(
            name=name,
            geom_wkt=geom_wkt,
            created_by=created_by,
            source_type=source_type,
            **kwargs
        )
        db.add(polygon)
        db.commit()
        db.refresh(polygon)
        return polygon
    
    @staticmethod
    def update_polygon(db: Session, polygon_id: int, **kwargs) -> Polygon:
        """Actualiza un polígono"""
        polygon = PolygonService.get_polygon(db, polygon_id)
        for key, value in kwargs.items():
            if hasattr(polygon, key):
                setattr(polygon, key, value)
        db.commit()
        db.refresh(polygon)
        return polygon
