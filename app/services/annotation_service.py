from sqlalchemy.orm import Session
from app.models.annotation import Annotation
from app.utils.exceptions import NotFoundException

class AnnotationService:
    @staticmethod
    def create_annotation(db: Session, polygon_id: int, author_id: int, content: str, annotation_type: str = "comment", location: str = None) -> Annotation:
        """Crea una anotación"""
        annotation = Annotation(
            polygon_id=polygon_id,
            author_id=author_id,
            content=content,
            annotation_type=annotation_type,
            location=location,
        )
        db.add(annotation)
        db.commit()
        db.refresh(annotation)
        return annotation
    
    @staticmethod
    def get_annotations(db: Session, polygon_id: int) -> list:
        """Obtiene anotaciones de un polígono"""
        return db.query(Annotation).filter(Annotation.polygon_id == polygon_id).all()
    
    @staticmethod
    def get_annotation(db: Session, annotation_id: int) -> Annotation:
        """Obtiene una anotación por ID"""
        annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
        if not annotation:
            raise NotFoundException("Anotación")
        return annotation
    
    @staticmethod
    def update_annotation(db: Session, annotation_id: int, **kwargs) -> Annotation:
        """Actualiza una anotación"""
        annotation = AnnotationService.get_annotation(db, annotation_id)
        for key, value in kwargs.items():
            if hasattr(annotation, key):
                setattr(annotation, key, value)
        db.commit()
        db.refresh(annotation)
        return annotation
