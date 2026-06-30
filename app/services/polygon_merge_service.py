import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union
from app.utils.logger import logger
from app.utils.exceptions import ValidationException

class PolygonMergeService:
    """Servicio para fusionar polígonos"""

    @staticmethod
    def merge_polygons(gdf: gpd.GeoDataFrame, polygon_ids: list, new_name: str = None) -> dict:
        """
        Fusiona múltiples polígonos en uno

        Args:
            gdf: GeoDataFrame con los polígonos
            polygon_ids: Lista de IDs de polígonos a fusionar
            new_name: Nombre para el polígono fusionado

        Returns:
            dict con geometría fusionada y propiedades

        Raises:
            ValidationException si hay menos de 2 polígonos o IDs inválidos
        """
        if len(polygon_ids) < 2:
            raise ValidationException("Se requieren al menos 2 polígonos para fusionar")

        try:
            # Obtener polígonos seleccionados
            selected_polys = []
            for pid in polygon_ids:
                if pid < 0 or pid >= len(gdf):
                    raise ValidationException(f"ID de polígono inválido: {pid}")
                selected_polys.append(gdf.iloc[pid])

            # Unir geometrías
            geometries = [poly.geometry for poly in selected_polys]
            merged_geom = unary_union(geometries)

            # Combinar propiedades
            merged_props = {}
            first_props = selected_polys[0].drop('geometry').to_dict()

            for key in first_props:
                values = [poly[key] for poly in selected_polys if key in poly.index and poly[key] is not None]
                if values:
                    # Para campos numéricos, sumar; para strings, concatenar
                    if isinstance(values[0], (int, float)):
                        merged_props[key] = sum(v for v in values if isinstance(v, (int, float)))
                    else:
                        merged_props[key] = " | ".join(str(v) for v in values)
                else:
                    merged_props[key] = None

            # Sobrescribir nombre si se proporciona
            if new_name:
                merged_props['Name'] = new_name

            result = {
                "geometry": merged_geom,
                "properties": merged_props,
                "source_polygons": polygon_ids,
                "polygon_count": len(polygon_ids)
            }

            logger.info(f"Fusionados {len(polygon_ids)} polígonos: {polygon_ids}")
            return result

        except ValidationException:
            raise
        except Exception as e:
            raise ValidationException(f"Error fusionando polígonos: {str(e)}")

    @staticmethod
    def split_polygon(geometry, split_line) -> list:
        """
        Divide un polígono por una línea

        Args:
            geometry: Geometría del polígono
            split_line: LineString para dividir

        Returns:
            list con geometrías resultantes
        """
        try:
            from shapely.ops import split
            split_polygons = list(split(geometry, split_line).geoms)
            logger.info(f"Polígono dividido en {len(split_polygons)} partes")
            return split_polygons
        except Exception as e:
            raise ValidationException(f"Error dividiendo polígono: {str(e)}")

    @staticmethod
    def simplify_polygon(geometry, tolerance: float = 0.001) -> Polygon:
        """
        Simplifica un polígono reduciendo vértices

        Args:
            geometry: Geometría a simplificar
            tolerance: Tolerancia de simplificación

        Returns:
            Geometría simplificada
        """
        try:
            simplified = geometry.simplify(tolerance)
            logger.info(f"Polígono simplificado: {len(geometry.exterior.coords)} -> {len(simplified.exterior.coords)} vértices")
            return simplified
        except Exception as e:
            raise ValidationException(f"Error simplificando polígono: {str(e)}")

    @staticmethod
    def buffer_polygon(geometry, distance: float) -> Polygon:
        """
        Crea un buffer alrededor de un polígono

        Args:
            geometry: Geometría original
            distance: Distancia del buffer

        Returns:
            Polígono con buffer aplicado
        """
        try:
            buffered = geometry.buffer(distance)
            logger.info(f"Buffer aplicado: {distance} unidades")
            return buffered
        except Exception as e:
            raise ValidationException(f"Error aplicando buffer: {str(e)}")
