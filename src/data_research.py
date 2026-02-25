import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def run_research():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", "nabir-16-2020-2021-roki_03-12-2018.csv")
    output_dir = os.path.join(current_dir, "..", "reports", "figures")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(file_path):
        print("❌ Помилка: файл не знайдено.")
        return

    df = pd.read_csv(file_path, sep=';', encoding='cp1251')

    def clean_num(value):
        if isinstance(value, str):
            return float(value.replace(',', '.').replace(' ', '').replace('\xa0', ''))
        return value

    scenario_labels = ['Сценарій 1', 'Сценарій 2', 'Сценарій 3']
    scenario_cols = ['Прогноз 2021 сценарій 1', 'Прогноз 2021 сценарій 2', 'Прогноз 2021 сценарій 3']
    for col in scenario_cols:
        df[col] = df[col].apply(clean_num)

    sns.set_theme(style="whitegrid")

    print("=== АНАЛІЗ ГІПОТЕЗ ЗА ТЕХНІЧНИМ ЗАВДАННЯМ ===\n")

    gdp_nom = df[df['Показник'].str.contains('продукт', case=False, na=False) &
                 df['Показник'].str.contains('номінальний', case=False, na=False)]

    if not gdp_nom.empty:
        s2 = gdp_nom['Прогноз 2021 сценарій 2'].values[0]
        s3 = gdp_nom['Прогноз 2021 сценарій 3'].values[0]
        diff = s2 - s3
        print(f"1. Порівняння сценаріїв ВВП (Сц.2 vs Сц.3):")
        print(f"   - Різниця: {diff:,.2f} млн грн.\n")

        plt.figure(figsize=(10, 6))
        sns.barplot(x=scenario_labels, y=gdp_nom[scenario_cols].values[0], palette="Blues_d")
        plt.title('Прогноз номінального ВВП на 2021 рік')
        plt.savefig(os.path.join(output_dir, "gdp_research.png"))
    else:
        print("⚠️ Дані для 1-ї гіпотези (ВВП номінальний) не знайдено.\n")

    inflation = df[df['Показник'].str.contains('споживчих цін', case=False, na=False)]
    if not inflation.empty:
        print(f"2. Аналіз інфляційних очікувань (ІСЦ):")
        for col in scenario_cols:
            print(f"   - {col}: {inflation[col].values[0]}%")
        print()

        plt.figure(figsize=(10, 6))
        sns.lineplot(x=scenario_labels, y=inflation[scenario_cols].values[0], marker='o', color='red')
        plt.title('Індекс споживчих цін за сценаріями')
        plt.savefig(os.path.join(output_dir, "inflation_research.png"))
    else:
        print("⚠️ Дані для 2-ї гіпотези (Інфляція) не знайдено.\n")

    wage = df[df['Показник'].str.contains('заробітна плата', case=False, na=False)]
    if not wage.empty:
        print(f"3. Аналіз соціального добробуту (Прогноз зарплат на 2021):")
        w_row = wage.iloc[0]
        s2_wage = w_row['Прогноз 2021 сценарій 2']
        s3_wage = w_row['Прогноз 2021 сценарій 3']
        diff_wage = s2_wage - s3_wage
        print(f"   - Оптимістичний сценарій (Сц. 2): {s2_wage:,.0f} грн.")
        print(f"   - Песимістичний сценарій (Сц. 3): {s3_wage:,.0f} грн.")
        print(f"   - Різниця в добробуті: {diff_wage:,.0f} грн/міс.")

        plt.figure(figsize=(10, 6))
        sns.barplot(x=scenario_labels, y=wage[scenario_cols].values[0], palette="Greens_d")
        plt.title('Середня заробітна плата за сценаріями')
        plt.savefig(os.path.join(output_dir, "wage_research.png"))
    else:
        print("⚠️ Показник для соціальної гіпотези не знайдено.")

    plt.close('all')


if __name__ == "__main__":
    run_research()