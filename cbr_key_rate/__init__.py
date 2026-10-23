"""
CBR Key Rate - библиотека для получения истории ключевой ставки ЦБ РФ.

Этот пакет предоставляет инструменты для скачивания, обработки и анализа
ежедневных значений ключевой ставки Центрального банка Российской Федерации.
"""

__version__ = "0.1.0"
__author__ = "CBR Key Rate Contributors"

from .scraper import (
    fetch_key_rate_range,
    fetch_full_key_rate_history,
    split_date_range,
)

__all__ = [
    "fetch_key_rate_range",
    "fetch_full_key_rate_history",
    "split_date_range",
    "__version__",
]
