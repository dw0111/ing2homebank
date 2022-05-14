# ing2homebank

Thank you to [hamvocke](https://github.com/hamvocke) for writing this for [DKB](https://github.com/hamvocke/dkb2homebank) and basically having done all the work already.

This script converts CSV account reports from ING to a
CSV format that can be imported by the personal finance software
[Homebank](http://homebank.free.fr/).

## How to run the script

To convert a file run:

    ./ing2homebank.py yourDKBExportFile.csv

You can also choose an alternative path for your output file, if the standard "converted\_{{ originalName }}.csv" in the working directory doesn't do it for you. Use `--output-file` or `-o` for that:

    ./ing2homebank.py yourCashReportFile.csv --output-file ~/Documents/Finances/import_to_homebank.csv

## Importing into Homebank

Import the converted CSV file into Homebank by going to `File -> Import` and selecting the _output_ file you got when running your script.

**Note**: If Homebank tells you that your CSV file is invalid, go to `Settings -> Import/Export` and make sure that the `Delimiter` is set to `semicolon` and try importing again.

## Requirements

To run this script, you need Python 3.4 or higher. I've verified that the exported CSV can be imported successfully on Homebank _5.0.0_ and above.

## Run the tests

I have included a (admittedly very small) set of tests to help a little bit during development.
These tests use Python's _unittest_ module and can be executed using:

    ./ing2homebankTest.py

You can also test the script manually by using the provided testfiles:

    ./ing2homebank.py testfiles/test.csv
