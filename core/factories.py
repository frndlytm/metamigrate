import os
from jinja2 import Environment, FileSystemLoader
from core.models import Model
from core.builders import TableBuilder

class ModelFactory:
    """ModelFactories use their loader to construct
    an information_schema-like DataFrame from a source.

    The most common ModelFactory will have mssql-flavor,
    and load from either Database or CSV. 
    """
    def __init__(self, flavor, loader):
        self.flavor = flavor
        self.loader = loader

    def make_model(self, source):
        """make_model is the Factory method. It builds
        info from source using the loader, and packages
        a template Environment from the file-system using
        the flavor.
        """
        info = self.loader.load(source)
        path = self._get_template_path()
        environ = Environment(
            loader=FileSystemLoader(path)
        )
        return Model(info, TableBuilder(), environ)

    def _get_template_path(self):
        """_get_template_path uses the location of this
        file to find the template directory for the chosen
        flavor of model.
        """
        # path to this file.
        path = os.path.dirname(
            os.path.abspath(__file__)
        )

        # join templates and flavor for model.
        path = os.path.join(
            path, 'templates', self.flavor
        )
        return path