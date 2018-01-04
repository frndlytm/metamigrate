"""
@name : metamigrate.migrate
@author : frndlytm@gmail.com

@description:
    Serializes meta data to prepare queries
    and initialize multi-phase database systems
    using a Jinja2 back-end.
"""
import os
import pyodbc as db
import pandas as pd
import settings


class Meta:
    """
    A container for our connection information and for
    selecting all data from a table.
    """
    def __init__(self, server, database, driver):
        """
        Establish the connection data.
        """
        self.server = server
        self.database = database
        self.driver = driver


    def __enter__(self):
        """
        Connect to the database for querying.
        """
        self.conn = db.connect(
            r'DRIVER='+self.driver+ \
            r'PORT=1433;'+ \
            r'SERVER='+self.server+ \
            r'DATABASE='+self.database+ \
            r'Trusted_Connection=yes;'
        )
        return self


    def __exit__(self, *args):
        """
        Disconnect on wrap-up.
        """
        self.conn.close()


    def select_all(self, table):
        """
        Select all data from a table on the connection.
        """
        query = "select * from {0}".format(table)
        data = pd.read_sql(query, self.conn)
        return data



def get_send(fields, group, item):
    """
    get_send returns the Send repr.
    """
    #
    # Make the table name using
    # the group and the item.
    #
    tablename = (
        group['Template_Dropzone']+'_'
        +item['zone']+'_'
        +group['Template_Name']+'_'
        +group['Template_FieldGroup']
    )

    #
    # Get the constraint.
    #
    constraint = item['filter']

    #
    # Build the mapping for the template.
    #
    # This block of code is a nightmare.
    # Need to re-design using clean DataFrame join logic:
    #   fields, groups, and item
    #
    fieldlist = pd.DataFrame()
    fieldlist['index'] = fields['Mapping_Template_FieldIndex']
    fieldlist['name'] = fields[item['names']]
    fieldlist['template'] = fields['Mapping_Template_ID']
    fieldlist['process'] = group['Template_Dropzone']
    fieldlist['group'] = group['Template_FieldGroup']
    fieldlist['zone'] = item['zone']
    fieldlist['file'] = group['Template_Name']
    fieldlist['dtype'] = fields['Mapping_Field_DataType']
    fieldlist['default'] = fields['Mapping_Field_Default']
    fieldlist['required'] = fields['Mapping_Field_IsRequired']
    #
    # If there's a constraint, get it,
    # else leave it true.
    #
    if constraint:
        fieldlist['constraint'] = fields[constraint]
    else:
        fieldlist['constraint'] = True


    #
    # RETURN the send.
    #
    return dict(
        tablename=tablename,
        fieldlist=(
            fieldlist[
                (fieldlist['constraint'])
                & (fieldlist['name'].notnull())
                & (fieldlist['template'] == group['Template_ID'])
            ].sort_values('index')
            .to_dict(orient='records'))
        )




def main():
    """
    A template generator for manual process creation in
    the schema.
    """
    #
    # Using ContextManager syntax, connect
    # to the database. This is cleaner than
    # doing open/close in main every time.
    #
    with Meta(settings.SERVER, settings.DATABASE, settings.DRIVER) as source:
        """
        groups contains the table naming API meta data.

            [Template_ID] is referenced by [Mapping_Template_ID].
            [Template_Name] is the ODI file name.
            [Template_FieldGroup] is the process we're maintaining.
            [Template_Dropzone] is 'inserts' or 'updates'.

        Table naming convention is, per the tablename.j2 template:
            SchemaName.{{dropzone}}_['input', 'edit', 'stage']_{{name}}_{{fieldgroup}}

        """
        groups = source.select_all(settings.GROUPS).to_dict(orient='records')


        """
        fieldlist contains ODI API for field mapping meta data.

            [Mapping_ID] is the table row identifier.
            [Mapping_Template_ID] is the FK to groups.
            [Mapping_Template_FieldIndex] is the column number.
            [Mapping_Template_FieldName] is the ODI field name.
            [Mapping_Field_Name] is the Granite field name.
            [Mapping_Field_DataType] is the SQL type for the Field.
            [Mapping_Field_Default] is the DEFAULT value CONSTRAINT.
            [Mapping_Field_IsPrimaryKey] indicates a field is in the PK.
            [Mapping_Field_IsRequired] indcates a field is required in the feed.
            [Mapping_Field_IsInput] indicates a field should be in the 'input' zone.
            [Mapping_Field_IsEditable] indicates a field should be in the 'edit' zone.

        """
        fields = source.select_all(settings.MAPPINGS)

        print(groups)
        for group in groups:
            for item in settings.GLOBAL_API[group['Template_Dropzone']]:
                send = get_send(fields, group, item)

                #
                # If there are some fields,
                # do the thing.
                #
                if send['fieldlist']:
                    #
                    # data maps the two querysets down to
                    # our rendered variables in our templates.
                    #
                    print(send['tablename'])
                    query = settings.MYENV.get_template('fields.j2').render(send)

                    #
                    # Print out the queries to .sql files
                    # in the queries directory
                    #
                    landing = os.path.join(settings.ROOT, 'queries', send['tablename']+'.sql')
                    with open(landing, 'w') as file:
                        file.write(query)

                    #
                    # Commit the creation
                    #
                    curs = source.conn.cursor()
                    curs.execute(query)
                    curs.commit()

                #
                # Else, do the next thing.
                #
                else:
                    continue





if __name__ == '__main__':
    main()
