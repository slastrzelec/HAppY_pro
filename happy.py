import pandas as pd

url = "https://raw.githubusercontent.com/slastrzelec/HAppY_pro/main/WHR25_Data_Figure_2.1.xlsx"
df = pd.read_excel(url)
print(df.head())
