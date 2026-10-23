"""
Модуль для парсинга данных о ключевой ставке с сайта ЦБ РФ.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Tuple, Generator


def fetch_key_rate_range(start_date: str, end_date: str) -> List[Tuple[datetime.date, float]]:
    """
    Получает ежедневные значения ключевой ставки за диапазон дат (макс. ~30 дней).
    
    Args:
        start_date: Дата начала в формате 'DD.MM.YYYY'
        end_date: Дата окончания в формате 'DD.MM.YYYY'
    
    Returns:
        Список кортежей (date, rate), где date - объект date, rate - float значение ставки
    """
    url = "https://cbr.ru/hd_base/KeyRate/"
    params = {
        "UniDbQuery.Posted": "True",
        "UniDbQuery.From": start_date,
        "UniDbQuery.To": end_date
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        return []

    rates = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 2:
            date_str = cells[0].get_text(strip=True)
            rate_str = cells[1].get_text(strip=True).replace('%', '').strip()
            try:
                date = datetime.strptime(date_str, "%d.%m.%Y").date()
                rate = float(rate_str.replace(',', '.'))
                rates.append((date, rate))
            except Exception:
                continue
    return rates


def split_date_range(start: datetime, end: datetime, chunk_days: int = 30) -> Generator[Tuple[datetime, datetime], None, None]:
    """
    Генерирует список диапазонов по N дней.
    
    Args:
        start: Дата начала диапазона
        end: Дата окончания диапазона
        chunk_days: Количество дней в одном чанке (по умолчанию 30)
    
    Yields:
        Кортежи (chunk_start, chunk_end) для каждого поддиапазона
    """
    current = start
    while current <= end:
        chunk_end = min(current + timedelta(days=chunk_days - 1), end)
        yield current, chunk_end
        current = chunk_end + timedelta(days=1)


def fetch_full_key_rate_history(start_date_str: str, end_date_str: str) -> List[Tuple[datetime.date, float]]:
    """
    Получает полную историю ключевой ставки с разбивкой на чанки.
    
    Args:
        start_date_str: Дата начала в формате 'DD.MM.YYYY'
        end_date_str: Дата окончания в формате 'DD.MM.YYYY'
    
    Returns:
        Отсортированный список уникальных кортежей (date, rate)
    """
    start = datetime.strptime(start_date_str, "%d.%m.%Y")
    end = datetime.strptime(end_date_str, "%d.%m.%Y")

    all_rates = []
    for chunk_start, chunk_end in split_date_range(start, end, chunk_days=30):
        s = chunk_start.strftime("%d.%m.%Y")
        e = chunk_end.strftime("%d.%m.%Y")
        print(f"Запрашиваю: {s} — {e}")
        chunk_rates = fetch_key_rate_range(s, e)
        all_rates.extend(chunk_rates)

    # Убираем дубликаты и сортируем
    all_rates = sorted(set(all_rates), key=lambda x: x[0])
    return all_rates
