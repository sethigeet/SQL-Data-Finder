from sqlalchemy import Table
from sqlalchemy.sql.expression import select
from fuzzywuzzy import fuzz, process


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


def get_columns(table_structures: dict) -> list:
    """Returns a list/tuple consisting of all the column names spanning across all the different tables

    Parameters
    ----------
    table_structures:
        A dictionary of table names as the keys and a list/tuple of column names
        that are there in the table as the values.

    Returns
    -------
    list:
        A list of the column names.

    Example
    -------
    >>> get_columns({
            "customers": ["customer_id", "first_name", "last_name"], 
            "order_items": ["order_id", "product_id", "quantity", "unit_price"]
        })
    [
        "customer_id", "first_name", "last_name", "order_id",
        "product_id", "quantity", "unit_price"
    ]

    """

    columns = []

    for column_names in table_structures.values():
        for column_name in column_names:
            columns.append(column_name)

    return list(set(columns))


def find_correct_column_name(search_term: str, columns: list) -> tuple:
    """Finds the completed and correct column name from the given search term

    Parameters
    ----------
    search_term:
        The term that has to be searched for.

    columns:
        A list of the available columns from which the search term has to be searched for

    Returns
    -------
    tuple:
        A tuple of the column name and the score out of 100

    Example
    -------
    >>> find_correct_column_name("customer", [
            "first_name", "state", "unit_price", "quantity", "comments",
            "phone", "last_name", "city", "birth_date", "customer_id"
        ])
    ("customer_id", 84)

    """

    column = process.extractOne(
        search_term, columns, scorer=fuzz.token_set_ratio)
    if column == None:
        raise Exception(f"No column found (Search input given: {search_term})")
    return column


def get_tables_from_column_name(column_name: str, table_structures: dict) -> list:
    """Finds the tables which contain the column name provided from the provided table structure

    Parameters
    ----------
    column_name:
        The term that has to be searched for

    table_structures:
        A dictionary of table names as the keys and a list/tuple of column names
        that are there in the table as the values.

    Returns
    -------
    tuple:
        A tuple of the column name and its score out of 100

    Example
    -------
    >>> get_tables_from_column("customer_id", {
            "customers": ["customer_id", "first_name", "last_name"], 
            "order_items": ["customer_id", "order_id", "product_id", "quantity", "unit_price"]
        })
    ["customers"]

    """

    tables = []
    for table_name in table_structures.keys():
        for column in table_structures[table_name]:
            if column_name == column:
                tables.append(table_name)
    return list(set(tables))


def get_joined_tables(common_column_name: str, req_tables: list, metadata, engine, connection, isouter=False, where={}) -> dict:
    """Returns a dict containing a list of the selected column names and a list of all the results obtained by executing the query to join all the req_tables on the commun_column_name

    Parameters
    ----------
    common_column_name:
        A name of the column that is present in all the req_tables on which the join has to be made

    req_tables:
        A list/tuple of all the required table names that contain the common_column_name

    metadata:
        A metadata to store the tables of the database in memory created using the SQLAlchemy library

    engine:
        An engine containing a connection to the database created using the SQLAlchemy library

    connection:
        A connection to the database created using the SQLAlchemy library

    isouter:
        A boolean value stating whether the join is an inner or outer join

    where:
        A dictionary which contains "column_name": Name of the column and "value": Value of the column 

    Returns
    -------
    dict:
        A dict of all the column names and results obtained

    Example
    -------
    >>> get_joined_tables("customer_id", ["customers", "order_items"], metadata, engine, connection)
    {
        "column_names: [
            "customer_id",
            "order_id",
            "order_date",
            ...
        ]
        "column_data": [
            (9, 10, datetime.date(2017, 7, 5), 2, 'Levy', 'Mynett', datetime.date(1969, 10, 13), '404-246-3370')
            (10, 6, datetime.date(2018, 4, 22), 2, 'Elka', 'Twiddell', datetime.date(1991, 9, 4), '312-480-8498')
        ]
    }

    """

    # Convert string table names to Table objects
    for i, table_name in enumerate(req_tables):
        req_tables[i] = Table(
            table_name, metadata, autoload=True, autoload_with=engine)

    # Join all the tables
    query = None
    for table_index in range(len(req_tables) - 1):
        if not query:
            query = req_tables[table_index].join(
                req_tables[table_index + 1],
                req_tables[table_index].c[common_column_name] ==
                req_tables[table_index + 1].c[common_column_name],
                isouter=isouter
            )
        else:
            query = query.join(
                req_tables[table_index + 1],
                req_tables[table_index].c[common_column_name] ==
                req_tables[table_index + 1].c[common_column_name],
                isouter=isouter
            )
    query = select(req_tables, from_obj=query)

    if where:
        query = query.where(
            req_tables[0].c[where["column_name"]].like(f"%{where['value']}%")
        )

    # Execute the query and fetch the results
    result_proxy = connection.execute(query)
    results = result_proxy.fetchall()

    selected_columns = results[0].keys()

    final_results = {"column_names": selected_columns, "column_data": results}
    return final_results


def get_where_condition_from_string(where_term: str, possible_columns: list) -> dict:
    """Returns a dict containing the where condition and an error if any by parsing the where_term for "is" or "="

    Parameters
    ----------
    where_term:
        A string of the condition that has to be parsed

    possible_columns:
        A list of all possible column names

    Returns
    -------
    dict:
        A dict of all the where_condition and an error if any

    Example
    -------
    >>> get_where_condition_from_string("customer_id" is 7)
    {
        "where_condition": {"column_name": "customer_id", "value": 7},
        "error": ""
    }

    """

    where = {}
    error = ""
    where_words = []
    contains_equals = False
    contains_is = False

    if where_term.count("=") > 0:
        where_words = where_term.split("=")
        contains_equals = True
    elif where_term.count(" is ") > 0:
        where_words = where_term.split(" ")
        contains_is = True

    for i, word in enumerate(where_words):
        word = word.strip()
        where_words[i] = word

    if contains_is:
        index_of_seperator = where_words.index("is")
        column_name = " ".join(where_words[:index_of_seperator])
        column_name = find_correct_column_name(
            column_name, possible_columns
        )[0]
        value = " ".join(where_words[index_of_seperator + 1:])
        where = {"column_name": column_name, "value": value}
    elif contains_equals:
        column_name = where_words[0]
        column_name = find_correct_column_name(
            column_name, possible_columns
        )[0]
        value = where_words[1]
        where = {"column_name": column_name, "value": value}
    else:
        error = "Could not parse where condition!"

    return {"where_condition": where, "error": error}
