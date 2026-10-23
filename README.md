# CBR Key Rate

Библиотека для получения истории ключевой ставки Центрального банка Российской Федерации.

## Описание

Этот пакет предоставляет инструменты для скачивания, обработки и анализа ежедневных значений ключевой ставки ЦБ РФ с официального сайта cbr.ru.

### Особенности

- Автоматическая разбивка запросов на 30-дневные периоды для обхода ограничений API
- Обработка и очистка данных
- Возврат данных в удобном формате (список кортежей)
- Интеграция с pandas для дальнейшего анализа

## Установка

```bash
pip install requests beautifulsoup4 pandas
```

## Использование

### Базовый пример

```python
from cbr_key_rate import fetch_full_key_rate_history
import pandas as pd

# Получение истории ключевой ставки
history = fetch_full_key_rate_history("17.09.2013", "15.10.2025")

# Преобразование в DataFrame
df = pd.DataFrame(history, columns=["Дата", "Ставка"])
print(df)

# Сохранение в CSV
df.to_csv("key_rate_history.csv", index=False, encoding="utf-8-sig")
```

### Получение данных за короткий период

```python
from cbr_key_rate import fetch_key_rate_range

# Получение данных за период до 30 дней
rates = fetch_key_rate_range("01.01.2024", "31.01.2024")
for date, rate in rates:
    print(f"{date}: {rate}%")
```

## API

### `fetch_key_rate_range(start_date: str, end_date: str)`

Получает ежедневные значения ключевой ставки за диапазон дат (макс. ~30 дней).

**Параметры:**
- `start_date`: Дата начала в формате 'DD.MM.YYYY'
- `end_date`: Дата окончания в формате 'DD.MM.YYYY'

**Возвращает:** Список кортежей `(date, rate)`

### `fetch_full_key_rate_history(start_date_str: str, end_date_str: str)`

Получает полную историю ключевой ставки с автоматической разбивкой на чанки.

**Параметры:**
- `start_date_str`: Дата начала в формате 'DD.MM.YYYY'
- `end_date_str`: Дата окончания в формате 'DD.MM.YYYY'

**Возвращает:** Отсортированный список уникальных кортежей `(date, rate)`

### `split_date_range(start, end, chunk_days=30)`

Генерирует список диапазонов по N дней.

**Параметры:**
- `start`: Дата начала диапазона (datetime)
- `end`: Дата окончания диапазона (datetime)
- `chunk_days`: Количество дней в одном чанке (по умолчанию 30)

**Возвращает:** Генератор кортежей `(chunk_start, chunk_end)`

## Тестирование

```bash
cd /workspace
python -m pytest tests/
```

Или запустить тесты напрямую:

```bash
python -m unittest tests.test_scraper
```

## Структура проекта

```
cbr_key_rate/
├── cbr_key_rate/
│   ├── __init__.py      # Экспорт основных функций
│   └── scraper.py       # Основная логика парсинга
├── tests/
│   └── test_scraper.py  # Юнит-тесты
├── README.md            # Документация
└── main                 # Пример использования (legacy)
```

## Лицензия

MIT
