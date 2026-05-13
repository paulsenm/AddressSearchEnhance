from dataclasses import dataclass

@dataclass
class JurisInfo:
    jurisdiction_name: str
    permit_types: list[str]
    
    def __str__(self) -> str:
        return f'juris name was: {self.jurisdiction_name}'