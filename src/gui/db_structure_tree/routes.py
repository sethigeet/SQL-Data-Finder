from flask import Blueprint, render_template

from gui import connection

from .utils import get_table_names, get_table_structures

db_structure = Blueprint(name='db_structure', import_name=__name__)


@db_structure.route('/db_structure_tree')
def db_structure_tree():
    tables = get_table_names(connection)
    table_structures = get_table_structures(tables, connection)

    db_structure_data = {
        "id": "db",
        "name": "Database",
        "data": {},
        "children": []
    }
    for table_structure in table_structures.keys():
        temp_table_structure = {
            "id": f"{table_structure}",
            "name": f"{table_structure}",
            "data": {},
            "children": []
        }

        for column in table_structures[table_structure]:
            temp_column_structure = {
                "id": f"{table_structure}-{column}",
                "name": f"{column}",
                "data": {},
                "children": []
            }
            temp_table_structure["children"].append(temp_column_structure)

        db_structure_data["children"].append(temp_table_structure)

    context = {
        "title": "Data Sructure",
        "active": "db_structure",
        "db_structure": db_structure_data
    }
    return render_template('db_structure_tree.html', **context)
