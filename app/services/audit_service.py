from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.utils.helpers import dict_to_json

class AuditService:
    @staticmethod
    def log_action(db: Session, entity_type: str, entity_id: int, action: str, user_id: int, changes: dict = None, old_values: dict = None, new_values: dict = None):
        """Registra una acción en el audit log"""
        audit_log = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            user_id=user_id,
            changes=dict_to_json(changes) if changes else None,
            old_values=dict_to_json(old_values) if old_values else None,
            new_values=dict_to_json(new_values) if new_values else None,
        )
        db.add(audit_log)
        db.commit()
