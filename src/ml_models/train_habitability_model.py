import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib
import os
from utils.db import get_engine

# --- CONFIG ---
FEATURES = [
	"planet_radius",
	"planet_mass",
	"planet_density",
	"equilibrium_temperature",
	"stellar_temperature",
	"stellar_mass",
	"stellar_radius"
]
TARGET = "habitability_index"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "habitability_model.pkl")

# --- DATA LOADING ---
def load_data():
	engine = get_engine()
	query = f"""
		SELECT {', '.join(FEATURES)}, {TARGET}
		FROM exoplanet_data.planets
	"""
	df = pd.read_sql(query, engine)
	return df

# --- OUTLIER REMOVAL ---
def remove_outliers_iqr(df, features):
	filtered = df.copy()
	for col in features:
		Q1 = filtered[col].quantile(0.25)
		Q3 = filtered[col].quantile(0.75)
		IQR = Q3 - Q1
		lower = Q1 - 1.5 * IQR
		upper = Q3 + 1.5 * IQR
		filtered = filtered[(filtered[col] >= lower) & (filtered[col] <= upper)]
	return filtered

# --- MAIN PIPELINE ---
def main():
	# Load and clean data
	df = load_data()
	df = df.dropna(subset=[TARGET])
	df = remove_outliers_iqr(df, FEATURES)
	X = df[FEATURES]
	y = df[TARGET].values.reshape(-1, 1)

	# Impute missing values
	imputer = SimpleImputer(strategy="median")
	X_imputed = imputer.fit_transform(X)

	# Normalize target to [0,1]
	scaler_y = MinMaxScaler()
	y_scaled = scaler_y.fit_transform(y).ravel()

	# Train/test split
	X_train, X_test, y_train, y_test = train_test_split(
		X_imputed, y_scaled, test_size=0.2, random_state=42
	)

	# Pipeline: imputer (for future missing) + regressor
	pipeline = Pipeline([
		("imputer", SimpleImputer(strategy="median")),
		("regressor", RandomForestRegressor(random_state=42))
	])

	# Grid search
	param_grid = {
		"regressor__n_estimators": [200, 400, 600],
		"regressor__max_depth": [10, 20, None],
		"regressor__min_samples_split": [2, 5, 10],
		"regressor__min_samples_leaf": [1, 2, 4]
	}
	grid = GridSearchCV(
		pipeline,
		param_grid,
		cv=5,
		scoring="r2",
		n_jobs=-1,
		verbose=2
	)
	grid.fit(X_train, y_train)

	# Evaluation
	y_pred = grid.predict(X_test)
	r2 = r2_score(y_test, y_pred)
	rmse = np.sqrt(mean_squared_error(y_test, y_pred))
	mae = mean_absolute_error(y_test, y_pred)
	print(f"R2 score: {r2:.4f}")
	print(f"RMSE: {rmse:.4f}")
	print(f"MAE: {mae:.4f}")

	# Cross-validation on full data
	cv_scores = cross_val_score(grid.best_estimator_, X_imputed, y_scaled, cv=5, scoring="r2")
	print(f"5-fold CV R2: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

	# Feature importance
	best_rf = grid.best_estimator_.named_steps["regressor"]
	importances = best_rf.feature_importances_
	indices = np.argsort(importances)[::-1]
	plt.figure(figsize=(8, 5))
	plt.title("Feature Importances")
	plt.bar(range(len(FEATURES)), importances[indices], align="center")
	plt.xticks(range(len(FEATURES)), [FEATURES[i] for i in indices], rotation=30)
	plt.tight_layout()
	plt.show()

	# Save pipeline (with scaler for y)
	full_pipeline = Pipeline([
		("imputer", SimpleImputer(strategy="median")),
		("regressor", grid.best_estimator_.named_steps["regressor"])
	])
	# Save scaler for y as attribute
	full_pipeline.y_scaler = scaler_y
	joblib.dump(full_pipeline, MODEL_PATH)
	print(f"Model pipeline saved to {MODEL_PATH}")

if __name__ == "__main__":
	main()