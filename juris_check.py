import json, sys

from math import inf
from shapely.geometry import shape, Point, LineString
from shapely.prepared import prep
from shapely.ops import nearest_points


from pyproj import Geod

CITY_LIMITS_PATH = "City_Limits.geojson"

CITY_FIELD = "CITYNAME"

_CITIES = None



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
        print(json.dump({"error":"No city features found"}), file=sys.stderr)
        sys.exit(2)
    return feats

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
        print(json.dump({"error":"No city features found"}), file=sys.stderr)
        sys.exit(2)
    print(f"A feature: {feats[3]}")


def get_cities():
    global _CITIES
    if _CITIES is None:
        _CITIES = load_city_polys(CITY_LIMITS_PATH)
    return _CITIES

def is_within_city_limmits(lat: float, lon: float):
    cities = get_cities()
    point = Point(lon, lat)
    x = lon
    y = lat

    for feature in cities:
        print(f'city name was: {feature["name"]}')
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
            print(f"The address is within {feature["name"]} city limits")
            return {"in_city_limits": True, "city": feature["name"]}
        continue
    
    # print(f'failed second test with lat: {y}, and lon: {x} for city: {feature["name"]}')
    # print(f'bbox for {feature["name"]} was: {feature["bbox"]}')
    print('Address does not appear to be within any city limits.')

    return {"in_city_limits": False, "city": None}
    

