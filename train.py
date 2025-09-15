# file: train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
import joblib

from features import featurize

LABEL_MAP = {"weak":0, "medium":1, "strong":2}

df = pd.read_csv("passwords_dataset.csv")
X = featurize(df)
y = df["label"].map(LABEL_MAP)

X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
    X, y, df, test_size=0.2, random_state=42, stratify=y
)

# tree-based model usually doesn't need scaling, but it doesn't hurt to keep pipeline simple here
model = GradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["weak","medium","strong"]))
print("confusion matrix:\n", confusion_matrix(y_test, y_pred))

# save artifacts
joblib.dump(model, "psm_model.joblib")
X_test.iloc[:5].to_csv("debug_sample_features.csv", index=False)
df_test.iloc[:5].to_csv("debug_sample_passwords.csv", index=False)
print("saved psm_model.joblib")
