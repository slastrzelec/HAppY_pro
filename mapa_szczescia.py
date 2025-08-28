import pandas as pd
import plotly.express as px

# Wczytanie pliku Excel z GitHub
url = "https://raw.githubusercontent.com/slastrzelec/HAppY_pro/main/WHR25_Data_Figure_2.1.xlsx"
df = pd.read_excel(url)

# Sprawdzenie kolumn
print(df.columns)

# Interaktywna mapa świata
fig = px.choropleth(
    df,
    locations="Country name",        # poprawiona nazwa kolumny
    locationmode="country names",
    color="Ladder score",           # poziom szczęścia
    hover_name="Country name",      # poprawiona nazwa kolumny
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Poziom szczęścia w różnych krajach"
)

# Wyświetlenie mapy
fig.show()
