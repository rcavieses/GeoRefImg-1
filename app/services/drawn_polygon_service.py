from datetime import datetime
from sqlalchemy.orm import Session
from app.models.drawn_polygon import DrawnPolygon
from app.utils.logger import logger
from app.utils.exceptions import ValidationException
import json

class DrawnPolygonService:
    """Servicio para gestionar polígonos dibujados por usuarios"""

    @staticmethod
    def create_drawn_polygon(
        db: Session,
        user_id: int,
        name: str,
        justification: str,
        geojson_data: dict = None
    ) -> DrawnPolygon:
        """
        Crea un registro de polígono dibujado

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario que dibuja
            name: Nombre del polígono
            justification: Justificación de por qué se creó el polígono
            geojson_data: Datos GeoJSON del polígono (opcional)

        Returns:
            DrawnPolygon creado

        Raises:
            ValidationException si hay error
        """
        try:
            if not name or not name.strip():
                raise ValidationException("El nombre no puede estar vacío")

            if not justification or not justification.strip():
                raise ValidationException("La justificación no puede estar vacía")

            # Convertir GeoJSON a string si es necesario
            geojson_str = None
            if geojson_data:
                try:
                    geojson_str = json.dumps(geojson_data)
                except:
                    pass

            polygon = DrawnPolygon(
                user_id=user_id,
                name=name,
                justification=justification,
                geojson_data=geojson_str
            )

            db.add(polygon)
            db.commit()
            db.refresh(polygon)

            logger.info(f"Polígono dibujado '{name}' creado por usuario #{user_id}")

            return polygon

        except ValidationException:
            raise
        except Exception as e:
            db.rollback()
            raise ValidationException(f"Error creando polígono dibujado: {str(e)}")

    @staticmethod
    def get_recent_drawn_polygons(db: Session, limit: int = 20) -> list:
        """
        Obtiene los polígonos dibujados más recientes

        Args:
            db: Sesión de base de datos
            limit: Número máximo de polígonos a retornar

        Returns:
            Lista de polígonos dibujados recientes
        """
        try:
            polygons = db.query(DrawnPolygon).order_by(
                DrawnPolygon.created_at.desc()
            ).limit(limit).all()

            return polygons
        except Exception as e:
            logger.error(f"Error obteniendo polígonos dibujados: {str(e)}")
            return []

    @staticmethod
    def get_user_drawn_polygons(db: Session, user_id: int) -> list:
        """
        Obtiene todos los polígonos dibujados por un usuario

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario

        Returns:
            Lista de polígonos dibujados del usuario
        """
        try:
            polygons = db.query(DrawnPolygon).filter(
                DrawnPolygon.user_id == user_id
            ).order_by(DrawnPolygon.created_at.desc()).all()

            return polygons
        except Exception as e:
            logger.error(f"Error obteniendo polígonos del usuario: {str(e)}")
            return []
