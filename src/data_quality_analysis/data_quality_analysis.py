import pandas as pd
import os
from sqlalchemy import create_engine


def check_data_quality():
    db_user = os.getenv("MYSQL_USER", "user")
    db_password = os.getenv("MYSQL_PASSWORD", "password")
    db_host = os.getenv("MYSQL_HOST", "db")
    db_name = os.getenv("MYSQL_DATABASE", "analytics_db")

    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

    print("=== ЗВІТ ПРО ЯКІСТЬ ДАНИХ (БАЗА ДАНИХ) ===")

    try:
        query = "SELECT * FROM raw_data"
        df = pd.read_sql(query, con=engine)

        print("✅ Дані успішно отримано з MySQL для аналізу.")

        print("\n1. Кількість порожніх значень (NaN):")
        print(df.isnull().sum())

        print("\n2. Типи даних по стовпцях (визначені БД):")
        print(df.dtypes)

        print(f"\n3. Виявлено повних дублікатів рядків: {df.duplicated().sum()}")

    except Exception as e:
        print(f"❌ Помилка при читанні з БД: {e}")
        print("Підказка: переконайтеся, що контейнер data_load вже відпрацював.")


if __name__ == "__main__":
    check_data_quality()