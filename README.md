# metamigrate
Generating database migrations using Jinja2 templates.

Inspired by Django makemigrations, this repository is meant to capture the same functionality without requiring a
Django (or other Python MVC framework) implementation for the given system.

This script was developed to translate tabular requirements into a database deployment, allowing end-users to maintain
meta data about the system they're maintaining without needing to write and maintain table creation queries.

The GLOBAL_API for the system migration is as follows:

GLOBAL_API = {
    'inserts': [
        {
            'zone': 'edit',
            'names': 'Mapping_Field_Name',
            'filter': 'Mapping_Field_IsEditable'
        },
        {
            'zone': 'stage',
            'names': 'Mapping_Template_FieldName',
            'filter': None
        }
    ],
    'updates': [
        {
            'zone': 'input',
            'names': 'Mapping_Template_FieldName',
            'filter': 'Mapping_Field_IsInput'
        },
        {
            'zone': 'edit',
            'names': 'Mapping_Field_Name',
            'filter': 'Mapping_Field_IsEditable'
        },
        {
            'zone': 'stage',
            'names': 'Mapping_Template_FieldName',
            'filter': None
        }
    ]
}

This API constructs dropzones for manual database "INSERTS" and "UPDATES" allowing end-users to interact with production 
data systems by removing development time for GUI-based maintenance applications.

It transforms the application into a three-stage MS Access workflow: 
  * an input area for Primary Keys of records that need editing,
  * an edit area containing results for editable fields with user-friendly naming, and
  * a stage area to transform the results back to the original structure for validation.
  
This workflow is generated for various GROUPS of MAPPINGS.

In the case of the project for which it was developed, there were 4 separate mappings into the same generic template files
which were fed to a cloud PaaS.

For more information about the ignored 'settings.py' file, feel free to contact me directly.
