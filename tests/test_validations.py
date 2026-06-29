import pytest
from app.services.validation_service import ValidationService
from app.services.user_service import UserService
from app.services.polygon_service import PolygonService
from app.services.geometry_service import GeometryService
from app.utils.exceptions import ValidationException, NotFoundException

@pytest.fixture
def user(db):
    return UserService.create_user(
        db, "validator", "val@test.com", "TestPassword123"
    )

@pytest.fixture
def polygon(db, user):
    return PolygonService.create_polygon(
        db, "Test", "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",
        created_by=user.id, source_type="test"
    )

class TestValidationService:
    
    def test_create_validation(self, db, user, polygon):
        validation = ValidationService.create_validation(
            db, polygon.id, user.id, "approved",
            validation_type="topology", score=85, notes="Valid"
        )
        
        assert validation.id is not None
        assert validation.polygon_id == polygon.id
        assert validation.status == "approved"
        assert validation.score == 85
    
    def test_create_validation_invalid_status(self, db, user, polygon):
        with pytest.raises(ValidationException):
            ValidationService.create_validation(
                db, polygon.id, user.id, "invalid_status"
            )
    
    def test_create_validation_invalid_score(self, db, user, polygon):
        with pytest.raises(ValidationException):
            ValidationService.create_validation(
                db, polygon.id, user.id, "approved", score=150
            )
    
    def test_get_validations(self, db, user, polygon):
        for i in range(3):
            ValidationService.create_validation(
                db, polygon.id, user.id, "approved"
            )
        
        validations = ValidationService.get_validations(db, polygon.id)
        assert len(validations) == 3
    
    def test_get_validation(self, db, user, polygon):
        created = ValidationService.create_validation(
            db, polygon.id, user.id, "approved"
        )
        
        retrieved = ValidationService.get_validation(db, created.id)
        assert retrieved.id == created.id
    
    def test_update_validation(self, db, user, polygon):
        validation = ValidationService.create_validation(
            db, polygon.id, user.id, "pending"
        )
        
        updated = ValidationService.update_validation(
            db, validation.id, status="approved", score=90
        )
        
        assert updated.status == "approved"
        assert updated.score == 90
    
    def test_approve_validation(self, db, user, polygon):
        validation = ValidationService.create_validation(
            db, polygon.id, user.id, "pending"
        )
        
        approved = ValidationService.approve_validation(db, validation.id)
        assert approved.status == "approved"
    
    def test_reject_validation(self, db, user, polygon):
        validation = ValidationService.create_validation(
            db, polygon.id, user.id, "pending"
        )
        
        rejected = ValidationService.reject_validation(db, validation.id)
        assert rejected.status == "rejected"
    
    def test_get_validator_validations(self, db, user, polygon):
        for i in range(2):
            ValidationService.create_validation(
                db, polygon.id, user.id, "approved"
            )
        
        validations = ValidationService.get_validator_validations(db, user.id)
        assert len(validations) == 2

class TestGeometryService:
    
    def test_validate_geometry_valid(self):
        geom_wkt = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        result = GeometryService.validate_geometry(geom_wkt)
        
        assert result["is_valid"] is True
        assert result["geom_type"] == "Polygon"
    
    def test_validate_topology(self):
        geom_wkt = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        result = GeometryService.validate_topology(geom_wkt)
        
        assert result["is_valid"] is True
    
    def test_calculate_quality_score(self):
        geom_wkt = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        score = GeometryService.calculate_quality_score(geom_wkt)
        
        assert 0 <= score <= 100
        assert score == 100
