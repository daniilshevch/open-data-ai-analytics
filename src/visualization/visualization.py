import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def create_visualizations():
    db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    engine = create_engine(db_url)

    output_dir = "/app/reports/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        df = pd.read_sql("SELECT * FROM research_results", con=engine)
        sns.set_theme(style="whitegrid")
        scenario_labels = ['Сценарій 1', 'Сценарій 2', 'Сценарій 3']
        scenario_cols = ['Прогноз 2021 сценарій 1', 'Прогноз 2021 сценарій 2', 'Прогноз 2021 сценарій 3']

        gdp_data = df[df['research_category'] == 'gdp']
        if not gdp_data.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=scenario_labels, y=gdp_data[scenario_cols].values[0], palette="Blues_d")
            plt.title('Прогноз номінального ВВП на 2021 рік (з БД)')
            plt.savefig(os.path.join(output_dir, "gdp_research.png"))

        inf_data = df[df['research_category'] == 'inflation']
        if not inf_data.empty:
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=scenario_labels, y=inf_data[scenario_cols].values[0], marker='o', color='red')
            plt.title('Індекс споживчих цін (з БД)')
            plt.savefig(os.path.join(output_dir, "inflation_research.png"))

        wage_data = df[df['research_category'] == 'wage']
        if not wage_data.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=scenario_labels, y=wage_data[scenario_cols].values[0], palette="Greens_d")
            plt.title('Середня заробітна плата (з БД)')
            plt.savefig(os.path.join(output_dir, "wage_research.png"))

        print(f"✅ Всі графіки згенеровано та збережено в {output_dir}")

    except Exception as e:
        print(f"❌ Помилка візуалізації: {e}")
    finally:
        plt.close('all')


if __name__ == "__main__":
    create_visualizations()