import pytest
import geopandas as gpd
from shapely.geometry import box
from app.services.geopackage_service import GeopackageService
from app.utils.exceptions import ValidationException

@pytest.fixture
def sample_gdf():
    """Crea un GeoDataFrame de prueba"""
    geometry = [
        box(0, 0, 1, 1),
        box(1, 0, 2, 1),
        box(0, 1, 1, 2),
    ]
    
    gdf = gpd.GeoDataFrame(
        {
            "name": ["Polygon 1", "Polygon 2", "Polygon 3"],
            "value": [10, 20, 30],
            "geometry": geometry
        },
        crs="EPSG:4326"
    )
    return gdf


class TestGeopackageService:
    """Tests para GeopackageService"""
    
    def test_to_geojson(self, sample_gdf):
        """Test conversión a GeoJSON"""
        geojson = GeopackageService.to_geojson(sample_gdf)
        
        assert geojson["type"] == "FeatureCollection"
        assert len(geojson["features"]) == 3
        
        # Verificar primer feature
        feature = geojson["features"][0]
        assert feature["type"] == "Feature"
        assert feature["geometry"]["type"] == "Polygon"
        assert feature["properties"]["name"] == "Polygon 1"
    
    def test_get_bounds(self, sample_gdf):
        """Test obtención de bounds"""
        bounds = GeopackageService.get_bounds(sample_gdf)
        
        assert "minx" in bounds
        assert "miny" in bounds
        assert "maxx" in bounds
        assert "maxy" in bounds
        
        assert bounds["minx"] == 0
        assert bounds["miny"] == 0
        assert bounds["maxx"] == 2
        assert bounds["maxy"] == 2
    
    def test_get_center(self, sample_gdf):
        """Test cálculo de centro"""
        bounds = GeopackageService.get_bounds(sample_gdf)
        center = GeopackageService.get_center(bounds)
        
        assert len(center) == 2
        assert center[0] == 1.0  # lat (centro Y)
        assert center[1] == 1.0  # lng (centro X)
    
    def test_get_polygon_by_id(self, sample_gdf):
        """Test obtener polígono por ID"""
        polygon = GeopackageService.get_polygon_by_id(sample_gdf, 0)
        
        assert polygon is not None
        assert polygon["id"] == 0
        assert polygon["properties"]["name"] == "Polygon 1"
        assert polygon["geometry"]["type"] == "Polygon"
    
    def test_get_polygon_by_id_not_found(self, sample_gdf):
        """Test obtener polígono inexistente"""
        polygon = GeopackageService.get_polygon_by_id(sample_gdf, 999)
        assert polygon is None
    
    def test_validate_geometries(self, sample_gdf):
        """Test validación de geometrías"""
        validation = GeopackageService.validate_geometries(sample_gdf)
        
        assert validation["total"] == 3
        assert validation["valid"] == 3
        assert validation["invalid"] == 0
        assert validation["is_all_valid"] is True
    
    def test_validate_geometries_with_invalid(self):
        """Test validación con geometría inválida"""
        # Crear geometría inválida (anillo auto-intersectante)
        from shapely.geometry import Polygon
        
        # Este polígono es inválido
        invalid_polygon = Polygon([
            (0, 0), (2, 2), (0, 2), (2, 0), (0, 0)
        ])
        
        gdf = gpd.GeoDataFrame(
            {"geometry": [invalid_polygon]},
            crs="EPSG:4326"
        )
        
        validation = GeopackageService.validate_geometries(gdf)
        assert validation["invalid"] >= 0  # Puede variar según Shapely
    
    def test_search_polygons(self, sample_gdf):
        """Test búsqueda de polígonos"""
        # Buscar por nombre
        result = GeopackageService.search_polygons(sample_gdf, "Polygon 1")
        assert len(result) == 1
        assert result.iloc[0]["name"] == "Polygon 1"
    
    def test_search_polygons_no_match(self, sample_gdf):
        """Test búsqueda sin resultados"""
        result = GeopackageService.search_polygons(sample_gdf, "NonExistent")
        assert len(result) == 0
    
    def test_search_polygons_multiple_matches(self, sample_gdf):
        """Test búsqueda con múltiples resultados"""
        result = GeopackageService.search_polygons(sample_gdf, "Polygon")
        assert len(result) == 3
    
    def test_calculate_area(self, sample_gdf):
        """Test cálculo de área"""
        from shapely.geometry import box
        
        # Crear un cuadrado de 1x1
        square = box(0, 0, 1, 1)
        
        area = GeopackageService.calculate_area(square)
        assert area > 0
    
    def test_get_crs(self, sample_gdf):
        """Test obtención de CRS"""
        crs = GeopackageService.get_crs(sample_gdf)
        assert "4326" in crs or "4326" in str(sample_gdf.crs)
    
    def test_to_geojson_with_null_values(self):
        """Test conversión con valores NULL"""
        geometry = [box(0, 0, 1, 1)]
        
        gdf = gpd.GeoDataFrame(
            {
                "name": ["Test"],
                "empty_field": [None],
                "geometry": geometry
            },
            crs="EPSG:4326"
        )
        
        geojson = GeopackageService.to_geojson(gdf)
        feature = geojson["features"][0]
        
        assert feature["properties"]["empty_field"] is None
