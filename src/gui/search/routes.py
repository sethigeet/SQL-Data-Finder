from flask import Blueprint, render_template, flash

from gui import connection, metadata, engine

from .utils import find_correct_column_name, get_table_names, get_table_structures, get_tables_from_column_name, get_joined_tables, get_columns
from .forms import ColumnSearchForm

search = Blueprint(name='search', import_name=__name__)


@search.route('/search', methods=["GET", "POST"])
def column_search():
    tables = get_table_names(connection)
    table_structures = get_table_structures(tables, connection)
    columns = get_columns(table_structures)

    results = {"column_names": [], "column_data": []}

    form = ColumnSearchForm()
    if form.validate_on_submit():
        correct_column_name = find_correct_column_name(
            form.search_term.data,
            columns
        )[0]
        tables_containing_column = get_tables_from_column_name(
            correct_column_name,
            table_structures
        )
        results = get_joined_tables(
            correct_column_name,
            tables_containing_column,
            metadata,
            engine,
            connection
        )

        flash('Your columns are being search for!', category='success')

    context = {
        "title": "Data Sructure",
        "form": form,
        "table_headers": results["column_names"],
        "table_data": results["column_data"]
    }
    return render_template('column_search.html', **context)
