def get_table_names(connection):
    """Returns a list consisting of all the tables in the database

    Parameters
    ----------
    connection:
        A connection to the database created using the SQLAlchemy library

    Returns
    -------
    lisr:
        A lisr of all the table names in the databse

    Example
    -------
    >>> get_table_names(connection)
    ["customers", "order_items"]

    """

    tables = connection.execute("SHOW TABLES")
    tables = tables.fetchall()
    tables = [table[0] for table in tables]
    return tables


def get_table_structures(tables: list, connection) -> dict:
    """Returns a dictionary consisting of the structure of all the tables in the database

    Parameters
    ----------
    tables:
        A list/tuple of all the table names

    connection:
        A connection to the database created using the SQLAlchemy library

    Returns
    -------
    dict:
        A dictionary of table names as the keys and a list/tuple of column names
        that are there in the table as the values.

    Example
    -------
    >>> get_table_structures(["customers", "order_items"], connection)
    {
        "customers": ["customer_id", "first_name", "last_name"], 
        "order_items": ["order_id", "product_id", "quantity", "unit_price"]
    }

    """

    table_structures = {}

    for table in tables:
        table_structure = connection.execute(f"DESCRIBE {table}")
        table_structure = table_structure.fetchall()

        table_columns = []
        for col in table_structure:
            table_columns.append(col[0])
        table_structures[table] = table_columns

    return table_structures
