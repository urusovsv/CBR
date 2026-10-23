"""
Тесты для библиотеки cbr_key_rate.
"""

import unittest
from datetime import datetime, timedelta
from cbr_key_rate.scraper import split_date_range


class TestSplitDateRange(unittest.TestCase):
    """Тесты для функции split_date_range."""

    def test_single_chunk(self):
        """Тест диапазона, который помещается в один чанк."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 15)
        chunks = list(split_date_range(start, end, chunk_days=30))
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], (start, end))

    def test_multiple_chunks(self):
        """Тест диапазона, требующего разбиения на несколько чанков."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 3, 1)  # 60 дней
        chunks = list(split_date_range(start, end, chunk_days=30))
        
        self.assertEqual(len(chunks), 2)  # 30 + 29 дней
        
        # Проверка первого чанка
        self.assertEqual(chunks[0][0], start)
        self.assertEqual(chunks[0][1], datetime(2023, 1, 30))
        
        # Проверка последнего чанка
        self.assertEqual(chunks[-1][1], end)

    def test_exact_chunk_boundary(self):
        """Тест диапазона, точно равного размеру чанка."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 30)
        chunks = list(split_date_range(start, end, chunk_days=30))
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], (start, end))

    def test_empty_range(self):
        """Тест пустого диапазона."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 1)
        chunks = list(split_date_range(start, end, chunk_days=30))
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], (start, end))


if __name__ == "__main__":
    unittest.main()
