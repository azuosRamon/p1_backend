import uuid
from dataclasses import dataclass, field
from typing import Optional

MAX_NAME = 255

@dataclass
class Category:

    """
    Entidade Category (sem framework).
    Regras:
    - name obrigatório e <= 255 chars
    - id/description/is_active opcionais
    - is_active default True
    - gera id (uuid4) se não for informado
    - permite update(name/description) e (des)ativar
    """

    name: str
    description: str = ""
    is_active: bool = True
    id: Optional[str] = field(default=None)

    def __post_init__(self):
        # Gera id se não vier um
        if not self.id:
            self.id = str(uuid.uuid4())
        # Valida e normaliza
        self.name = self._validate_name(self.name)
        self.description = self.description or ""
        self.is_active = bool(self.is_active)
    
    # ---- Validação de regras de negócio ----
    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("name deve ser string")
        n = name.strip()
        if not n:
            raise ValueError("name é obrigatório")
        if len(n) > MAX_NAME:
            raise ValueError(f"name deve ter no máximo {MAX_NAME}caracteres")
        return n
    # ---- Comportamentos do domínio ----
    def update(self, *, name: Optional[str] = None, description:
    Optional[str] = None) -> None:
        if name is not None:
            self.name = self._validate_name(name)
        if description is not None:
            self.description = description

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    # Representações úteis para depuração e logs
    def __str__(self) -> str:
        return f"{self.name} | {self.description} ({self.is_active})"
    
    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"