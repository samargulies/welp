from django.contrib.gis.geos import Polygon, Point
import mercantile
import mapbox_vector_tile
from .models import Place

SRID_LNGLAT = 4326
SRID_SPHERICAL_MERCATOR = 3857  

def point_in_tile(tile_bounds, point):
    # `mapbox-vector-tile` has a hardcoded tile extent of 4096 units.
    MVT_EXTENT = 4096

    # We need tile bounds in spherical mercator
    assert tile_bounds.srid == SRID_SPHERICAL_MERCATOR

    # And we need the line to be in a known projection so we can re-project
    assert point.srid is not None
    point.transform(SRID_SPHERICAL_MERCATOR)

    (x0, y0, x_max, y_max) = tile_bounds.extent
    x_span = x_max - x0
    y_span = y_max - y0

    return Point(int((point.x - x0) * MVT_EXTENT / x_span),
            int((point.y - y0) * MVT_EXTENT / y_span))

# encode places to mpt with the given properties
def encode(places, tile_bounds):
    features = []
    buildings = []
    for place in places:
        # only add each building to the map once
        if place.building:
            if place.building not in buildings:
                buildings.append(place.building)
            else:
                continue
            
        feature_point = point_in_tile(tile_bounds, place.location)
        features.append({
            "geometry": feature_point.wkt,
            "properties": place.map_properties()
        })
    
    return mapbox_vector_tile.encode({
        "name": "places",
        "features": features
    }, round_fn=round)
    
# return results for a given tile query
def encode_objects_for_tile(xyz):
    tile_bounds = Polygon.from_bbox(mercantile.bounds(*xyz))
    tile_bounds.srid = SRID_LNGLAT
    tile_bounds.transform(SRID_SPHERICAL_MERCATOR)
    
    objects = Place.objects.filter(location__intersects=tile_bounds).select_related('building').all()[:20]
    
    return encode(objects, tile_bounds)