from addr_search import get_lat_lon
from juris_check import load_city_polys, get_cities, is_within_city_limits, is_within_county_limits
from soap_requests import request_city, request_county, get_juris_contact

def handle_address(address_string):
    lat_lon = get_lat_lon(address_string)
    city_limits_obj = is_within_city_limits(lat_lon[0], lat_lon[1])
    county_limits_obj = is_within_county_limits(lat_lon[0], lat_lon[1])
    #find_point_container(44.123, -123.123)
    if city_limits_obj['in_city_limits'] == True:
        info_to_return = {}
        city_name = city_limits_obj['city']
        juris_objs = request_city(city_name)
        contact_objects = get_juris_contact(city_name)
        #print(f'addr was within {juris_objs}')
        print(f'contact blob: {contact_objects}')
        info_to_return['city name'] = city_name
        info_to_return['juris objects'] = juris_objs
        info_to_return['contact objects'] = contact_objects
        return info_to_return
    if county_limits_obj['in_county_limits'] == True:
        info_to_return = {}
        county_name = county_limits_obj['county']
        juris_objs = request_county(county_name)
        contact_objects = get_juris_contact(county_name)
        info_to_return['county name'] = county_name
        info_to_return['juris objects'] = juris_objs
        info_to_return['contact objects'] = contact_objects

        county_name = county_limits_obj['county']
        print(f'county was: {county_name}')
        return info_to_return

    


