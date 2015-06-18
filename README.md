# junit_to_html
Python module to create an HTML summary page from junit XML reports.

# Usage


# Private varaiables and functions


# Public variables and functions
### `cssFile`
File path to stylesheet for the HTML report. Defaults to "stylesheet.css". The `cssFile` variable
can be overridden to use any stylesheet.

### `jsFile`
File path to JavaScript file for the HTML report. Defaults to "utils.js". Like `cssFile`, the
`jsFile` variable can be overridden to use any JavaScript file.

### `createHtmlString()`
Create an HTML string literal.

This function builds an HTML string for writing to a file. It requires that the private `_junitFiles`
variable has been populated. The HTML string includes a summary of test results and separate tables
for each testsuite. The string can then be written to a new file or embedded into an existing HTML
file.

### `writeHtmlFile(junitDir, targetFile, css=None, js=None)`
Write an HTML report to a specified file.

Arguments:
* `junitDir (str)` Directory containing junit XML files to process.
* `targetFile (str)` File to write the HTML report.
* `css (Optional [str])` Override default CSS file.
* `js (Optional [str])` Override default JavaScript file.
