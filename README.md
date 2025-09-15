
# 🔐 Password Strength Meter using Machine Learning

A project that predicts password strength (**Weak / Medium / Strong**) and provides actionable suggestions.  
It combines a **heuristic scoring engine (0–100)** with a **Gradient Boosting Classifier** trained on synthetic password datasets.

---

## 🚀 Features

- Synthetic dataset generator for weak, medium, and strong passwords
- ~20 interpretable features (length, diversity, entropy, sequences, repeats, dictionary hits, etc.)
- Supervised ML classifier (Gradient Boosting)
- Heuristic score (0–100) + human-readable suggestions
- CLI demo for quick testing
- Optional Streamlit app with password strength bar + tips
- Results: confusion matrix, feature importance, metrics

---

## 📂 Project Structure

password-strength-ml/
│── app.py                 # Streamlit frontend (interactive strength meter)
│── predict.py             # CLI password strength checker
│── train.py               # Train Gradient Boosting model
│── make_dataset.py        # Generate synthetic dataset (weak/medium/strong)
│── features.py            # Feature engineering (~20 password features)
│── utils.py               # Heuristic scoring, penalties, suggestions
│── psm_model.joblib       # Trained ML model (saved after training)
│── passwords_dataset.csv  # Generated dataset of passwords + labels
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation




## ⚙️ Installation

```bash
# create and activate venv
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# install dependencies
pip install --upgrade pip
pip install numpy pandas scikit-learn matplotlib streamlit
🏗️ Usage
1. Generate dataset
bash
python make_dataset.py
2. Train model
bash
python train.py
This will output metrics and save psm_model.joblib.

3. CLI Demo
bash
python predict.py
Example:

objective

Enter a password: Tr@ins_Bridge#49
Predicted: strong  | probs weak=0.02 medium=0.18 strong=0.80
Heuristic score: 88 (strong)
Suggestions:
 - Great! Keep it long and unique. Consider a passphrase with 3–4 random words.
4. Streamlit App
bash
Copy code
streamlit run app.py
Opens a browser UI with password input, strength bar, and suggestions.

📊 Flow Diagram
mermaid
Copy code
flowchart LR
    A[Generate synthetic passwords] --> B[Heuristic scoring (0–100)]
    B --> C[Label mapping (weak/medium/strong)]
    C --> D[Feature engineering (~20 features)]
    D --> E[Train Gradient Boosting]
    E --> F[Evaluate & Save model]
    F --> G[Inference: password → features → predict]
    G --> H[Combine with heuristic score + tips]
📈 Results
Model: Gradient Boosting Classifier

Dataset: ~12k synthetic passwords

Accuracy: ~90% (varies per run)

📖 References (After 2021)
[1] D. Wang, X. Shan, Q. Dong, Y. Shen, and C. Jia, “No Single Silver Bullet: Measuring the Accuracy of Password Strength Meters,” USENIX Security Symposium, 2023.
[2] V. V. Belikov and I. A. Prokuronov, “Password Strength Verification Based on Machine Learning Algorithms and LSTM Recurrent Neural Networks,” Russian Technological Journal, vol. 11, no. 4, pp. 7-15, 2023.
[3] B. L. T. Thai and H. Tanaka, “A Statistical Markov-based Password Strength Meter,” Internet of Things, vol. 25, Article 101057, 2024.
