import pytest
import json
from datetime import datetime
from app.services.annotation_service import AnnotationService
from app.services.user_service import UserService
from app.services.polygon_service import PolygonService
from app.utils.exceptions import NotFoundException

@pytest.fixture
def user(db):
    """Crea un usuario de prueba"""
    return UserService.create_user(
        db,
        username="annotator",
        email="annotator@test.com",
        password="TestPassword123"
    )

@pytest.fixture
def polygon(db, user):
    """Crea un polígono de prueba"""
    return PolygonService.create_polygon(
        db,
        name="Test Polygon",
        geom_wkt="POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",
        created_by=user.id,
        source_type="test"
    )

class TestAnnotationService:
    """Tests para AnnotationService"""
    
    def test_create_annotation(self, db, user, polygon):
        """Test crear anotacion"""
        annotation = AnnotationService.create_annotation(
            db=db,
            polygon_id=polygon.id,
            author_id=user.id,
            content="Test annotation",
            annotation_type="comment"
        )
        
        assert annotation.id is not None
        assert annotation.polygon_id == polygon.id
        assert annotation.author_id == user.id
        assert annotation.content == "Test annotation"
        assert annotation.annotation_type == "comment"
        assert annotation.is_resolved is False
    
    def test_create_annotation_flag(self, db, user, polygon):
        """Test crear flag"""
        annotation = AnnotationService.create_annotation(
            db=db,
            polygon_id=polygon.id,
            author_id=user.id,
            content="Limite incorrecto",
            annotation_type="flag"
        )
        
        assert annotation.annotation_type == "flag"
    
    def test_get_annotations(self, db, user, polygon):
        """Test obtener anotaciones de un poligono"""
        for i in range(3):
            AnnotationService.create_annotation(
                db=db,
                polygon_id=polygon.id,
                author_id=user.id,
                content=f"Anotacion {i+1}",
                annotation_type="comment"
            )
        
        annotations = AnnotationService.get_annotations(db, polygon.id)
        
        assert len(annotations) == 3
        assert all(a.polygon_id == polygon.id for a in annotations)
    
    def test_get_annotation(self, db, user, polygon):
        """Test obtener una anotacion por ID"""
        created = AnnotationService.create_annotation(
            db=db,
            polygon_id=polygon.id,
            author_id=user.id,
            content="Test",
            annotation_type="comment"
        )
        
        retrieved = AnnotationService.get_annotation(db, created.id)
        
        assert retrieved.id == created.id
        assert retrieved.content == "Test"
    
    def test_update_annotation(self, db, user, polygon):
        """Test actualizar anotacion"""
        annotation = AnnotationService.create_annotation(
            db=db,
            polygon_id=polygon.id,
            author_id=user.id,
            content="Original",
            annotation_type="comment"
        )
        
        updated = AnnotationService.update_annotation(
            db=db,
            annotation_id=annotation.id,
            content="Modificado"
        )
        
        assert updated.content == "Modificado"
    
    def test_annotation_types(self, db, user, polygon):
        """Test todos los tipos de anotacion"""
        types = ["comment", "flag", "suggestion", "issue"]
        
        for atype in types:
            annotation = AnnotationService.create_annotation(
                db, polygon.id, user.id, f"Test {atype}", atype
            )
            assert annotation.annotation_type == atype
