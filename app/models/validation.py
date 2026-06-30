from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Validation(Base):
    __tablename__ = "validations"
    
    id = Column(Integer, primary_key=True, index=True)
    polygon_id = Column(Integer, ForeignKey("polygons.id"), nullable=False)
    validator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # 'pending', 'approved', 'rejected', 'needs_revision', 'merged'
    validation_type = Column(String(100), nullable=True)  # 'topology', 'accuracy', 'manual'
    score = Column(Float, nullable=True)
    notes = Column(String(2000), nullable=True)
    validation_metadata = Column(String(2000), nullable=True)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
