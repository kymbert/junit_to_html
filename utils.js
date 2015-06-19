window.onload = function() {
    cells = document.querySelectorAll("div.feature td");
    summaryCells = document.querySelectorAll("div#summary td")
    colorize(cells);
    updateStepsFont(cells);
    addLinks(summaryCells);
}

function colorize(cells) {
    var i = 0;
    while (i != cells.length) {
        if (cells[i].innerHTML == "failed" || cells[i].innerHTML == "error") {
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

function addLinks(cells) {
    var i = 0;
    while (i != cells.length) {
        if (cells[i].previousSibling == null) {
            cells[i].setAttribute("onclick",
                                  "document.getElementById('" + cells[i].innerHTML + "').scrollIntoView()");
        }
        i++;
    }
}