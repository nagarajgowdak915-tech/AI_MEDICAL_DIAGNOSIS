
import pandas as pd
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
columns = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

data = pd.read_csv("diabetes.csv", header=None, names=columns)

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Model accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

# Explain the trained model with SHAP
scaler = model.named_steps["standardscaler"]
classifier = model.named_steps["logisticregression"]

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test),
    columns=X_test.columns,
    index=X_test.index
)

explainer = shap.LinearExplainer(classifier, scaler.transform(X_train))
shap_values = explainer(X_test_scaled)

# Show feature importance
plt.figure()
shap.plots.bar(shap_values, show=False)
plt.tight_layout()
plt.savefig("shap_feature_importance.png", dpi=200, bbox_inches="tight")
plt.show()

print("SHAP explanation completed.")
print("Feature importance chart saved as shap_feature_importance.png")
