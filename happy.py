import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Wczytanie pliku Excel z GitHub
url = "https://raw.githubusercontent.com/slastrzelec/HAppY_pro/main/WHR25_Data_Figure_2.1.xlsx"
df = pd.read_excel(url)

# Wybieramy tylko kolumny numeryczne i usuwamy kolumny niechciane
cols_to_drop = ['upperwhisker', 'lowerwhisker', 'Year']
df_num = df.select_dtypes(include='number').drop(columns=cols_to_drop, errors='ignore')

# Wyświetlenie kolumn numerycznych
print(df_num.columns)

# Heatmapa korelacji tylko dla liczb
plt.figure(figsize=(12,10))
sns.heatmap(df_num.corr(), annot=True, fmt=".2f", cmap="viridis")
plt.title("Heatmapa korelacji (bez kolumn Year i whisker) - aktualizacja 28.08")
plt.xlabel("Kolumny")
plt.ylabel("Kolumny")
plt.show()
