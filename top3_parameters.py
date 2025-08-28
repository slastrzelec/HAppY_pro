import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# ===============================
# 1. Load dataset
# ===============================
url = "https://raw.githubusercontent.com/slastrzelec/HAppY_pro/main/WHR25_Data_Figure_2.1.xlsx"
df = pd.read_excel(url)

# Remove irrelevant columns and keep only numerical ones
cols_to_drop = ['Year', 'upperwhisker', 'lowerwhisker']
df_num = df.select_dtypes(include='number').drop(columns=cols_to_drop, errors='ignore')

# Fill missing values with column means
df_num = df_num.fillna(df_num.mean())

# Split features and target
X = df_num.drop(columns=['Ladder score'])
y = df_num['Ladder score']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===============================
# 2. Correlation Analysis
# ===============================
correlations = X.corrwith(y)
top3_corr = correlations.abs().sort_values(ascending=False).head(3)
corr_results = pd.DataFrame({
    "Parameter": top3_corr.index,
    "Correlation": [correlations[param] for param in top3_corr.index]
})

print("=== Correlation Analysis ===")
print(corr_results, "\n")

# ===============================
# 3. Linear Regression Analysis
# ===============================
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
coefs = pd.Series(lin_reg.coef_, index=X.columns)
top3_linreg = coefs.abs().sort_values(ascending=False).head(3)

linreg_results = pd.DataFrame({
    "Parameter": top3_linreg.index,
    "Coefficient": [coefs[param] for param in top3_linreg.index]
})

print("=== Linear Regression Analysis ===")
print(linreg_results, "\n")

# ===============================
# 4. Neural Network Analysis (MLP)
# ===============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

mlp = MLPRegressor(hidden_layer_sizes=(50,),
                   max_iter=5000,
                   random_state=42,
                   early_stopping=True,
                   n_iter_no_change=20,
                   validation_fraction=0.1)

mlp.fit(X_train_scaled, y_train)

# Permutation importance
perm_importance = permutation_importance(mlp, X_test_scaled, y_test, n_repeats=10, random_state=42)
perm_series = pd.Series(perm_importance.importances_mean, index=X.columns)
top3_mlp = perm_series.sort_values(ascending=False).head(3)

mlp_results = pd.DataFrame({
    "Parameter": top3_mlp.index,
    "Importance": [perm_series[param] for param in top3_mlp.index]
})

print("=== Neural Network Analysis (MLP) ===")
print(mlp_results, "\n")

# ===============================
# 5. Neural Network Training Curve
# ===============================
plt.figure(figsize=(8, 5))
plt.plot(mlp.loss_curve_, marker="o")
plt.title("Neural Network Training Loss Curve")
plt.xlabel("Iterations")
plt.ylabel("Loss")
plt.grid(True)
plt.show()

# ===============================
# 6. Final Summary with Pie Charts
# ===============================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Correlation Pie
axes[0].pie(corr_results["Correlation"].abs(),
            labels=corr_results["Parameter"],
            autopct='%1.1f%%',
            startangle=90)
axes[0].set_title("Top 3 Correlated Features")

# Linear Regression Pie
axes[1].pie(linreg_results["Coefficient"].abs(),
            labels=linreg_results["Parameter"],
            autopct='%1.1f%%',
            startangle=90)
axes[1].set_title("Top 3 Linear Regression Features")

# MLP Pie
axes[2].pie(mlp_results["Importance"].abs(),
            labels=mlp_results["Parameter"],
            autopct='%1.1f%%',
            startangle=90)
axes[2].set_title("Top 3 Neural Network Features")

plt.tight_layout()
plt.show()
