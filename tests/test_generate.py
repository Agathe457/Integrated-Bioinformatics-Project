import unittest
from io import StringIO
from unittest.mock import patch

from bin import generate_codec

fake_args = [
    'prot.fasta',
    'out',  # Separate the output_folder and its value
    '3',
    'taurus',  # Separate the name and its value
    'fasta',
]


class TestGenerateProteinCodec(unittest.TestCase):
    @patch('sys.argv', ['generate_codec.py'] + fake_args)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        generate_codec.main()
        output = mock_stdout.getvalue().strip()  # Remove leading/trailing whitespace
        expected_output = "Codec taurus has been generated"  # Replace with your expected output
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
