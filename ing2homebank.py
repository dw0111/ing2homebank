#! /usr/bin/env python3
"""
Convert a ING cash account csv file to homebank-readable csv format
"""

import argparse
import csv
from datetime import datetime


class ING(csv.Dialect):
    """ING csv format"""
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


class InvalidInputException(Exception):
    """Exception for input CSVs that seem not to be valid ING input files."""

    def __init__(self, message):
        self.message = message


csv.register_dialect("ing", ING)

ing_field_names = [
    "buchung",
    "valuta",
    "auftraggeber/empfaenger",
    "buchungstext",
    "verwendungszweck",
    "saldo",
    "waehrung",
    "betrag",
    "waehrung",
]

homebank_field_names = [
    "date", "paymode", "info", "payee", "memo", "amount", "category", "tags"
]


def _identify_csv_dialect(file_handle, field_names):
    """
    :param file_handle:
    :param field_names:
    :return:
    """
    dialect = csv.Sniffer().sniff(file_handle.readline())
    file_handle.seek(0)
    return csv.DictReader(find_transaction_lines(file_handle),
                          dialect=dialect,
                          fieldnames=field_names)


def convert_ing_cash(file_handle, output_file="homebank.csv"):
    """
    Convert a ING cash file (i.e. normal bank account) to a homebank-readable import CSV.

    :param file_handle: file handle of the file to be converted
    :param output_file: the output file path as a string
    """
    reader = _identify_csv_dialect(file_handle, ing_field_names)
    with open(output_file, 'w', 1, "latin_1") as outfile:
        writer = csv.DictWriter(outfile,
                                dialect='ing',
                                fieldnames=homebank_field_names)
        for row in reader:
            writer.writerow({
                'date':
                convert_date(row["buchung"]),
                'paymode':
                8,
                'info':
                None,
                'payee':
                row["auftraggeber/empfaenger"],
                'memo':
                row["verwendungszweck"]
                if row["verwendungszweck"] else row["buchungstext"],
                'amount':
                row["betrag"],
                'category':
                None,
                'tags':
                None
            })


def find_transaction_lines(file):
    """
    Reduce the csv lines to the lines containing actual data relevant for the conversion.

    :param file: The export CSV from ING to be converted
    :return: The lines containing the actual transaction data
    """
    lines = file.readlines()
    i = 1
    for line in lines:
        # simple heuristic to find the csv header line.
        if "Buchung" in line and "Betrag" in line:
            return lines[i:]
        i = i + 1


def convert_date(date_string):
    """Convert the date_string to dd-mm-YYYY format."""
    date = datetime.strptime(date_string, "%d.%m.%Y")
    return date.strftime('%d-%m-%Y')


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Convert a CSV export file from ING online banking "
        "to a Homebank compatible CSV format.")
    parser.add_argument("filename", help="The CSV file to convert.")

    parser.add_argument(
        '-o',
        '--output-file',
        help='choose where to store the output file (default: working directory'
    )

    parser.add_argument('--debug',
                        '-d',
                        help='output some information to STDERR')

    return parser.parse_args()


def main():
    args = setup_parser()

    with open(args.filename, 'r', encoding='latin_1') as csv_file:
        output = args.output_file or f"converted_{args.filename.split('/')[-1]}"
        convert_ing_cash(csv_file, output)
        print(f"ING Cash file converted. Output file: {output}"
              ) if args.debug else None


if __name__ == '__main__':
    main()
