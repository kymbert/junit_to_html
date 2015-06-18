window.onload = function() {
    cells = document.querySelectorAll("div.feature td");
    colorize(cells);
    updateStepsFont(cells);
}

function colorize(cells) {
    var i = 0;
    while (i != cells.length) {
        if (cells[i].innerHTML == "failed") {
            cells[i].setAttribute("style", "background-color:#faa");
        }
        else if (cells[i].innerHTML == "passed") {
            cells[i].setAttribute("style", "background-color:#afa");
        }
        i++;
    }
}

function updateStepsFont(cells) {
  var i = 0;
    while (i != cells.length) {
        if (cells[i].nextElementSibling == null) {
            if (cells[i].parentElement.getAttribute("class") != "table_header") {
                cells[i].setAttribute("style", "font-family: monospace");
            }
        }
        i++;
    }
}