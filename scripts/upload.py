import sys, os
projects = 'C:\\workspace\\python\\projects\\'
target = os.path.join(projects, 'metamigrate', 'data', 'information_schema.csv')
sys.path.append(projects)



if __name__ == '__main__':
    import pandas
    import sqlalchemy as sql
    from urllib.parse import quote_plus
    from metamigrate.settings import config

    #
    # helper for __str__ to simplify the connection string.
    #
    def params(driver, port, server, database):
        return quote_plus(
            'DRIVER={};PORT={};SERVER={};DATABASE={};Trusted_Connection=yes;'
            .format(driver, port, server, database)
        )

    #
    # connection string
    #
    p = params(config.driver, config.port, config.server, config.database)
    url = '{}+pyodbc:///?odbc_connect={}'.format('mssql', p)


    #
    # database connection and upload
    #
    db = sql.create_engine(url)
    data = pandas.read_csv(target)
    data.to_sql('_Model', db, schema=config.schema, if_exists='replace', index=False)
    db.dispose()