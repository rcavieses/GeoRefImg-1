import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.user_service import UserService
from app.services.polygon_service import PolygonService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_advanced.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """BD de prueba limpia para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def admin_user(db):
    """Usuario admin de prueba"""
    return UserService.create_user(
        db, "admin", "admin@test.com", "AdminPassword123"
    )

@pytest.fixture
def validator_user(db):
    """Usuario validador de prueba"""
    user = UserService.create_user(
        db, "validator", "validator@test.com", "ValidPassword123"
    )
    user.role = "validator"
    db.commit()
    return user

@pytest.fixture
def test_polygon(db, admin_user):
    """Polígono de prueba"""
    return PolygonService.create_polygon(
        db,
        name="Test Polygon",
        geom_wkt="POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",
        created_by=admin_user.id,
        source_type="test"
    )

@pytest.fixture
def sample_geojson():
    """GeoJSON de ejemplo"""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        },
        "properties": {"name": "Test"}
    }
