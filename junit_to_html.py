# -*- coding: utf-8 -*-
#!usr/bin/python
"""Create a summary html page to display junit test results."""
import os
from xml.etree import ElementTree

_junitFiles = []
"""List of junit XML files to process. Empty until `_getJunitFiles` is called."""

cssFile = "stylesheet.css"
"""Stylesheet for the HTML report. Defaults to "stylesheet.css"."""

jsFile = "utils.js"
"""JavaScript file for the HTML report. Defaults to "utils.js"."""


def _createSummaryTable():
    """Create the summary of the test run.

    Scans the current working directory for all XML files (by checking the file
    extension). Uses the `<testsuite>` element of the XML file to get information
    about the feature results and appends to a table.

    Returns:
        ElementTree.Element: A div element containing the summary table as below.
            <div id="summary">
                <h1>Summary</h1>
                <table>
                    <tr class="table-header">
                        <td>(headers) ... </td>
                    </tr>
                    <tr>
                        <td>(testsuite[0] results) ... </td>
                    </tr>
                    <tr>
                        <td>(testsuite[n] results) ... </td>
                    </tr>
                </table>
            </div>
    """
    summary = ElementTree.Element("div")
    summary.set("id", "summary")

    h1 = ElementTree.Element("h1")
    h1.text = "Summary"

    table = ElementTree.Element("table")
    header = ElementTree.Element("tr")
    header.set("class", "table_header")
    headers = ["Test Suite",
               "Tests Executed",
               "Failures",
               "Errors",
               "Percent Passing"]
    for h in headers:
        cell = ElementTree.Element("td")
        cell.text = h
        header.append(cell)
    table.append(header)

    for f in _junitFiles:
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


def _createTestsuiteTable(junitFile):
    """Create a table of test case results for a feature file.

    Iterates through `<testcase>` elements and creates a table of results
    including Test Case (name), Status, Time, Type (error type), Message
    (error message), and System Out (the steps).

    Args:
        junitFile (file): junit file containing test cases to display results.
    Returns:
        ElementTree.Element: div containing the table with results as below.
        <div class="feature">
            <h2>suiteName</h2>
            <table>
                <tr class="table-header">
                    <td>(headers) ... </td>
                </tr>
                <tr>
                    <td>(testcase[0] results) ... </td>
                </tr>
                <tr>
                    <td>(testcase[n] results) ... </td>
                </tr>
            </table>
        </div>
    """
    with open(junitFile) as f:
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
               "Failure/Error Type",
               "Message", ]
               # "Steps"]
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
                err_type = test.find("error").get("type")
                message = test.find("error").text
                # message = test.get("message")
                system_out = test.find("system-out").text
            elif status == "error":
                name = test.get("name")
                time = test.get("time")
                err_type = test.find("error").get("type")
                message = test.find("error").text
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
                     message, ]
                     # system_out]
            for c in cells:
                cell = ElementTree.Element("td")
                cell.text = c
                row.append(cell)
            table.append(row)

    div.append(anchor)
    div.append(h2)
    div.append(table)
    return div


def _getJunitFiles(junitDir):
    """Populate _junitFiles with *.xml files."""

    for f in os.listdir(junitDir):
        if f.endswith(".xml"):
            junitFile = "{0}\\{1}".format(junitDir, f)  # TODO: cross-platform
            _junitFiles.append(junitFile)
        else:
            pass


def createHtmlString():
    """Create an HTML string literal for reporting.

    Builds an HTML string for writing to a file. This includes a summary of
    test results and separate tables for each testsuite (junit XML file).

    Returns:
        string: Serialized representation of the HTML.
    """
    html = ElementTree.Element("html")
    # <head>
    head = ElementTree.Element("head")
    title = ElementTree.Element("title")
    title.text = "Test Results"
    with open(cssFile) as f:
        style = ElementTree.Element("style")
        style.text = f.read()
    with open(jsFile) as f:
        script = ElementTree.Element("script")
        script.set("type", "text/javascript")
        script.text = f.read()
    # </head>
    # <body>
    body = ElementTree.Element("body")
    summary = _createSummaryTable()
    for f in _junitFiles:
        testsuite = _createTestsuiteTable(f)
        body.append(testsuite)
    # </body>

    head.append(title)
    head.append(style)
    head.append(script)
    body.insert(0, summary)
    html.append(head)
    html.append(body)

    return ElementTree.tostring(html)


def writeHtmlFile(junitDir, targetFile, css=None, js=None):
    """Write an HTML report to specified file.

    Args:
        junitDir (str): Directory containing junit XML files to process.
        targetFile (str): New file to write the HTML report.
        css (Optional [str]): Override default CSS file.
        js (Optional [str]): Override default JavaScript file.
    """
    global cssFile, jsFile
    if css is not None:
        cssFile = css
    if js is not None:
        jsFile = js

    _getJunitFiles(junitDir)
    html = createHtmlString()
    with open(targetFile, "w") as f:
        f.write(html)


# if __name__ == "__main__":
#     writeHtmlFile("./", "./index.html")
