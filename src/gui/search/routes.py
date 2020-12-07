from flask import Blueprint, render_template

from gui import connection, metadata, engine

from .utils import find_correct_column_name, get_table_names, get_table_structures, get_tables_from_column_name, get_joined_tables, get_columns, get_where_condition_from_string
from .forms import ColumnSearchForm

search = Blueprint(name='search', import_name=__name__)


@search.route('/search', methods=["GET", "POST"])
def column_search():
    tables = get_table_names(connection)
    table_structures = get_table_structures(tables, connection)
    columns = get_columns(table_structures)

    results = {"column_names": [], "column_data": []}
    search_error = ""
    inferred_column_name = ""
    where = {}

    form = ColumnSearchForm()
    if form.validate_on_submit():
        try:
            inferred_column_name = find_correct_column_name(
                form.search_term.data,
                columns
            )[0]
            tables_containing_column = get_tables_from_column_name(
                inferred_column_name,
                table_structures
            )

            possible_columns = []
            for index in range(len(tables_containing_column)):
                possible_columns += table_structures[tables_containing_column[index]]

            if form.where_term.data:
                where_condition = get_where_condition_from_string(
                    form.where_term.data, possible_columns)
                where = where_condition["where_condition"]
                search_error = where_condition["error"]
                # print(where)

            results = get_joined_tables(
                inferred_column_name,
                tables_containing_column,
                metadata,
                engine,
                connection,
                where=where
            )
            if len(results["column_data"]) == 0:
                search_error = "Your search query did not return any results"
        except Exception as e:
            search_error = e

    context = {
        "title": "Data Sructure",
        "form": form,
        "table_headers": results["column_names"],
        "table_data": results["column_data"],
        "inferred_column_name": inferred_column_name,
        "search_error": search_error
    }
    return render_template('column_search.html', **context)
