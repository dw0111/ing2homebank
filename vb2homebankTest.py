#! /usr/bin/env python3

from builtins import ResourceWarning
import unittest
import vb2homebank
import os
import warnings
import tempfile
import subprocess


class Vb2HomebankTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def testShouldConvertCashFile(self):
        with open(r'testfiles/cash.csv', encoding='iso-8859-1') as csv_file:
            vb2homebank.convert_vb_cash(csv_file, 'cashHomebank.csv')
            csv_file.seek(0)
            lineNumber = len(vb2homebank.find_transaction_lines(csv_file))
            self.assertEqual(lineNumber, 2)

    def testShouldConvertCashFileAndWriteToAlternativeOutputDir(self):
        with open(r'testfiles/cash.csv', encoding='iso-8859-1') as csv_file:
            tmpdir = tempfile.gettempdir()
            vb2homebank.convert_vb_cash(csv_file, os.path.join(tmpdir, "cashHomebank.csv"))

    def testThrowErrorForEmptyCashFile(self):
        with self.assertRaises(ValueError) as context:
            with open('testfiles/cash_empty.csv', encoding='iso-8859-1') as csv_file:
                vb2homebank.convert_vb_cash(csv_file)
        self.assertTrue("Can't convert CSV file without header line" in str(context.exception))

    def testShouldConvertVisaFile(self):
        with open('testfiles/visa.csv', encoding='iso-8859-1') as csv_file:
            vb2homebank.convert_visa(csv_file, 'visaHomebank.csv')
            csv_file.seek(0)
            lineNumber = len(vb2homebank.find_transaction_lines(csv_file))
        self.assertEqual(lineNumber, 4)

    def testShouldConvertVisaFileWithRange(self):
        with open('testfiles/visaRange.csv', encoding='iso-8859-1') as csv_file:
            vb2homebank.convert_visa(csv_file, 'visaHomebank.csv')
            csv_file.seek(0)
            lineNumber = len(vb2homebank.find_transaction_lines(csv_file))
            self.assertEqual(lineNumber, 1)

    def tearDown(self):
        self.delete('homebank.csv')

    def delete(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)


class Vb2HomebankFunctionalTest(unittest.TestCase):
    def testShouldRunScriptWithCashParameter(self):
        result = subprocess.run(["./vb2homebank.py", "--cash", "testfiles/cash.csv"])
        self.assertEqual(0, result.returncode)

    def testShouldRunScriptWithVisaParameter(self):
        result = subprocess.run(["./vb2homebank.py", "--visa", "testfiles/visa.csv"])
        self.assertEqual(0, result.returncode)

    def testShouldRunScriptWithOutputParameter(self):
        result = subprocess.run(["./vb2homebank.py", "--cash", "testfiles/cash.csv", "--output-file", "/tmp/vb2homebank.csv"])
        self.assertEqual(0, result.returncode)


if __name__ == '__main__':
    unittest.main()
