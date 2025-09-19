# Run this script to train and save the iris model as iris_model.pkl
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/iris_model.pkl")
print("Model saved to models/iris_model.pkl")
