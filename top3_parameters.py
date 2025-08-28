import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

# Wczytanie danych z GitHub
url = "https://raw.githubusercontent.com/slastrzelec/HAppY_pro/main/WHR25_Data_Figure_2.1.xlsx"
df = pd.read_excel(url)

# Wybieramy tylko kolumny numeryczne i usuwamy nieistotne
cols_to_drop = ['Year', 'upperwhisker', 'lowerwhisker']
df_num = df.select_dtypes(include='number').drop(columns=cols_to_drop, errors='ignore')

# Obsługa brakujących wartości - wypełniamy średnią kolumny
df_num = df_num.fillna(df_num.mean())

# Oddzielamy cechy od targetu
X = df_num.drop(columns=['Ladder score'])
y = df_num['Ladder score']

# ===============================
# 1. Correlation Analysis
# ===============================
print("=== Correlation Analysis ===")
correlations = X.corrwith(y)
top3_corr = correlations.abs().sort_values(ascending=False).head(3)
for param in top3_corr.index:
    print(f"{param}: correlation = {correlations[param]:.3f}")

# ===============================
# 2. Linear Regression Analysis
# ===============================
print("\n=== Linear Regression Analysis ===")
lin_reg = LinearRegression()
lin_reg.fit(X, y)
coefs = pd.Series(lin_reg.coef_, index=X.columns)
top3_linreg = coefs.abs().sort_values(ascending=False).head(3)
for param in top3_linreg.index:
    print(f"{param}: coefficient = {coefs[param]:.3f}")

# ===============================
# 3. Neural Network Analysis (MLP)
# ===============================
print("\n=== Neural Network Analysis (MLP) ===")
# Standaryzacja danych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

mlp = MLPRegressor(hidden_layer_sizes=(50,), max_iter=2000, random_state=42)
mlp.fit(X_scaled, y)

# Permutation importance
perm_importance = permutation_importance(mlp, X_scaled, y, n_repeats=10, random_state=42)
perm_series = pd.Series(perm_importance.importances_mean, index=X.columns)
top3_mlp = perm_series.sort_values(ascending=False).head(3)

for param in top3_mlp.index:
    print(f"{param}: importance = {perm_series[param]:.3f}")
