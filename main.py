"""
@author: frndlytm
@name: metamigrate.main
@description:
    Testing the API.
"""
from managers import ModelManager
from models import ModelFactory
from fields import FieldFactory

class Main:
    def __init__(self, config):
        self.manager = ModelManager(
            config.flavor,
            config.server,
            config.database,
            config.driver,
            config.port,
            config.schema
        )
        self.factory = ModelFactory(
            config.environment,
            config.flavor,
            FieldFactory()
        )


    def __call__(self):
        # Connect to the server and query model metadata
        with self.manager as meta:
            tables = meta.tables()
            columns = [meta.columns(table=table[3]) for table in tables]

        # Zip the serialized values together
        zipped = zip(tables, columns)

        # Map the Model.__repr__ onto the zipped records.
        results = map(
            lambda x: str(self.factory.make(x[0][1], x[0][2], x[0][3], fields=x[1])),
            zipped
        )

        # Send the table creation back to the server.
        for result in results:
            print(result)


if __name__ == '__main__':
    from settings import config
    main = Main(config)
    main()



