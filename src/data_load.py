import pandas as pd
import os

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", "nabir-16-2020-2021-roki_03-12-2018.csv")
    print(f"🔍 Шукаю файл за шляхом: {os.path.abspath(file_path)}")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';', encoding='cp1251')
        print("✅ Дані успішно завантажено!")
        print(df.head())
        return df
    else:
        print("❌ Файл не знайдено!")
        print(f"Переконайся, що файл лежить тут: {os.path.abspath(file_path)}")
        return None


if __name__ == "__main__":
    load_data()