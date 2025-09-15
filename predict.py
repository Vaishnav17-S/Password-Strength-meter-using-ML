# file: predict.py
import joblib
import pandas as pd
from features import featurize
from utils import base_score, strength_label, suggestions

LABEL_INV = {0:"weak", 1:"medium", 2:"strong"}

model = joblib.load("psm_model.joblib")

def classify_password(pw: str):
    df = pd.DataFrame({"password":[pw]})
    X = featurize(df)
    proba = model.predict_proba(X)[0]
    pred_class = int(proba.argmax())
    score = base_score(pw)
    return {
        "password": pw,
        "predicted_label": LABEL_INV[pred_class],
        "probabilities": {"weak":float(proba[0]),"medium":float(proba[1]),"strong":float(proba[2])},
        "heuristic_score_0_100": score,
        "heuristic_bucket": strength_label(score),
        "suggestions": suggestions(pw)
    }

if __name__ == "__main__":
    while True:
        try:
            pw = input("Enter a password (or 'exit'): ").strip()
            if pw.lower() == "exit": break
            res = classify_password(pw)
            print("\n== Result ==")
            print(f"Predicted: {res['predicted_label']}  | probs {res['probabilities']}")
            print(f"Heuristic score: {res['heuristic_score_0_100']} ({res['heuristic_bucket']})")
            print("Suggestions:")
            for s in res["suggestions"]:
                print(f" - {s}")
            print()
        except KeyboardInterrupt:
            break
