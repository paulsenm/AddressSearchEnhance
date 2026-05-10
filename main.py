from addr_search import get_lat_lon
from juris_check import load_city_polys, get_cities, is_within_city_limits, is_within_county_limits
from soap_requests import request_city, get_juris_contact

def main():
    print("main")
    addr_str = input("Enter the address: ")
    lat_lon = get_lat_lon(addr_str)
    city_limits_obj = is_within_city_limits(lat_lon[0], lat_lon[1])
    county_limits_obj = is_within_county_limits(lat_lon[0], lat_lon[1])
    #find_point_container(44.123, -123.123)
    if city_limits_obj['in_city_limits'] == True:
        city_name = city_limits_obj['city']
        juris_obj = request_city(city_name)
        contact_objects = get_juris_contact(city_name)
        print(f'addr was within {juris_obj}')
        print(f'contact blob: {contact_objects}')
    


if __name__ == "__main__":
    main()