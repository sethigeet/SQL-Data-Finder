function autocomplete(inp, arr) {
    var currentFocus;
    var original_arr = [...arr];
    var new_arr = [];

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
            original_arr = [...arr];
        } else if (
            val.substr(val.length - 2, val.length - 1) === ", " ||
            val[val.length - 1] === " " ||
            val[val.length - 1] === ","
        ) {
            original_arr = original_arr.map((_, i) => val + arr[i]);
        } else {
            original_arr = [...new_arr];
        }
        new_arr = [...original_arr];
        for (i = 0; i < original_arr.length; i++) {
            if (
                new_arr[i].substr(0, val.length).toLowerCase() ==
                val.toLowerCase()
            ) {
                b = document.createElement("DIV");
                b.innerHTML =
                    "<strong>" + new_arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += new_arr[i].substr(val.length);
                b.innerHTML +=
                    "<input type='hidden' value='" + new_arr[i] + "'>";
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
