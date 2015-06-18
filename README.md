# junit_to_html
Python module to create an HTML summary page from junit XML reports.

## Usage
Usage notes are forthcoming.

## Details

### Public variables and functions
#### cssFile
File path to stylesheet for the HTML report. Defaults to "stylesheet.css". The `cssFile` variable
can be overridden to use any stylesheet.

#### jsFile
File path to JavaScript file for the HTML report. Defaults to "utils.js". Like `cssFile`, the
`jsFile` variable can be overridden to use any JavaScript file.

#### createHtmlString()
Create an HTML string literal.

This function builds an HTML string for writing to a file. It requires that the private `_junitFiles`
variable has been populated. The HTML string includes a summary of test results and separate tables
for each testsuite. The string can then be written to a new file ~~or embedded into an existing HTML
file~~.

#### writeHtmlFile(junitDir, targetFile, css=None, js=None)
Write an HTML report to a specified file.

Arguments:
* `junitDir (str)` Directory path containing junit XML files to process.
* `targetFile (str)` New file to write the HTML report.
* `css (Optional [str])` Override default CSS file.
* `js (Optional [str])` Override default JavaScript file.

### Private varaiables and functions
#### _junitFiles
List of junit XML files to process. Empty until `_getJunitFiles` is called.

#### _createSummaryTable()
Create the summary of the test run.

Scans the current working directory for all XML files (by checking the file
extension). Uses the `<testsuite>` element of the XML file to get information
about the feature results and appends to a table.

Returns a div element containing the summary table as below.
```html
<div id="summary">
    <h1>Summary</h1>
    <table>
        <tr class="table-header"><!-- headers --></tr>
        <tr><!-- testsuite[0] results --></tr>
        ...
        <tr><!-- testsuite[n] results --></tr>
    </table>
</div>
```

#### _createTestsuiteTable(junitFile)
Create a table of test case results for a feature file.

Iterates through `<testcase>` elements and creates a table of results
including Test Case (name), Status, Time, Type (error type), Message
(error message), and System Out (the steps).

Arguments:
* `junitFile (str)` File path to junit file containing test cases to display results. Returns a div
containing the table with results as below.
```html
<div class="feature">
    <h2>suiteName</h2>
    <table>
        <tr class="table-header"><!-- headers --></tr>
        <tr><!-- testcase[0] results --></tr>
        ...
        <tr><!-- testcase[n] results --></tr>
    </table>
</div>
```

#### _getJunitFiles(junitDir)
Populate `_junitFiles` with *.xml files.

Iterates through all files found within the `junitDir`, appends any file with the extension ".xml"
to the module-level `_junitFiles` variable.
