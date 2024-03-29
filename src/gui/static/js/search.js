function autocomplete(inp, table_structures) {
    var tables = [];
    for (let table in table_structures) {
        tables.push(table);
    }

    var currentFocus;
    var recommendations = [...tables];
    var val_tables = [];

    inp.addEventListener("input", function () {
        var a,
            b,
            i,
            val = this.value;

        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(a);

        if (
            val.indexOf(", ") === -1 &&
            val.indexOf(" ") === -1 &&
            val.indexOf(",") === -1
        ) {
            recommendations = [...tables];
        } else if (
            val.substr(val.length - 2, val.length - 1) === ", " ||
            val[val.length - 1] === " " ||
            val[val.length - 1] === ","
        ) {
            if (
                val
                    .split(" ")
                    .filter((val) => !(val in [",", " ", "."]))
                    .indexOf("where") !== -1
            ) {
                recommendations = [];
                val_tables = val
                    .split(" where ")[0]
                    .split(" ")
                    .filter((val) => !(val in [",", " ", "."]));
                for (let i in val_tables) {
                    columns = table_structures[val_tables[i]];
                    for (let column_i in columns) {
                        column = columns[column_i];
                        if (
                            val
                                .split(" where ")[1]
                                .split(" ")
                                .filter((val) => !(val in [",", " ", "."]))
                                .indexOf(column) === -1
                        ) {
                            recommendations[recommendations.length] =
                                val + column;
                        }
                    }
                }
            } else {
                for (let i = 0; i < tables.length; i++) {
                    if (
                        val
                            .split(" ")
                            .filter((val) => !(val in [",", " ", "."]))
                            .indexOf(tables[i]) === -1
                    ) {
                        recommendations[recommendations.length] =
                            val + tables[i];
                    }
                }
            }

            if (
                val
                    .split(" ")
                    .filter((val) => !(val in [",", " ", "."]))
                    .indexOf("where") === -1
            ) {
                recommendations[recommendations.length] = val + "where";
            }
        }

        for (i = 0; i < recommendations.length; i++) {
            if (
                recommendations[i].substr(0, val.length).toLowerCase() ==
                val.toLowerCase()
            ) {
                b = document.createElement("DIV");
                b.innerHTML =
                    "<strong>" +
                    recommendations[i].substr(0, val.length) +
                    "</strong>";
                b.innerHTML += recommendations[i].substr(val.length);
                b.innerHTML +=
                    "<input type='hidden' value='" + recommendations[i] + "'>";
                b.addEventListener("click", function () {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = x.length - 1;
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}
