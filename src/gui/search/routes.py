from flask import Blueprint, render_template

from gui import connection, metadata, engine, nlp

from .utils import find_correct_name, get_common_column_name_from_tables, get_table_data, get_table_names, get_table_structures, get_tables_from_column_name, get_joined_tables, get_columns, get_where_condition_from_string
from .forms import ColumnSearchForm

search = Blueprint(name='search', import_name=__name__)


@search.route('/search', methods=["GET", "POST"])
def column_search():
    tables = get_table_names(connection)
    table_structures = get_table_structures(tables, connection)

    results = {"column_names": [], "column_data": []}
    search_term = ""
    where_term = ""
    search_error = ""
    inferred_table_names = []
    where = {}

    form = ColumnSearchForm()
    if form.validate_on_submit():
        try:
            if form.search_term.data.count("where") > 0:
                search_term = form.search_term.data.split(" where ")[0]
                where_term = form.search_term.data.split(" where ")[1]
            else:
                search_term = form.search_term.data

            search_term = nlp(search_term)
            for token in search_term:
                if token.pos_ != "PUNCT" and len(token.text.strip()) != 0:
                    inferred_table_name = find_correct_name(
                        token.text.strip(),
                        tables,
                        cutoff=50
                    )[0]
                    inferred_table_names.append(inferred_table_name)

            if len(inferred_table_names) > 0:
                if where_term:
                    possible_column_names = []
                    for table_name in inferred_table_names:
                        for col_name in table_structures[table_name]:
                            possible_column_names.append(col_name)
                    where_condition = get_where_condition_from_string(
                        where_term, possible_column_names)
                    where = where_condition["where_condition"]
                    search_error = where_condition["error"]

                if len(inferred_table_names) == 1:
                    results = get_table_data(
                        inferred_table_names[0], metadata, engine, connection)
                else:
                    common_column_name = get_common_column_name_from_tables(
                        inferred_table_names, table_structures)
                    if common_column_name:
                        results = get_joined_tables(
                            common_column_name,
                            inferred_table_names,
                            metadata,
                            engine,
                            connection,
                            table_structures,
                            where=where
                        )
                        if len(results["column_data"]) == 0:
                            search_error = "Your search query did not return any results"
                    else:
                        search_error = "The requested tables do not have any common columns"
            else:
                search_error = "Unable to parse any table names from search query"
        except Exception as e:
            search_error = e

    context = {
        "title": "Data Sructure",
        "active": "search",
        "form": form,
        "table_headers": results["column_names"],
        "table_data": results["column_data"],
        "inferred_table_names": inferred_table_names,
        "search_error": search_error
    }
    return render_template('column_search.html', **context)
