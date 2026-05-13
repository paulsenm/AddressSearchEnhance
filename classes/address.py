from dataclasses import dataclass

@dataclass
class AddressPoint:
        address_string: str
        latlon : list[float]
        in_city_limits : bool
        location_name: str

        def __Str__(self):
                return f'address string was: {self.address_string}'