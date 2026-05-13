from dataclasses import dataclass

from address import Address
from contact import Contact

@dataclass
class JurisInfo:
    address: Address
    permit_types: str
    contact: Contact
    
    