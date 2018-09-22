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
    def tables(self) -> List(tuple):
        pass
    @property   
    def columns(self) -> List(tuple):
        pass

