import pandas as pd

class Loader:
    def load(self, source, target) -> pd.DataFrame:
        raise NotImplementedError

class DatabaseLoader(Loader):
    """DatabaseLoader assumes the source is a valid
    SQL database (engine) with a _model table at its 
    target (schema).
    """
    def load(self, source, target):
        query = f'select * from {target}._model'
        info = pd.read_sql(query, source)
        return info

class CSVLoader(Loader):
    pass
