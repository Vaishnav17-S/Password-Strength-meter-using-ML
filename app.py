# file: app.py
import streamlit as st
import joblib
import pandas as pd
from features import featurize
from utils import base_score, strength_label, suggestions

st.set_page_config(page_title="Password Strength Meter (ML)")

@st.cache_resource
def load_model():
    return joblib.load("psm_model.joblib")

model = load_model()
LABEL_INV = {0:"weak", 1:"medium", 2:"strong"}

st.title("🔐 Password Strength Meter — ML + Heuristics")
st.write("Type a password to see the predicted strength, probabilities, and targeted suggestions.")

pw = st.text_input("Password", type="password", value="")

if pw:
    df = pd.DataFrame({"password":[pw]})
    X = featurize(df)
    proba = model.predict_proba(X)[0]
    pred_class = int(proba.argmax())

    score = base_score(pw)
    bucket = strength_label(score)
    tips = suggestions(pw)

    st.subheader("Result")
    st.metric("Model prediction", LABEL_INV[pred_class])
    st.write(f"**Probabilities:** Weak: {proba[0]:.2f} | Medium: {proba[1]:.2f} | Strong: {proba[2]:.2f}")
    st.progress(score/100.0, text=f"Heuristic score: {score}/100 ({bucket})")

    st.subheader("Suggestions")
    for t in tips:
        st.markdown(f"- {t}")

    st.caption("Note: This demo combines a trained classifier with a heuristic score for interpretability.")

st.divider()
st.write("**Tip:** Use a long passphrase (12–16+), mix character types, avoid common words, repeats, and sequences.")
