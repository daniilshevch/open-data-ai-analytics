import pandas as pd
import os
from sqlalchemy import create_engine

def run_research():
    db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    engine = create_engine(db_url)

    try:
        df = pd.read_sql("SELECT * FROM raw_data", con=engine)
        print("✅ Дані отримано з MySQL для розрахунків.")

        def clean_num(value):
            if isinstance(value, str):
                return float(value.replace(',', '.').replace(' ', '').replace('\xa0', ''))
            return value

        scenario_cols = ['Прогноз 2021 сценарій 1', 'Прогноз 2021 сценарій 2', 'Прогноз 2021 сценарій 3']
        for col in scenario_cols:
            df[col] = df[col].apply(clean_num)

        print("=== ВИКОНАННЯ РОЗРАХУНКІВ ДЛЯ ГІПОТЕЗ ===\n")

        processed_data = []

        gdp_nom = df[df['Показник'].str.contains('продукт', case=False, na=False) &
                     df['Показник'].str.contains('номінальний', case=False, na=False)]
        if not gdp_nom.empty:
            row = gdp_nom.iloc[0]
            diff = row['Прогноз 2021 сценарій 2'] - row['Прогноз 2021 сценарій 3']
            print(f"1. Різниця ВВП (Сц.2 - Сц.3): {diff:,.2f}")
            gdp_row = row.copy()
            gdp_row['research_category'] = 'gdp'
            gdp_row['calculated_diff'] = diff
            processed_data.append(gdp_row)

        inflation = df[df['Показник'].str.contains('споживчих цін', case=False, na=False)]
        if not inflation.empty:
            inf_row = inflation.iloc[0].copy()
            inf_row['research_category'] = 'inflation'
            inf_row['calculated_diff'] = 0
            processed_data.append(inf_row)

        wage = df[df['Показник'].str.contains('заробітна плата', case=False, na=False)]
        if not wage.empty:
            w_row = wage.iloc[0]
            diff_wage = w_row['Прогноз 2021 сценарій 2'] - w_row['Прогноз 2021 сценарій 3']
            print(f"3. Різниця в зарплатах: {diff_wage:,.0f} грн.")
            wage_res = w_row.copy()
            wage_res['research_category'] = 'wage'
            wage_res['calculated_diff'] = diff_wage
            processed_data.append(wage_res)

        df_final = pd.DataFrame(processed_data)
        df_final.to_sql('research_results', con=engine, if_exists='replace', index=False)
        print("\n✅ Всі розрахунки збережено в таблицю 'research_results'.")

    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    run_research()