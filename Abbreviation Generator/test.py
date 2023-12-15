import unittest
import os
import unittest.mock

from main import getabbr, calculatescores, getbestscore, readfile, outputfile

class TestAbbreviation(unittest.TestCase):

    def test_abbreviation_content(self):
        input_filename = 'test_input'
        input_surname = 'alozie'

        # Create an input file with specific content
        with open(f'{input_filename}.txt', 'w') as test_input:
            test_input.write("Cold\n")
            test_input.write("Cool\n")
            test_input.write("C++ Code")

        # Read file content based on the provided filename
        file, nameoffile = readfile()

        # Generate abbreviations from file content
        wordstoabbr = getabbr(file)

        # Calculate scores for abbreviations
        abbrsandscores = calculatescores(wordstoabbr)

        # Get the best score for each name
        abbrsandbestscores = getbestscore(abbrsandscores)

        # Write the generated abbreviations to an output file based on the provided surname
        outputfile(abbrsandbestscores, nameoffile)

        # Check if the output file is created
        output_filename = f'{input_surname}_{nameoffile}_abbrevs.txt'
        self.assertTrue(os.path.exists(output_filename))

        # Check the content of the output file
        expected_content = [
            "Cold\n",
            "CLD\n",
            "\n",
            "Cool\n",
            "COO\n",
            "\n",
            "C++ Code\n",
            "CCD\n",
            "\n"
        ]

        with open(output_filename, 'r') as output_file:
            actual_content = output_file.readlines()

        # Check each line of the output file against the expected content
        for expected, actual in zip(expected_content, actual_content):
            self.assertEqual(expected, actual)

        # Clean up - remove the test input and output files
        #os.remove(f'{input_filename}.txt')
        #os.remove(output_filename)

if __name__ == '__main__':
    unittest.main()
