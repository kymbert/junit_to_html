#!usr/bin/env python
import os
from xml.etree import ElementTree


_cssString = """
body {
    font-family: "Helvetica", sans-serif;
}

table {
    border-collapse: collapse;
}

td {
    border: solid;
    border-width: thin;
    background: #fff;
    padding: 0.25em;
    white-space: pre-line;
}

tr.table_header td{
   font-weight: bold;
   background: #fa4;
}

div.feature {
    margin-top: 1em;
    margin-bottom: 1em;
    padding: 0.25em;
    /* background: #bcf; */
}

div#summary {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    padding: 0.25em;
    border: solid;
    border-color: #921;
    /* background: #ff9; */
}
"""


_jsString = """
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
"""


def _junitFiles(junitDir):
    """Get a list of *.xml files in current working directory.

    Returns:
        list: *.xml files in current working directory.
    """
    files = []
    for f in os.listdir(junitDir):
        if f.endswith(".xml"):
            junitFile = "{0}\\{1}".format(junitDir, f)
            files.append(junitFile)
        else:
            pass
    return files


def _summaryTable(junitDir):
    """Create the summary of the test run.

    Scans the current working directory for all xml files (by checking the file
    extension). Uses the <testsuite> element of the xml file to get information
    about the feature results and appends to a table.

    Returns:
        ElementTree.Element: a div element containing the summary table.
    """
    summary = ElementTree.Element("div")
    summary.set("id", "summary")

    h1 = ElementTree.Element("h1")
    h1.text = "Summary"

    table = ElementTree.Element("table")
    header = ElementTree.Element("tr")
    header.set("class", "table_header")
    headers = ["Feature",
               "Tests Executed",
               "Failures",
               "Errors",
               "Percent Passing"]
    for h in headers:
        cell = ElementTree.Element("td")
        cell.text = h
        header.append(cell)
    table.append(header)

    for f in _junitFiles(junitDir):
        with open(f) as g:
            doc = ElementTree.parse(g)

        testsuite = doc.iter("testsuite")
        suite = next(testsuite)

        name = suite.get("name")
        numTest = suite.get("tests")
        numFail = suite.get("failures")
        numErr = suite.get("errors")
        numSkip = suite.get("skipped")
        numExec = str(int(numTest) - int(numSkip))

        try:
            percentPass = 100 * \
                (float(numTest) - float(numFail) - float(numErr) - float(numSkip)) \
                / float(numExec)
        except:
            percentPass = "N/A"

        row = ElementTree.Element("tr")
        cells = [name,
                 numExec,
                 numFail,
                 numErr,
                 str(percentPass) + "%"]
        for c in cells:
            cell = ElementTree.Element("td")
            cell.text = c
            row.append(cell)
        table.append(row)

    summary.append(h1)
    summary.append(table)
    return summary


def _featureTable(featureFile):
    """Create a table of test case results for a feature file.

    Iterates through <testcase> elements and creates a table of results
    including Test Case (name), Status, Time, Type (error type), Message
    (error message), and System Out (the steps).

    Arguments:
        junitDir filepath: directory location of the junit files.
        featureFile file: junit file containing test cases to display results.
    Returns:
        ElementTree.Element: div containing the table with results.
    """
    with open(featureFile) as f:
        doc = ElementTree.parse(f)
    testsuite = doc.iter("testsuite")
    suiteName = next(testsuite).get("name")

    div = ElementTree.Element("div")
    div.set("class", "feature")

    anchor = ElementTree.Element("a")
    anchor.set("id", suiteName)

    h2 = ElementTree.Element("h2")
    h2.text = suiteName

    table = ElementTree.Element("table")
    header = ElementTree.Element("tr")
    header.set("class", "table_header")
    headers = ["Test Case",
               "Status",
               "Time (sec)",
               "Message",
               "Fail Type",
               "Steps"]
    for h in headers:
        cell = ElementTree.Element("td")
        cell.text = h
        header.append(cell)
    table.append(header)

    testCases = doc.iter("testcase")
    for test in testCases:
        status = test.get("status")
        if status == "skipped":
            pass
        else:
            if status == "passed":
                name = test.get("name")
                time = test.get("time")
                err_type = ""
                message = ""
                # system_out = test.find("system-out").text
                system_out = ""
            elif status == "failed":
                name = test.get("name")
                time = test.get("time")
                err_type = test.get("type")
                message = test.get("message")
                system_out = test.find("system-out").text
            elif status == "error":
                name = test.get("name")
                time = test.get("time")
                err_type = test.find("error").get("type")
                message = ""  # test.find("error").text
                system_out = test.find("system-out").text
            else:
                name = ""
                time = ""
                err_type = ""
                message = ""
                system_out = ""

            row = ElementTree.Element("tr")
            cells = [name,
                     status,
                     time,
                     err_type,
                     message,
                     system_out]
            for c in cells:
                cell = ElementTree.Element("td")
                cell.text = c
                row.append(cell)
            table.append(row)

    div.append(anchor)
    div.append(h2)
    div.append(table)
    return div


def htmlString(junitDir):
    """Create an HTML file for reporting.

    Builds an HTML string for writing to a file. This includes a summary of
    test results and separate tables for each feature (junit xml file).

    Returns:
        string: serialized representation of the HTML.
    """
    html = ElementTree.Element("html")
    # <head>
    head = ElementTree.Element("head")
    title = ElementTree.Element("title")
    title.text = "Test Results"
    style = ElementTree.Element("style")
    style.text = _cssString
    script = ElementTree.Element("script")
    script.set("type", "text/javascript")
    script.text = _jsString
    # </head>
    # <body>
    body = ElementTree.Element("body")
    summary = _summaryTable(junitDir)
    for f in _junitFiles(junitDir):
        feature = _featureTable(f)
        body.append(feature)
    # </body>

    head.append(title)
    head.append(style)
    head.append(script)
    body.insert(0, summary)
    html.append(head)
    html.append(body)

    return ElementTree.tostring(html)


def writeHTMLFile(junitDir, targetFile):
    html = htmlString(junitDir)
    with open(targetFile, "w") as f:
        f.write(html)

if __name__ == "__main__":
    writeHTMLFile("./", "./index.html")
