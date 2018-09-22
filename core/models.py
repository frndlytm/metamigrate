from typing import List
from pandas import DataFrame
from jinja2 import Environment
from core.builders import TableBuilder


class Model:
    def __init__(self, info: DataFrame, flavor: str, tablebuilder: TableBuilder, templates: Environment) -> None:
        self.info = info
        self.flavor = flavor
        self.tablebuilder = tablebuilder
        self.templates = templates

    @property
    def schemas(self) -> list:
        pass
    @property
    def tables(self) -> List(Table):
        pass
    @property   
    def columns(self) -> List(Field):
        pass


class Table:
    def __init__(self, fields=[], constraints={}):
        self.fields = fields

    def add_field(self, field):
        self.fields.append(field)


class Field:
    def __init__(self, position, name, dtype, nullable, default) -> None:
        self.position = position
        self.name = name
        self.dtype = dtype
        self.nullable = self._convert_nullable(nullable)
        self.default = default

    def __repr__(self) -> dict:
        return dict(
            position = self.position,
            name = self.name,
            dtype = self.dtype,
            nullable = self.nullable,
            default = self.default
        )

    def _convert_nullable(self, nullable) -> bool:
        if isinstance(nullable, bool): return nullable
        elif nullable == 'YES' or nullable == 1: return True
        elif nullable == 'NO' or nullable == 2: return False
        else: raise ValueError

    
            