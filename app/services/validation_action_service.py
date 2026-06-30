from datetime import datetime
from sqlalchemy.orm import Session
from app.models.validation import Validation
from app.utils.logger import logger
from app.utils.exceptions import ValidationException

class ValidationActionService:
    """Servicio para registrar acciones de validación de polígonos"""

    @staticmethod
    def record_validation_action(
        db: Session,
        polygon_id: int,
        user_id: int,
        action: str,
        notes: str = None,
        related_polygon_ids: list = None
    ) -> Validation:
        """
        Registra una acción de validación

        Args:
            db: Sesión de base de datos
            polygon_id: ID del polígono siendo validado
            user_id: ID del usuario que realiza la acción
            action: Tipo de acción ('approved', 'rejected', 'review', 'merge_initiated')
            notes: Notas adicionales sobre la acción
            related_polygon_ids: IDs de polígonos relacionados (para merge)

        Returns:
            Objeto Validation creado

        Raises:
            ValidationException si hay error
        """
        try:
            # Mapear acciones a estados de validación
            status_map = {
                "approved": "approved",
                "rejected": "rejected",
                "review": "needs_revision",
                "merge_initiated": "pending"
            }

            status = status_map.get(action, "pending")

            # Crear datos de metadatos
            metadata_dict = {
                "action": action,
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
            }

            if related_polygon_ids:
                metadata_dict["related_polygon_ids"] = related_polygon_ids

            if notes:
                metadata_dict["notes"] = notes

            import json
            metadata_json = json.dumps(metadata_dict)

            # Crear o actualizar validación
            validation = Validation(
                polygon_id=polygon_id,
                validator_id=user_id,
                status=status,
                validation_type="user_review",
                notes=notes,
                validation_metadata=metadata_json
            )

            db.add(validation)
            db.commit()
            db.refresh(validation)

            logger.info(f"Acción '{action}' registrada para polígono #{polygon_id} por usuario #{user_id}")

            return validation

        except Exception as e:
            db.rollback()
            raise ValidationException(f"Error registrando acción de validación: {str(e)}")

    @staticmethod
    def get_polygon_validation_history(db: Session, polygon_id: int) -> list:
        """
        Obtiene el historial de validaciones de un polígono

        Args:
            db: Sesión de base de datos
            polygon_id: ID del polígono

        Returns:
            Lista de acciones de validación
        """
        try:
            validations = db.query(Validation).filter(
                Validation.polygon_id == polygon_id
            ).order_by(Validation.created_at.desc()).all()

            return validations
        except Exception as e:
            logger.error(f"Error obteniendo historial: {str(e)}")
            return []

    @staticmethod
    def record_merge_action(
        db: Session,
        source_polygon_ids: list,
        target_polygon_id: int,
        user_id: int,
        merge_name: str
    ) -> dict:
        """
        Registra una acción de fusión de polígonos

        Args:
            db: Sesión de base de datos
            source_polygon_ids: IDs de polígonos a fusionar
            target_polygon_id: ID del polígono resultado (puede ser nuevo)
            user_id: ID del usuario
            merge_name: Nombre del polígono fusionado

        Returns:
            dict con resultado de la operación
        """
        try:
            import json

            # Registrar acción para cada polígono origen
            for poly_id in source_polygon_ids:
                metadata = {
                    "action": "merged",
                    "timestamp": datetime.utcnow().isoformat(),
                    "user_id": user_id,
                    "merged_into": target_polygon_id,
                    "merge_name": merge_name,
                    "source_polygons": source_polygon_ids
                }

                validation = Validation(
                    polygon_id=poly_id,
                    validator_id=user_id,
                    status="merged",
                    validation_type="merge",
                    notes=f"Fusionado en polígono #{target_polygon_id}",
                    validation_metadata=json.dumps(metadata)
                )

                db.add(validation)

            db.commit()

            logger.info(f"Fusión registrada: {source_polygon_ids} → #{target_polygon_id}")

            return {
                "success": True,
                "message": f"Fusión registrada",
                "source_polygons": source_polygon_ids,
                "target_polygon_id": target_polygon_id
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error registrando fusión: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
