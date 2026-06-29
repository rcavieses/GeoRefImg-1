import pytest
from app.services.user_service import UserService
from app.services.polygon_service import PolygonService
from app.services.validation_service import ValidationService
from app.services.annotation_service import AnnotationService
from app.services.drawing_service import DrawingService
from app.services.report_service import ReportService

class TestFullWorkflow:
    """Tests de flujo completo del sistema"""
    
    def test_user_creation_and_auth(self, db):
        """Test crear usuario y autenticar"""
        user = UserService.create_user(
            db, "testuser", "test@example.com", "TestPassword123"
        )
        
        authenticated = UserService.authenticate_user(
            db, "testuser", "TestPassword123"
        )
        
        assert authenticated.id == user.id
    
    def test_polygon_lifecycle(self, db, admin_user):
        """Test ciclo de vida de polígono"""
        polygon = PolygonService.create_polygon(
            db, "Test", "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",
            created_by=admin_user.id
        )
        
        retrieved = PolygonService.get_polygon(db, polygon.id)
        assert retrieved.name == "Test"
        
        updated = PolygonService.update_polygon(
            db, polygon.id, name="Updated"
        )
        assert updated.name == "Updated"
    
    def test_validation_with_annotation(self, db, admin_user, test_polygon):
        """Test validar polígono y anotar"""
        validation = ValidationService.create_validation(
            db, test_polygon.id, admin_user.id, "pending"
        )
        
        annotation = AnnotationService.create_annotation(
            db, test_polygon.id, admin_user.id,
            "Necesita revisión", "flag"
        )
        
        approved = ValidationService.approve_validation(
            db, validation.id, "Aprobado"
        )
        
        assert approved.status == "approved"
        assert annotation.is_resolved == False
    
    def test_drawing_and_save(self, db, admin_user):
        """Test dibujar y guardar polígono"""
        coords = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
        
        is_valid, msg = DrawingService.validate_drawn_polygon(coords)
        assert is_valid is True
        
        wkt = DrawingService.coordinates_to_wkt(coords)
        
        polygon = PolygonService.create_polygon(
            db, "Drawn Polygon", wkt,
            created_by=admin_user.id,
            source_type="drawn"
        )
        
        assert polygon.source_type == "drawn"
    
    def test_system_statistics(self, db, admin_user, test_polygon):
        """Test obtener estadísticas del sistema"""
        ValidationService.create_validation(
            db, test_polygon.id, admin_user.id, "approved"
        )
        
        overview = ReportService.get_system_overview(db)
        
        assert overview["total_polygons"] == 1
        assert overview["total_validations"] == 1
    
    def test_multi_user_collaboration(self, db, admin_user, validator_user, test_polygon):
        """Test colaboración entre usuarios"""
        annotation1 = AnnotationService.create_annotation(
            db, test_polygon.id, admin_user.id,
            "Comentario del admin", "comment"
        )
        
        annotation2 = AnnotationService.create_annotation(
            db, test_polygon.id, validator_user.id,
            "Comentario del validador", "comment"
        )
        
        annotations = AnnotationService.get_annotations(db, test_polygon.id)
        assert len(annotations) == 2
    
    def test_geometry_operations(self):
        """Test operaciones geométricas"""
        wkt1 = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        wkt2 = "POLYGON((1 0, 2 0, 2 1, 1 1, 1 0))"
        
        merged = DrawingService.merge_polygons([wkt1, wkt2])
        assert merged is not None
        
        stats = DrawingService.calculate_polygon_stats(wkt1)
        assert stats["num_vertices"] == 4
