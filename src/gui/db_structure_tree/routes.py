from flask import Blueprint, render_template, url_for, flash, redirect

from gui import connection

from .utils import get_table_names, get_table_structures

posts = Blueprint(name='posts', import_name=__name__)

tables = get_table_names(connection)
table_structures = get_table_structures(tables, connection)


@posts.route('/db_structure_tree')
def db_structure_tree():
    context = {
        "title": "Data Sructure",
        "table_structures": table_structures
    }
    return render_template('db_structure_tree.html', **context)
