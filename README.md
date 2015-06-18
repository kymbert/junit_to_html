# junit_to_html
Python module to create an HTML summary page from junit XML reports.

### FUNCTIONS
*createHtmlString*
    createHtmlString()
        Create an HTML string literal for reporting.

        Builds an HTML string for writing to a file. This includes a summary of
        test results and separate tables for each testsuite (junit XML file).

        Returns:
            string: Serialized representation of the HTML.

*writeHtmlFile*
    writeHtmlFile(junitDir, targetFile, css=None, js=None)
        Write an HTML report to specified file.

        Args:
            junitDir (str): Directory containing junit XML files to process.
            targetFile (str): File to write the HTML report.
            css (Optional [str]): Override default CSS file.
            js (Optional [str]): Override default JavaScript file.

### DATA
    cssFile = 'stylesheet.css'
    jsFile = 'utils.js'