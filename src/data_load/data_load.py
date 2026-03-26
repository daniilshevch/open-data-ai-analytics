import pandas as pd
import os
from sqlalchemy import create_engine


def load_data_to_mysql():
    db_user = os.getenv("MYSQL_USER", "user")
    db_password = os.getenv("MYSQL_PASSWORD", "password")
    db_host = os.getenv("MYSQL_HOST", "db")
    db_name = os.getenv("MYSQL_DATABASE", "analytics_db")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "..", "data", "nabir-16-2020-2021-roki_03-12-2018.csv")

    if not os.path.exists(file_path):
        print("❌ Файл CSV не знайдено!")
        return

    df = pd.read_csv(file_path, sep=';', encoding='cp1251')

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

    try:
        df.to_sql('raw_data', con=engine, if_exists='replace', index=False)
        print("✅ Дані успішно імпортовано в MySQL таблицю 'raw_data'!")
    except Exception as e:
        print(f"❌ Помилка при записі в БД: {e}")


if __name__ == "__main__":
    load_data_to_mysql()