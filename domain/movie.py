import uuid
from dataclasses import dataclass, field
from typing import Optional
MAX_TITLE = 255
@dataclass

class Movie:
    """Entidade Movie simples; relaciona com Category via category_id."""
    title: str
    year: int
    category_id: str
    description: str = ""
    is_active: bool = True
    id: Optional[str] = field(default=None)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        self.title = self._validate_title(self.title)
        self.year = self._validate_year(self.year)
        self.description = self.description or ""
        self.is_active = bool(self.is_active)

    @staticmethod
    def _validate_title(title: str) -> str:
        if not isinstance(title, str):
            raise TypeError("title deve ser string")
        t = title.strip()
        if not t:
            raise ValueError("title é obrigatório")
        if len(t) > MAX_TITLE:
            raise ValueError(f"title deve ter no máximo {MAX_TITLE} caracteres")
        return t
    
    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int):
            raise TypeError("year deve ser int")
        if year < 1880 or year > 2100:
            raise ValueError("year fora do intervalo razoável (1880..2100)")
        return year
    
    def update(
        self, *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        year: Optional[int] = None,
        category_id: Optional[str] = None
        ):
        if title is not None:
            self.title = self._validate_title(title)
        if description is not None:
            self.description = description
        if year is not None:
            self.year = self._validate_year(year)
        if category_id is not None:
            self.category_id = category_id
    
    def activate(self): self.is_active = True
    
    def deactivate(self): self.is_active = False
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) | cat={self.category_id}({self.is_active})"
    
    def __repr__(self) -> str:
        return f"<Movie {self.title} ({self.id})>"