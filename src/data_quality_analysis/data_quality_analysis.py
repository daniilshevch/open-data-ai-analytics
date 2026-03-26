import pandas as pd
import os

def check_data_quality():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", "nabir-16-2020-2021-roki_03-12-2018.csv")

    if not os.path.exists(file_path):
        print("❌ Файл не знайдено для аналізу якості!")
        return

    df = pd.read_csv(file_path, sep=';', encoding='cp1251')

    print("=== ЗВІТ ПРО ЯКІСТЬ ДАНИХ ===")

    print("\n1. Кількість порожніх значень (NaN):")
    print(df.isnull().sum())

    print("\n2. Типи даних по стовпцях:")
    print(df.dtypes)

    print(f"\n3. Виявлено повних дублікатів рядків: {df.duplicated().sum()}")


if __name__ == "__main__":
    check_data_quality()