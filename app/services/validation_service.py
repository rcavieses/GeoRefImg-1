from sqlalchemy.orm import Session
from app.models.validation import Validation
from app.utils.exceptions import NotFoundException

class ValidationService:
    @staticmethod
    def create_validation(db: Session, polygon_id: int, validator_id: int, status: str, validation_type: str = None, score: float = None, notes: str = None) -> Validation:
        """Crea una validación"""
        validation = Validation(
            polygon_id=polygon_id,
            validator_id=validator_id,
            status=status,
            validation_type=validation_type,
            score=score,
            notes=notes,
        )
        db.add(validation)
        db.commit()
        db.refresh(validation)
        return validation
    
    @staticmethod
    def get_validations(db: Session, polygon_id: int) -> list:
        """Obtiene validaciones de un polígono"""
        return db.query(Validation).filter(Validation.polygon_id == polygon_id).all()
    
    @staticmethod
    def get_validation(db: Session, validation_id: int) -> Validation:
        """Obtiene una validación por ID"""
        validation = db.query(Validation).filter(Validation.id == validation_id).first()
        if not validation:
            raise NotFoundException("Validación")
        return validation
