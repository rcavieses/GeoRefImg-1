from datetime import datetime
from sqlalchemy.orm import Session
from app.models.point_annotation import PointAnnotation
from app.utils.logger import logger
from app.utils.exceptions import ValidationException

class AnnotationService:
    """Servicio para gestionar anotaciones puntuales"""

    @staticmethod
    def create_point_annotation(
        db: Session,
        user_id: int,
        latitude: float,
        longitude: float,
        annotation_type: str,
        description: str
    ) -> PointAnnotation:
        """Crea una anotación puntual en el mapa"""
        try:
            if not (-90 <= latitude <= 90):
                raise ValidationException("Latitud debe estar entre -90 y 90")
            if not (-180 <= longitude <= 180):
                raise ValidationException("Longitud debe estar entre -180 y 180")
            if not description or not description.strip():
                raise ValidationException("La descripción no puede estar vacía")

            annotation = PointAnnotation(
                user_id=user_id,
                latitude=latitude,
                longitude=longitude,
                annotation_type=annotation_type,
                description=description
            )

            db.add(annotation)
            db.commit()
            db.refresh(annotation)

            logger.info(f"Anotación puntual creada en ({latitude:.6f}, {longitude:.6f}) por usuario #{user_id}")

            return annotation

        except ValidationException:
            raise
        except Exception as e:
            db.rollback()
            raise ValidationException(f"Error creando anotación: {str(e)}")

    @staticmethod
    def get_recent_annotations(db: Session, limit: int = 20) -> list:
        """Obtiene las anotaciones más recientes"""
        try:
            annotations = db.query(PointAnnotation).order_by(
                PointAnnotation.created_at.desc()
            ).limit(limit).all()
            return annotations
        except Exception as e:
            logger.error(f"Error obteniendo anotaciones: {str(e)}")
            return []

    @staticmethod
    def get_user_annotations(db: Session, user_id: int) -> list:
        """Obtiene todas las anotaciones de un usuario"""
        try:
            annotations = db.query(PointAnnotation).filter(
                PointAnnotation.user_id == user_id
            ).order_by(PointAnnotation.created_at.desc()).all()
            return annotations
        except Exception as e:
            logger.error(f"Error obteniendo anotaciones: {str(e)}")
            return []
