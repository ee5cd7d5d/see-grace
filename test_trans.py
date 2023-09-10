import unittest

from trans import get_header_width


class TransTest(unittest.TestCase):
    def test_get_header_with_returns_expected_from_single_line_header(self):
        content = bytearray([0x01, 0x0B, 0x12, 0x2, 0x0A])
        self.assertEqual(get_header_width(content), 4)

    def test_get_header_with_returns_expected_from_multiple_line_header_with_data(self):
        content = bytearray(
            [0x01, 0x0B, 0x12, 0x2, 0x0A, 0x02, 0xAB, 0x32, 0x24, 0x0A, 0x32, 0x24]
        )
        self.assertEqual(get_header_width(content), 4)


# pragma: no cover is needed because this function needs to be excluded from code coverage
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
