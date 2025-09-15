# file: features.py
import re
import numpy as np
import pandas as pd
from utils import SYMBOLS, has_sequence, has_repeats, dictionary_hits, est_bits, charset_size

def char_stats(pw):
    lowers = sum(c.islower() for c in pw)
    uppers = sum(c.isupper() for c in pw)
    digits = sum(c.isdigit() for c in pw)
    symbols = sum(c in SYMBOLS for c in pw)
    return lowers, uppers, digits, symbols

def ratio(x, L): return (x / L) if L else 0

def extract_features(pw: str) -> dict:
    L = len(pw)
    lowers, uppers, digits, symbols = char_stats(pw)
    diversity = sum(int(x > 0) for x in [lowers, uppers, digits, symbols])

    feats = {
        "len": L,
        "lower_cnt": lowers,
        "upper_cnt": uppers,
        "digit_cnt": digits,
        "symbol_cnt": symbols,
        "lower_ratio": ratio(lowers, L),
        "upper_ratio": ratio(uppers, L),
        "digit_ratio": ratio(digits, L),
        "symbol_ratio": ratio(symbols, L),
        "diversity_classes": diversity,
        "has_sequence": int(has_sequence(pw)),
        "has_repeats": int(has_repeats(pw)),
        "is_numeric_only": int(re.fullmatch(r"\d+", pw) is not None),
        "has_dictionary_word": int(dictionary_hits(pw)),
        "charset_size": charset_size(pw),
        "est_bits": est_bits(pw),
        "ends_with_year": int(re.search(r"(19|20)\d{2}$", pw) is not None),
        "has_year_anywhere": int(re.search(r"(19|20)\d{2}", pw) is not None),
        "has_common_suffix123": int(pw.lower().endswith("123")),
        "has_titlecase": int(pw[0].isupper()) if L else 0,
    }
    return feats

def featurize(df: pd.DataFrame) -> pd.DataFrame:
    rows = [extract_features(p) for p in df["password"].astype(str)]
    X = pd.DataFrame(rows)
    return X
