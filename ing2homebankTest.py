#! /usr/bin/env python3

from builtins import ResourceWarning
import unittest
import os
import warnings
import tempfile
import subprocess
import ing2homebank


class ING2HomebankTest(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def testShouldConvertCashFile(self):
        with open(r'testfiles/test.csv', encoding='latin_1') as csv_file:
            ing2homebank.convert_ing_cash(csv_file, 'testresult.csv')
            csv_file.seek(0)
            lineNumber = len(ing2homebank.find_transaction_lines(csv_file))
            self.assertEqual(lineNumber, 2)

    def testShouldConvertCashFileAndWriteToAlternativeOutputDir(self):
        with open(r'testfiles/test.csv', encoding='latin_1') as csv_file:
            tmpdir = tempfile.gettempdir()
            ing2homebank.convert_ing_cash(
                csv_file, os.path.join(tmpdir, "testresult.csv"))

    def tearDown(self):
        self.delete('testresult.csv')

    def delete(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)


class ING2HomebankFunctionalTest(unittest.TestCase):

    def testShouldRunScript(self):
        result = subprocess.run(["./ing2homebank.py", "testfiles/test.csv"])
        self.assertEqual(0, result.returncode)

    def testShouldRunScriptWithOutputParameter(self):
        result = subprocess.run([
            "./ing2homebank.py", "testfiles/test.csv", "--output-file",
            "/tmp/testresult.csv"
        ])
        self.assertEqual(0, result.returncode)

    def tearDown(self):
        default_output_name = 'converted_test.csv'
        self.delete(default_output_name)

    def delete(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
