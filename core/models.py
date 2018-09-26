"""
@name: metamigrate.core.models
@auth: frndlytm@github.com
"""
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
    def __init__(
        self, 
        info: pd.DataFrame,         # INFORMATION_SCHEMA
        tablebuilder: TableBuilder, # A way of building
        templates: Environment      # A templating environment
    ) -> None:

        self.info = info
        self.tablebuilder = tablebuilder
        self.templates = templates


    def schemas(self) -> pd.Series:
        """schemas exposes the distinct schema names in the model from
        the metadata for convenience (just in case).
        """
        return pd.unique(self.info.get('TABLE_SCHEMA'))


    def tables(self, schema=None: str) -> List(tuple):
        """tables exposes the tables as a convenience attribute. It
        relies on the tablebuilder to ensure they are Table objects.
        """
        fields = [
            'TABLE_CATALOG',
            'TABLE_SCHEMA',
            'TABLE_NAME'
        ]
        tables = pd.unique(self.info[fields])
        if schema:
            tables = tables.query(f'TABLE_SCHEMA == {schema}')
        return tables.to_records()


    def fields(self, table=None: str) -> List(tuple):
        """columns exposes the fields in the model. To enable filtering
        by table, we need to also expose  
        """
        fields = [
            'ORDINAL_POSITION', 
            'COLUMN_NAME', 
            'DATA_TYPE', 
            'IS_NULLABLE', 
            'COLUMN_DEFAULT'
        ]
        if table:
            fields = (
                self.info.query(f'TABLE_NAME == {table}'))[fields]
            )
        else:
            fields = self.info[fields]
        return fields.fillna(value=False).to_records()

    


class ModelComponent:
    def expose(self) -> dict:
        raise NotImplementedError


class Table(ModelComponent):
    """Table is a holder object containing fields for later rendering.
    Since Table is a ModelComponent, it must expose itself as a dict
    so that the template engine can render it.
    """
    def __init__(
        self, 
        catalog : str,          # database name
        schema  : str,          # schema name
        name    : str,          # table name
        fields  : List(Field),  # Field objects
    ) -> None:

        self.catalog = catalog
        self.schema = schema
        self.name = name
        self.fields = fields

    def expose(self) -> dict:
        """expose releases access to the catalog, schema, and name, as
        well as exposes the fields that have been added to it. 
        """
        fields = map(lambda f: f.expose(), self.fields)
        return dict(
            catalog=self.catalog,
            schema=self.schema,
            name=self.name,
            fields=list(fields)
        )

    def add_field(self, field):
        self.fields.append(field)


class Field(ModelComponent):
    """Field is an holder object for the metadata of a column in a Table.
    A Field is a leaf-level ModelComponent, and only exposes its internals
    as a dictionary.
    """
    def __init__(
        self, 
        position: int,   # column ordering
        name:     str,   # column nam
        dtype:    str,   # flavor-specific data type
        nullable: bool,  # IS NULL or IS NOT NULL
        default:  object # default constraint
    ) -> None:
    
        self.position = position
        self.name = name
        self.dtype = dtype
        self.nullable = self._convert_nullable(nullable)
        self.default = default

    def expose(self) -> dict:
        return dict(
            position = self.position,
            name = self.name,
            dtype = self.dtype,
            nullable = self.nullable,
            default = self.default
        )

    def _convert_nullable(self, nullable) -> bool:
        """_convert_nullable is used during initialization to ensure
        the nullable member is a boolean.
        """
        if isinstance(nullable, bool): return nullable
        elif nullable == 'YES' or nullable == 1: return True
        elif nullable == 'NO' or nullable == 2: return False
        else: raise ValueError

    
            