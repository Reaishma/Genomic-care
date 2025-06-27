import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Generate random genetic data with increased sample size
np.random.seed(42)
data = pd.DataFrame({
    'Gene1': np.random.rand(1000),
    'Gene2': np.random.rand(1000),
    'Gene3': np.random.rand(1000),
    'disease_status': np.random.randint(0, 2, 1000)
})

# Calculate statistical features
data['mean'] = data[['Gene1', 'Gene2', 'Gene3']].mean(axis=1)
data['std'] = data[['Gene1', 'Gene2', 'Gene3']].std(axis=1)
data['var'] = data[['Gene1', 'Gene2', 'Gene3']].var(axis=1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop('disease_status', axis=1), data['disease_status'], test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled[:, :3])
X_test_pca = pca.transform(X_test_scaled[:, :3])

# Add statistical features to the PCA data
X_train_pca = np.concatenate((X_train_pca, X_train_scaled[:, 3:]), axis=1)
X_test_pca = np.concatenate((X_test_pca, X_test_scaled[:, 3:]), axis=1)

# Random Forest Hyperparameter Tuning
rf_model = RandomForestClassifier(random_state=42)
param_grid_rf = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10]
}
grid_search_rf = GridSearchCV(rf_model, param_grid_rf, cv=5)
grid_search_rf.fit(X_train_pca, y_train)
print(f'Best Parameters for Random Forest: {grid_search_rf.best_params_}')
y_pred_rf = grid_search_rf.best_estimator_.predict(X_test_pca)
print(f'Random Forest Accuracy: {accuracy_score(y_test, y_pred_rf):.3f}')

# Gradient Boosting Hyperparameter Tuning
gb_model = GradientBoostingClassifier(random_state=42)
param_grid_gb = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.1, 0.05, 0.01],
    'max_depth': [3, 5, 10]
}
grid_search_gb = GridSearchCV(gb_model, param_grid_gb, cv=5)
grid_search_gb.fit(X_train_pca, y_train)
print(f'Best Parameters for Gradient Boosting: {grid_search_gb.best_params_}')
y_pred_gb = grid_search_gb.best_estimator_.predict(X_test_pca)
print(f'Gradient Boosting Accuracy: {accuracy_score(y_test, y_pred_gb):.3f}')
