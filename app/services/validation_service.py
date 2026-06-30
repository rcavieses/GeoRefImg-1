from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.validation import Validation
from app.models.polygon import Polygon
from app.utils.exceptions import NotFoundException, ValidationException
from app.utils.logger import logger
import json

class ValidationService:
    """Servicio para gestión de validaciones"""

    # Estados válidos
    VALID_STATUSES = ["pending", "approved", "rejected", "needs_revision"]
    VALID_TYPES = ["topology", "accuracy", "completeness", "manual"]

    @staticmethod
    def create_validation(db: Session, polygon_id: int, validator_id: int, status: str,
                         validation_type: str = None, score: float = None, notes: str = None,
                         metadata: dict = None) -> Validation:
        """
        Crea una validación

        Args:
            db: Sesión de BD
            polygon_id: ID del polígono
            validator_id: ID del validador
            status: Estado (pending, approved, rejected, needs_revision)
            validation_type: Tipo de validación
            score: Puntuación 0-100
            notes: Notas de validación
            metadata: Datos adicionales en JSON

        Returns:
            Validation object
        """
        # Validar estado
        if status not in ValidationService.VALID_STATUSES:
            raise ValidationException(f"Status inválido: {status}")

        # Validar score
        if score is not None and not (0 <= score <= 100):
            raise ValidationException("Score debe estar entre 0 y 100")

        metadata_json = json.dumps(metadata) if metadata else None

        validation = Validation(
            polygon_id=polygon_id,
            validator_id=validator_id,
            status=status,
            validation_type=validation_type,
            score=score,
            notes=notes,
            validation_metadata=metadata_json
        )

        db.add(validation)
        db.commit()
        db.refresh(validation)

        logger.info(f"Validación creada: {validation.id} para polígono {polygon_id}")

        return validation

    @staticmethod
    def get_validations(db: Session, polygon_id: int) -> list:
        """Obtiene validaciones de un polígono"""
        return db.query(Validation).filter(
            Validation.polygon_id == polygon_id
        ).order_by(Validation.created_at.desc()).all()

    @staticmethod
    def get_validation(db: Session, validation_id: int) -> Validation:
        """Obtiene una validación por ID"""
        validation = db.query(Validation).filter(Validation.id == validation_id).first()
        if not validation:
            raise NotFoundException("Validación")
        return validation

    @staticmethod
    def get_validator_validations(db: Session, validator_id: int, status: str = None) -> list:
        """Obtiene validaciones de un validador específico"""
        query = db.query(Validation).filter(Validation.validator_id == validator_id)

        if status:
            query = query.filter(Validation.status == status)

        return query.order_by(Validation.created_at.desc()).all()

    @staticmethod
    def update_validation(db: Session, validation_id: int, **kwargs) -> Validation:
        """Actualiza una validación"""
        validation = ValidationService.get_validation(db, validation_id)

        for key, value in kwargs.items():
            if hasattr(validation, key):
                if key == "score" and value is not None:
                    if not (0 <= value <= 100):
                        raise ValidationException("Score debe estar entre 0 y 100")

                setattr(validation, key, value)

        db.commit()
        db.refresh(validation)

        logger.info(f"Validación {validation_id} actualizada")

        return validation

    @staticmethod
    def get_polygon_validation_summary(db: Session, polygon_id: int) -> dict:
        """Obtiene resumen de validaciones de un polígono"""
        validations = ValidationService.get_validations(db, polygon_id)

        if not validations:
            return {
                "polygon_id": polygon_id,
                "total": 0,
                "by_status": {},
                "average_score": 0,
                "approved": False,
                "latest": None
            }

        by_status = {}
        total_score = 0
        count_scores = 0

        for val in validations:
            status = val.status
            by_status[status] = by_status.get(status, 0) + 1

            if val.score is not None:
                total_score += val.score
                count_scores += 1

        avg_score = total_score / count_scores if count_scores > 0 else 0
        approved = by_status.get("approved", 0) > 0

        return {
            "polygon_id": polygon_id,
            "total": len(validations),
            "by_status": by_status,
            "average_score": round(avg_score, 2),
            "approved": approved,
            "latest": validations[0] if validations else None
        }

    @staticmethod
    def get_validation_stats(db: Session) -> dict:
        """Obtiene estadísticas globales de validaciones"""
        all_validations = db.query(Validation).all()

        if not all_validations:
            return {
                "total": 0,
                "by_status": {},
                "average_score": 0
            }

        by_status = {}
        total_score = 0
        count_scores = 0

        for val in all_validations:
            status = val.status
            by_status[status] = by_status.get(status, 0) + 1

            if val.score is not None:
                total_score += val.score
                count_scores += 1

        avg_score = total_score / count_scores if count_scores > 0 else 0

        return {
            "total": len(all_validations),
            "by_status": by_status,
            "average_score": round(avg_score, 2),
            "approval_rate": round(by_status.get("approved", 0) / len(all_validations) * 100, 2) if all_validations else 0
        }

    @staticmethod
    def get_pending_validations(db: Session, limit: int = 10) -> list:
        """Obtiene validaciones pendientes"""
        return db.query(Validation).filter(
            Validation.status == "pending"
        ).order_by(Validation.created_at.asc()).limit(limit).all()

    @staticmethod
    def approve_validation(db: Session, validation_id: int, notes: str = None) -> Validation:
        """Aprueba una validación"""
        return ValidationService.update_validation(
            db, validation_id,
            status="approved",
            notes=notes or ""
        )

    @staticmethod
    def reject_validation(db: Session, validation_id: int, notes: str = None) -> Validation:
        """Rechaza una validación"""
        return ValidationService.update_validation(
            db, validation_id,
            status="rejected",
            notes=notes or ""
        )

    @staticmethod
    def mark_needs_revision(db: Session, validation_id: int, notes: str = None) -> Validation:
        """Marca como requiere revisión"""
        return ValidationService.update_validation(
            db, validation_id,
            status="needs_revision",
            notes=notes or ""
        )
