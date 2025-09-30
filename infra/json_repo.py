from __future__ import annotations
import json, os
from typing import Dict, List, TypeVar, Callable

T = TypeVar("T")

class JsonRepo:
    def __init__(self, *, path: str, to_dict: Callable[[T], dict],
    from_dict: Callable[[dict], T]):
        self.path = path
        self.to_dict = to_dict # como serializar o objeto
        self.from_dict = from_dict # como reconstruir o objeto
        self._data: Dict[str, T] = {}
        self._load()
    # ---- Persistência ----
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            self._data = {k: self.from_dict(v) for k, v in raw.items()}
        
    def _save(self):
        raw = {k: self.to_dict(v) for k, v in self._data.items()}
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        
    # ---- CRUD ----
    def add(self, obj: T):
        oid = getattr(obj, 'id')
        if oid in self._data:
            raise ValueError(f"objeto com id {oid} já existe")
        self._data[oid] = obj
        self._save()
        return obj

    def get(self, oid: str) -> T | None:
        return self._data.get(oid)

    def list(self) -> List[T]:
        return list(self._data.values())

    def update(self, obj: T):
        oid = getattr(obj, 'id')
        if oid not in self._data:
            raise KeyError(f"não encontrado: {oid}")
        self._data[oid] = obj
        self._save()
        return obj
    
    def delete(self, oid: str):
        if oid in self._data:
            del self._data[oid]
            self._save()