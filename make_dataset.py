# file: make_dataset.py
import random
import string
import pandas as pd
from utils import base_score, strength_label

random.seed(42)

COMMON_PATTERNS = [
    "password","password1","admin123","welcome","iloveyou","qwerty","qwerty123",
    "abc123","hello123","india123","ganesh123","krishna108","omnamahshivay",
    "letmein","dragon","football","sunshine","shadow","master","killer","secret",
    "mobile123","google123","apple123","samsung123"
]

def gen_weak(n=8000):
    out = []
    # simple words, dates, repeats, numeric-only
    for _ in range(n//4):
        out.append(random.choice(COMMON_PATTERNS))
    for _ in range(n//4):
        year = random.choice(range(1980, 2026))
        out.append(f"{random.choice(['india','love','admin','user'])}{year}")
    for _ in range(n//4):
        ch = random.choice(string.ascii_lowercase + string.digits)
        out.append(ch * random.choice([4,5,6,7,8]))
    for _ in range(n - 3*(n//4)):
        L = random.choice([4,5,6,7])
        out.append("".join(random.choices(string.digits, k=L)))
    return out

def gen_mixed(n=8000):
    out = []
    charset = string.ascii_letters + string.digits
    for _ in range(n):
        L = random.choice(range(8, 13))
        pw = "".join(random.choices(charset, k=L))
        # sometimes append a symbol
        if random.random() < 0.4:
            pw += random.choice("!@#$%^&*")
        out.append(pw)
    return out

def gen_strong(n=8000):
    out = []
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()_+-=[]{};':,.<>/?\\|`~"
    for _ in range(n):
        L = random.choice(range(12, 21))
        pw = "".join(random.choices(charset, k=L))
        out.append(pw)
    return out

def build_df(n_each=8000):
    data = gen_weak(n_each) + gen_mixed(n_each) + gen_strong(n_each)
    scores = [base_score(p) for p in data]
    labels = [strength_label(s) for s in scores]
    return pd.DataFrame({"password": data, "score": scores, "label": labels})

if __name__ == "__main__":
    df = build_df(7000)  # ~21k rows
    df.to_csv("passwords_dataset.csv", index=False)
    print(df.label.value_counts())
    print("saved passwords_dataset.csv")
