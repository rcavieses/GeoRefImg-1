from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(100), nullable=False)  # 'polygon', 'validation', 'annotation'
    entity_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)  # 'create', 'update', 'delete', 'validate'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    changes = Column(String(2000), nullable=True)  # JSON diff
    old_values = Column(String(2000), nullable=True)
    new_values = Column(String(2000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
