import unittest
from io import StringIO
from unittest.mock import patch

from bin import compress_proteins
fake_args = [
    'B.taurus.fasta',
    'out',
    'taurus_save',
    'out/taurus.pc'
]


class TestCompressProteins(unittest.TestCase):

    @patch('sys.argv', ['compress_proteins.py'] + fake_args)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        compress_proteins.main()
        output = mock_stdout.getvalue()
        # Replace this assertion with the actual expected output
        self.assertEqual(output, "Compressed all 37502 sequences\n")


if __name__ == '__main__':
    unittest.main()
