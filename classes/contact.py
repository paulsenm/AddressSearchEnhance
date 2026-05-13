from dataclasses import dataclass

@dataclass
class Contact:
    contact_info: str
    is_on_epermitting: bool = False