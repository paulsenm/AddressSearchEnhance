import json, sys

from math import inf
from shapely.geometry import shape, Point, LineString
from shapely.prepared import prep
from shapely.ops import nearest_points


from pyproj import Geod

CITY_LIMITS_PATH = "City_Limits.geojson"
COUNTY_LIMITS_PATH = "County_Limits.geojson"

CITY_FIELD = "CITYNAME"
COUNTY_FIELD = "COUNTY_NAME"

_CITIES = None
_COUNTIES = None


def load_city_polys(path):
    try:
        data = json.load(open(path, "r", encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error":f"Failed to read {path}: {e}"}), file=sys.stderr)
        sys.exit(2)

    feats = []
    for feature in data.get("features", []):
        geom = feature.get("geometry")
        if not geom:
            continue
        city_shape = shape(geom)
        if city_shape.is_empty:
            continue

        name = str(feature.get("properties", {}).get(CITY_FIELD) or "")
        feats.append({"name":name, "geom":city_shape, "bbox":city_shape.bounds, "prep": prep(city_shape)})
    if not feats:
        print(json.dumps({"error":"No city features found"}), file=sys.stderr)
        sys.exit(2)
    return feats

def load_county_polys(path):
    try:
        data = json.load(open(path, 'r', encoding='utf-8'))
    except Exception as e:
        print(json.dumps({"Error":f"failed to read {path}: {e}"}), file=sys.stderr)
        sys.exit(2)
    
    features = []
    for feature in data.get('features', []):
        geometry = feature.get('geometry')
        if not geometry:
            continue
        county_shape = shape(geometry)
        if county_shape.is_empty:
            continue

        name = str(feature.get('properties', {}).get(COUNTY_FIELD) or "")
        features.append({'name':name, 'geom':county_shape, 'bbox':county_shape.bounds, prep:prep(county_shape)})
    if not features:
        print(json.dumps({"error":"No county features found"}), file=sys.stderr)
        sys.exit(2)
    
    return features


def city_test(path):
    try:
        data = json.load(open(path, "r", encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error":f"Failed to read {path}: {e}"}), file=sys.stderr)
        sys.exit(2)

    feats = []
    for feature in data.get("features", []):
        geom = feature.get("geometry")
        if not geom:
            continue
        g = shape(geom)
        if g.is_empty:
            continue

        name = str(feature.get("properties", {}).get(CITY_FIELD) or "")
        feats.append({"name":name, "geom":g, "bbox":g.bounds, "prep": prep(g)})
    if not feats:
        print(json.dumps({"error":"No city features found"}), file=sys.stderr)
        sys.exit(2)
    print(f'A feature: {feats[3]}')


def get_cities():
    global _CITIES
    if _CITIES is None:
        _CITIES = load_city_polys(CITY_LIMITS_PATH)
    return _CITIES

def get_counties():
    global _COUNTIES
    if _COUNTIES is None:
        _COUNTIES = load_county_polys(COUNTY_LIMITS_PATH)
    return _COUNTIES




def is_within_city_limits(lat: float, lon: float):
    cities = get_cities()
    point = Point(lon, lat)
    x = lon
    y = lat

    for feature in cities:
        #print(f'city name was: {feature["name"]}')
        min_x, min_y, max_x, max_y = feature["bbox"]
        if x < min_x:
            #print(f"The min x for {f["name"]} was: {min_x}")
            continue
        if y < min_y:
            #print(f"The min x for {f["name"]} was: {min_y}")
            continue
        if x > max_x:
            #print(f"The min x for {f["name"]} was: {max_x}")
            continue
        if y > max_y:
            #print(f"The min x for {f["name"]} was: {max_y}")
            continue                

        if feature["geom"].covers(point):
            print(f'The address is within {feature["name"]} city limits')
            #return {"in_city_limits": True, "city": feature["name"]}
            return True
        continue
    return False

def get_location_name(lat: float, lon: float, is_within_city_limits: bool):
    location_name = ''
    point = Point(lon, lat)
    x = lon
    y = lat
    location_group = None
    if is_within_city_limits:
        location_group = get_cities()
    else:
        location_group = get_counties()
    for feature in location_group:
        if feature['geom'].covers(point):
            location_name = feature['name']

    return location_name


