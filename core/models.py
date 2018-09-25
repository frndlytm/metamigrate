import pandas as pd

from typing import List
from jinja2 import Environment
from core.builders import TableBuilder


class Model:
    """Model houses the INFORMATION_SCHEMA-style metadata for the data 
    model, a TableBuilder which consumes metadata for a Table and yields
    a Table object from prototype, and a template Environment for turning
    commands into valid flavor-code.
    """
    def __init__(self, info: pd.DataFrame, tablebuilder: TableBuilder, templates: Environment) -> None:
        self.info = info
        self.tablebuilder = tablebuilder
        self.templates = templates

    @property
    def schemas(self) -> list:
        """schemas exposes the distinct schema names in the model from
        the metadata for convenience
        """
        return pd.unique(self.info.get('TABLE_SCHEMA'))

    @property
    def tables(self) -> List(Table):
        """tables exposes the tables as a convenience attribute. It
        relies on the tablebuilder to ensure they are Table objects.
        """
        tables = pd.unique(self.info.get('TABLE_NAME'))
        
        
    @property   
    def columns(self) -> List(Field):
        """
        """
        pass



class Table:
    def __init__(self, fields=[], constraints={}):
        self.fields = fields

    def add_field(self, field):
        self.fields.append(field)


class Field:
    """Field is an holder for 
    """
    def __init__(self, position, name, dtype, nullable, default) -> None:
        self.position = position
        self.name = name
        self.dtype = dtype
        self.nullable = self._convert_nullable(nullable)
        self.default = default

    def __lt__(self, other):
        return self.position < other.position

    def expose(self) -> dict:
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

    
            