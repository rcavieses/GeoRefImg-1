import pytest
from app.services.report_service import ReportService
from app.services.user_service import UserService
from app.services.polygon_service import PolygonService
from app.services.validation_service import ValidationService

@pytest.fixture
def user(db):
    return UserService.create_user(
        db, "reporter", "reporter@test.com", "TestPassword123"
    )

@pytest.fixture
def polygon(db, user):
    return PolygonService.create_polygon(
        db, "Test", "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",
        created_by=user.id
    )

class TestReportService:
    
    def test_get_system_overview(self, db):
        """Test obtener overview del sistema"""
        overview = ReportService.get_system_overview(db)
        
        assert "total_polygons" in overview
        assert "total_validations" in overview
        assert "total_users" in overview
        assert "approval_rate" in overview
    
    def test_get_user_stats(self, db, user):
        """Test obtener stats de usuario"""
        stats = ReportService.get_user_stats(db, user.id)
        
        assert stats["user_id"] == user.id
        assert stats["username"] == "reporter"
        assert stats["polygons_created"] == 0
        assert stats["validations_done"] == 0
    
    def test_get_user_stats_with_data(self, db, user, polygon):
        """Test stats con datos"""
        ValidationService.create_validation(
            db, polygon.id, user.id, "approved"
        )
        
        stats = ReportService.get_user_stats(db, user.id)
        
        assert stats["validations_done"] == 1
    
    def test_get_top_validators(self, db, user):
        """Test obtener top validators"""
        validators = ReportService.get_top_validators(db, limit=5)
        
        assert isinstance(validators, list)
