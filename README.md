# XML analyzer and formatter

## Testing

You can find test files in the test folder.

### Testing formatter

* test/formatter/import1.xml - to test how program sets indents, aligns attributes and formats short text
* test/formatter/import2.xml - to test how program formats long text that can be split and text that cannot be split (doesn't have whitespaces)
* test/formatter/import3.xml - to test how program formats long attributes
* test/formatter/import4.xml - to test what program does with empty lines

### Testing analyzer

* test/analyzer/import1.xml - file with unclosed tags
* test/analyzer/import2.xml - file with unmatched closing tag (<name1></name>)
* test/analyzer/import3.xml - file with unclosing double quote in attribute
* test/analyzer/import4.xml - file with invalid tag name (<1name></1name>)
* test/analyzer/import5.xml - file with attribute without value
* test/analyzer/import5.xml - file with attribute's name xml
