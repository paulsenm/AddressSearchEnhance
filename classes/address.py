from dataclasses import dataclass

@dataclass
class Address:
        address_string: str
        latlon = list[float] | None
        in_city_limits = bool | False
        location_name: str

    