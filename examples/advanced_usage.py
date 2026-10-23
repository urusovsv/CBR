"""
Пример расширенного использования библиотеки cbr_key_rate.
Анализ изменений ключевой ставки и визуализация.
"""

from cbr_key_rate import fetch_full_key_rate_history
import pandas as pd
import matplotlib.pyplot as plt

def analyze_rate_changes(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет анализ изменений ставки."""
    df = df.copy()
    df['Изменение'] = df['Ставка'].diff()
    df['Изменение_абс'] = df['Изменение'].abs()
    return df

if __name__ == "__main__":
    # Получение данных за весь доступный период
    start_date = "17.09.2013"
    end_date = "15.10.2025"

    print(f"Загрузка данных с {start_date} по {end_date}...")
    history = fetch_full_key_rate_history(start_date, end_date)
    
    df = pd.DataFrame(history, columns=["Дата", "Ставка"])
    df = analyze_rate_changes(df)
    
    # Статистика изменений
    changes = df[df['Изменение'].notna()]
    if len(changes) > 0:
        print("\n=== Статистика изменений ставки ===")
        print(f"Количество изменений: {len(changes)}")
        print(f"Повышений: {(changes['Изменение'] > 0).sum()}")
        print(f"Понижений: {(changes['Изменение'] < 0).sum()}")
        print(f"Без изменений: {(changes['Изменение'] == 0).sum()}")
        print(f"Среднее изменение: {changes['Изменение'].mean():.3f}%")
        print(f"Максимальное повышение: {changes['Изменение'].max():.3f}%")
        print(f"Максимальное понижение: {changes['Изменение'].min():.3f}%")
    
    # Визуализация
    plt.figure(figsize=(14, 6))
    plt.plot(df['Дата'], df['Ставка'], linewidth=2, label='Ключевая ставка')
    plt.xlabel('Дата')
    plt.ylabel('Ставка, %')
    plt.title('Динамика ключевой ставки ЦБ РФ')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_plot = "key_rate_chart.png"
    plt.savefig(output_plot, dpi=300)
    print(f"\nГрафик сохранён: {output_plot}")
    
    # Сохранение полных данных
    output_csv = "key_rate_history_extended.csv"
    df.to_csv(output_csv, index=False, encoding="utf-8-sig", date_format='%d.%m.%Y')
    print(f"Данные сохранены: {output_csv}")
    
    print("\n=== Последние 5 записей ===")
    print(df.tail(5).to_string(index=False))
