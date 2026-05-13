from dataclasses import dataclass

from classes.juris_info import JurisInfo

@dataclass
class Contact:
    juris_block: JurisInfo
    contact_info: str
    is_on_epermitting: bool = False

    def __str__(self):
        return f'contact info was {self.contact_info}'