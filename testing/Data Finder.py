import sqlalchemy as db

from helpers import (
    get_table_names,
    find_correct_column_name,
    get_joined_tables,
    get_table_structures,
    get_columns,
    get_tables_from_column_name
)

engine = db.create_engine(
    "mysql+mysqldb://root:password@localhost:3306/sql_store", echo=True)
connection = engine.connect()
metadata = db.MetaData()

tables = get_table_names(connection)
table_structures = get_table_structures(tables, connection)
columns = get_columns(table_structures)


# * Testing ==>
print(f"Available Columns: {columns}")

input_col_name = input("Column name: ")
print(f"You typed: {input_col_name}")

print("\n------------------------------------\n")

inferred_col_name = find_correct_column_name(input_col_name, columns)[0]
print(f"Inferred column name: {inferred_col_name}")

tables_containing_inferred_col = get_tables_from_column_name(
    inferred_col_name, table_structures)
print(f"Tables containing inferred column: {tables_containing_inferred_col}")

results = get_joined_tables(inferred_col_name,
                            tables_containing_inferred_col,
                            metadata,
                            engine,
                            connection,
                            where={"column_name": "order_id", "value": "1"})
for r in results:
    print(r)
