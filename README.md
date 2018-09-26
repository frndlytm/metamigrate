# MetaMigrate

A WYSIWYG database migration management tool in pure Python.

## Overview

MetaMigrate was inspired by django-admin as a way to manage metadata and automate model maintenance processes in its own framework. Django, as a full-featured MVC Framework, enables database development and ORM querying in pure Python; however, I found it lacking coming from a SQL-first modeling experience. Many of my use cases are in rapid model development on persistent data sets or in prototyping data models. I am not an application developer by nature, and while Django managed model redeployment on existing/tracked meta data in pure Python files, it felt too robust and manual for prototyping with managed metadata. To that end, I initially developed a tool which populated SQL templates to generate CREATE TABLE statments, similar to a SQL-like engine in Django. The project has since grown to require a more robust command pallette, and it has necessitated a near-complete re-design.

## Intent

The mission of this project is to provide a clean command-line interface (CLI) to manage structured data models purely from tabular metadata. The project should provide clean access to multiple source types, like CSV or SQL, and translate the model into various SQL-like flavors, like Impala, MSSQL, and even Django. Using the tool should be as simple as the following code for targeting a schema-level, or current directory migration respectively:

```sh
python metamigrate create --schema=MySchema
python metamigrate backup --dir
```

It should also support macros which chain together multiple commands, or shell scripting as a way to enable OS-level interaction with the migration API. Keeping the intent in mind will be important as the project grows, but for now, I expect to support SQL-to-SQL migrations and feature requests for automating all aspects of a model's lifecycle, from creation to code generation further into code re-writingsince these are the use cases most applicable to my work-load.

## Model

The project is structured similarly to other frameworks I've come across thus far: a `root` directory with configuration and a `core` directory with the essential features of the project. Inside `core` there are a series of files split primarily by design patterns used. I will present them in the order I deem most important.

### Commands

Commands are the back-bone of this project. Commands essentially define the types of migration requests that are accessible to the CLI. A basic Command describes a simple interaction with a model, like creation or deletion; however, a MacroCommand should enable the execution of a string of Commands, for example a reployment command might issue the series [Backup, Delete, Create, Restore] in order.

### Loaders

Loaders decouple the querying process which constructs an INFORMATION_SCHEMA-like view for the Model to manage, from the Model itself. Currently, only a DatabaseLoader exists, but the next simplest Model loader will be from CSV.

### Models

Models contains the actually Model class which maintains the metadata for the model and accessors, but also the core components of the model: Tables and Fields. This part of the project is most up in the air, as the TableBuilder can be decoupled from the Model in the near future; however, I would like to develop the core functionality for how a Command is called before I focus further on building the concrete components. In short though, the accessors should provide sufficient access to unpacking Table and Field metadata.

### Factories

Factories builds a model from a loader and a flavor. This can be handled with configuration in the `main` script.

### Builders

Builders construct Tables and Fields from tuples.

## Conclusion

Stay tuned for more updates on this project as it develops and achieves a stable state.