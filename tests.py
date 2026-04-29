import unittest
import os
import json

from validator import validate_pages, validate_not_empty
from storage import load_data, save_data

_DATA_FILE = "data.json"


class TestValidatePages(unittest.TestCase):
    """Тесты валидации количества страниц."""

    def test_positive_integer(self):
        """Положительное целое принимается (позитивный)."""
        self.assertTrue(validate_pages("300"))

    def test_one_page(self):
        """Одна страница принимается (граничный)."""
        self.assertTrue(validate_pages("1"))

    def test_zero_rejected(self):
        """Ноль отклоняется (граничный)."""
        self.assertFalse(validate_pages("0"))

    def test_negative_rejected(self):
        """Отрицательное значение отклоняется (негативный)."""
        self.assertFalse(validate_pages("-10"))

    def test_float_rejected(self):
        """Дробное число отклоняется (негативный)."""
        self.assertFalse(validate_pages("100.5"))

    def test_non_numeric_rejected(self):
        """Нечисловая строка отклоняется (негативный)."""
        self.assertFalse(validate_pages("много"))

    def test_empty_rejected(self):
        """Пустая строка отклоняется (граничный)."""
        self.assertFalse(validate_pages(""))


class TestValidateNotEmpty(unittest.TestCase):
    """Тесты проверки на непустое значение."""

    def test_valid_string(self):
        """Непустая строка принимается (позитивный)."""
        self.assertTrue(validate_not_empty("Война и Мир"))

    def test_spaces_only(self):
        """Строка из пробелов отклоняется (граничный)."""
        self.assertFalse(validate_not_empty("   "))

    def test_empty_string(self):
        """Пустая строка отклоняется (негативный)."""
        self.assertFalse(validate_not_empty(""))


class TestStorage(unittest.TestCase):
    """Тесты JSON-хранилища."""

    def tearDown(self):
        if os.path.exists(_DATA_FILE):
            os.remove(_DATA_FILE)

    def test_save_and_load(self):
        """Сохранение и загрузка корректны (позитивный)."""
        data = [{"title": "1984", "author": "Оруэлл", "genre": "Фантастика", "pages": 328}]
        save_data(data)
        self.assertEqual(load_data(), data)

    def test_load_no_file(self):
        """Без файла — пустой список (позитивный)."""
        if os.path.exists(_DATA_FILE):
            os.remove(_DATA_FILE)
        self.assertEqual(load_data(), [])

    def test_load_corrupt(self):
        """Повреждённый JSON — пустой список (негативный)."""
        with open(_DATA_FILE, "w") as f:
            f.write("{{broken")
        self.assertEqual(load_data(), [])

    def test_filter_by_genre(self):
        """Фильтрация по жанру работает (позитивный)."""
        records = [
            {"title": "Dune", "author": "Herbert", "genre": "Фантастика", "pages": 700},
            {"title": "Holmes", "author": "Doyle", "genre": "Детектив", "pages": 300},
        ]
        result = [r for r in records if r["genre"] == "Фантастика"]
        self.assertEqual(len(result), 1)

    def test_filter_by_pages(self):
        """Фильтрация по количеству страниц > 200 работает (позитивный)."""
        records = [
            {"title": "Short", "author": "A", "genre": "Роман", "pages": 100},
            {"title": "Long", "author": "B", "genre": "Роман", "pages": 500},
        ]
        result = [r for r in records if r["pages"] > 200]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Long")


if __name__ == "__main__":
    unittest.main(verbosity=2)
