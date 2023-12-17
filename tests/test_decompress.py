import unittest
from io import StringIO
from unittest.mock import patch

from bin import decompress_proteins

fake_args = [
    'out/taurus_save.pc',
    'out',
    'taurus_save',
    'out/B.taurus.sequences',
]


class TestDecompressProteins(unittest.TestCase):

    @patch('sys.argv', ['decompress_proteins.py'] + fake_args)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        decompress_proteins.main(limit=1)
        output = mock_stdout.getvalue()
        # Replace this assertion with the actual expected output
        self.assertIn("Decompressed 2 proteins\n", output)


if __name__ == '__main__':
    unittest.main()
