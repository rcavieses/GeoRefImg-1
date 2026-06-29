import pytest
from app.services.drawing_service import DrawingService
from app.utils.exceptions import ValidationException

class TestDrawingService:
    
    def test_geojson_to_wkt(self):
        """Test convertir GeoJSON a WKT"""
        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
                ]
            }
        }
        
        wkt_result = DrawingService.geojson_to_wkt(geojson)
        assert "POLYGON" in wkt_result
    
    def test_wkt_to_geojson(self):
        """Test convertir WKT a GeoJSON"""
        wkt_geom = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        
        geojson = DrawingService.wkt_to_geojson(wkt_geom)
        
        assert geojson["type"] == "Feature"
        assert geojson["geometry"]["type"] == "Polygon"
    
    def test_coordinates_to_wkt(self):
        """Test convertir coordenadas a WKT"""
        coords = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
        
        wkt_result = DrawingService.coordinates_to_wkt(coords)
        
        assert "POLYGON" in wkt_result
    
    def test_validate_drawn_polygon_valid(self):
        """Test validar poligono valido"""
        coords = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
        
        is_valid, msg = DrawingService.validate_drawn_polygon(coords)
        
        assert is_valid is True
    
    def test_validate_drawn_polygon_insufficient_points(self):
        """Test validar con puntos insuficientes"""
        coords = [[0, 0], [1, 0]]
        
        is_valid, msg = DrawingService.validate_drawn_polygon(coords)
        
        assert is_valid is False
    
    def test_get_polygon_vertices(self):
        """Test obtener vertices de poligono"""
        wkt_geom = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        
        vertices = DrawingService.get_polygon_vertices(wkt_geom)
        
        assert len(vertices) == 5
    
    def test_calculate_polygon_stats(self):
        """Test calcular estadisticas"""
        wkt_geom = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        
        stats = DrawingService.calculate_polygon_stats(wkt_geom)
        
        assert "area" in stats
        assert "perimeter" in stats
        assert "num_vertices" in stats
        assert stats["num_vertices"] == 4
    
    def test_buffer_polygon(self):
        """Test expandir poligono"""
        wkt_geom = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        
        buffered = DrawingService.buffer_polygon(wkt_geom, 0.1)
        
        assert "POLYGON" in buffered
    
    def test_simplify_polygon(self):
        """Test simplificar poligono"""
        wkt_geom = "POLYGON((0 0, 0.5 0, 1 0, 1 0.5, 1 1, 0.5 1, 0 1, 0 0.5, 0 0))"
        
        simplified = DrawingService.simplify_polygon(wkt_geom)
        
        assert "POLYGON" in simplified
    
    def test_merge_polygons(self):
        """Test fusionar poligonos"""
        wkt1 = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        wkt2 = "POLYGON((1 0, 2 0, 2 1, 1 1, 1 0))"
        
        merged = DrawingService.merge_polygons([wkt1, wkt2])
        
        assert merged is not None
        assert "POLYGON" in merged or "MULTI" in merged
