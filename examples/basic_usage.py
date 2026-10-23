"""
Пример базового использования библиотеки cbr_key_rate.
Получение истории ключевой ставки ЦБ РФ.
"""

from cbr_key_rate import fetch_full_key_rate_history
import pandas as pd

if __name__ == "__main__":
    # Укажите нужный диапазон дат в формате DD.MM.YYYY
    start_date = "17.09.2013"
    end_date = "15.10.2025"

    print(f"Загрузка истории ключевой ставки с {start_date} по {end_date}...")
    
    # Получение данных
    history = fetch_full_key_rate_history(start_date, end_date)
    
    # Создание DataFrame
    df = pd.DataFrame(history, columns=["Дата", "Ставка"])
    
    # Вывод результатов
    print("\nПоследние 10 записей:")
    print(df.tail(10))
    
    print(f"\nВсего записей: {len(df)}")
    print(f"Диапазон дат: {df['Дата'].min()} — {df['Дата'].max()}")
    print(f"Минимальная ставка: {df['Ставка'].min()}%")
    print(f"Максимальная ставка: {df['Ставка'].max()}%")
    print(f"Средняя ставка: {df['Ставка'].mean():.2f}%")
    
    # Сохранение в CSV (опционально)
    output_file = "key_rate_history.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\nДанные сохранены в файл: {output_file}")
