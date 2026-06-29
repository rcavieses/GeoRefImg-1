import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.polygon import Polygon
from app.models.validation import Validation
from app.models.annotation import Annotation
from app.models.user import User
from app.utils.logger import logger

class ReportService:
    """Servicio para generar reportes y estadisticas"""
    
    @staticmethod
    def get_system_overview(db: Session) -> dict:
        """Obtiene resumen general del sistema"""
        try:
            total_polygons = db.query(func.count(Polygon.id)).scalar() or 0
            total_validations = db.query(func.count(Validation.id)).scalar() or 0
            total_annotations = db.query(func.count(Annotation.id)).scalar() or 0
            total_users = db.query(func.count(User.id)).scalar() or 0
            
            validation_stats = db.query(
                Validation.status,
                func.count(Validation.id)
            ).group_by(Validation.status).all()
            
            by_status = {status: count for status, count in validation_stats}
            
            polygon_stats = db.query(
                Polygon.source_type,
                func.count(Polygon.id)
            ).group_by(Polygon.source_type).all()
            
            by_source = {source or 'unknown': count for source, count in polygon_stats}
            
            avg_score = db.query(func.avg(Validation.score)).scalar() or 0
            
            total_val = total_validations if total_validations > 0 else 1
            approval_rate = (by_status.get("approved", 0) / total_val * 100)
            
            return {
                "total_polygons": int(total_polygons),
                "total_validations": int(total_validations),
                "total_annotations": int(total_annotations),
                "total_users": int(total_users),
                "validations_by_status": by_status,
                "polygons_by_source": by_source,
                "average_validation_score": float(avg_score),
                "approval_rate": float(approval_rate),
                "generated_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}
    
    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Obtiene estadisticas de un usuario"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {}
            
            polygons_created = db.query(func.count(Polygon.id)).filter(
                Polygon.created_by == user_id
            ).scalar() or 0
            
            validations_done = db.query(func.count(Validation.id)).filter(
                Validation.validator_id == user_id
            ).scalar() or 0
            
            annotations_created = db.query(func.count(Annotation.id)).filter(
                Annotation.author_id == user_id
            ).scalar() or 0
            
            avg_score = db.query(func.avg(Validation.score)).filter(
                Validation.validator_id == user_id
            ).scalar() or 0
            
            approved = db.query(func.count(Validation.id)).filter(
                Validation.validator_id == user_id,
                Validation.status == "approved"
            ).scalar() or 0
            
            val_done = validations_done if validations_done > 0 else 1
            approval_rate = (approved / val_done * 100)
            
            return {
                "user_id": user_id,
                "username": user.username,
                "polygons_created": int(polygons_created),
                "validations_done": int(validations_done),
                "annotations_created": int(annotations_created),
                "average_score": float(avg_score),
                "approval_rate": float(approval_rate),
                "role": user.role
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}
    
    @staticmethod
    def get_top_validators(db: Session, limit: int = 10) -> list:
        """Obtiene validadores con mas validaciones"""
        try:
            validators = db.query(
                User.id,
                User.username,
                func.count(Validation.id).label('count'),
                func.avg(Validation.score).label('avg_score')
            ).join(Validation, User.id == Validation.validator_id).group_by(
                User.id
            ).order_by(func.count(Validation.id).desc()).limit(limit).all()
            
            return [
                {
                    "user_id": v[0],
                    "username": v[1],
                    "validations_count": int(v[2]),
                    "avg_score": float(v[3] or 0)
                }
                for v in validators
            ]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
