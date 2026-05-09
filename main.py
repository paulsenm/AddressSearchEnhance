from addr_search import get_lat_lon
from juris_check import load_city_polys, get_cities, is_within_city_limmits

def main():
    print("main")
    addr_str = input("Enter the address: ")
    lat_lon = get_lat_lon(addr_str)
    is_within_city_limmits(lat_lon[0], lat_lon[1])
    #find_point_container(44.123, -123.123)


if __name__ == "__main__":
    main()