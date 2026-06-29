from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Polygon(Base):
    __tablename__ = "polygons"
    
    id = Column(Integer, primary_key=True, index=True)
    geopackage_id = Column(Integer, nullable=True)  # ID original del geopackage
    name = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_type = Column(String(50), nullable=True)  # 'geopackage' | 'drawn'
    geom_wkt = Column(String(8000), nullable=True)  # Well-Known Text
    bbox = Column(String(500), nullable=True)  # JSON string
    area_sqm = Column(Float, nullable=True)
    properties = Column(String(2000), nullable=True)  # JSON string
    is_validated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
