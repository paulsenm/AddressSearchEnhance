from addr_search import get_lat_lon
from juris_check import is_within_city_limits, get_location_name
from soap_requests import request_juris

from classes.address import AddressPoint

CITY_STRING = "City"
COUNTY_STRING = "County"



def create_address(address_string:str):
    [lat, lon] = get_lat_lon(address_string)
    in_city_limits = is_within_city_limits(lat, lon)
    location_name = get_location_name(lat, lon, in_city_limits)

    the_address = AddressPoint(
        address_string=address_string,
        latlon = [lat, lon],
        in_city_limits = in_city_limits,
        location_name= location_name
        )
    
    return the_address
    
def get_juris_permit_type_blocks(address:AddressPoint):
    city_or_county = ''
    if address.in_city_limits == True:
        city_or_county = CITY_STRING
    else:
        city_or_county = COUNTY_STRING
    
    return request_juris(address.location_name, city_or_county)
