# file: utils.py
import re
import math
from functools import lru_cache

# minimal common dictionary (expand if you like: colors, animals, sports, etc.)
COMMON_WORDS = {
    "password","admin","welcome","login","user","test","guest","love","secret",
    "qwerty","abc","abcd","abc123","iloveyou","letmein","monkey","dragon","football",
    "baseball","star","sun","india","bharat","krishna","ganesh","om","jay","mobile",
    "hello","world","prime","king","queen","money","google","apple","samsung",
    "shadow","master","killer","freedom","hacker","flower","tiger","lion","super","cool"
}

KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]

SYMBOLS = r"!@#$%^&*()_+\-=\[\]{};':\",.<>/?\\|`~"

def has_sequence(pw, min_run=4):
    s = pw.lower()
    # alphabetic ascending runs
    for i in range(len(s) - min_run + 1):
        run = s[i:i+min_run]
        asc = "".join(chr(ord(run[0]) + k) for k in range(min_run))
        if run == asc:
            return True
    # numeric ascending runs
    if any(seq in s for seq in ["0123","1234","2345","3456","4567","5678","6789"]):
        return True
    # keyboard row runs
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - min_run + 1):
            if row[i:i+min_run] in s:
                return True
    return False

def has_repeats(pw, min_repeat=3):
    # repeated same char like aaaa or 111
    return re.search(r"(.)\1{" + str(min_repeat-1) + r",}", pw) is not None

def count_classes(pw):
    lowers = sum(c.islower() for c in pw)
    uppers = sum(c.isupper() for c in pw)
    digits = sum(c.isdigit() for c in pw)
    symbols = sum(c in SYMBOLS for c in pw)
    return lowers, uppers, digits, symbols

def dictionary_hits(pw):
    s = pw.lower()
    return any(w in s for w in COMMON_WORDS)

def charset_size(pw):
    size = 0
    has_low = any(c.islower() for c in pw)
    has_up  = any(c.isupper() for c in pw)
    has_dig = any(c.isdigit() for c in pw)
    has_sym = any(c in SYMBOLS for c in pw)
    if has_low: size += 26
    if has_up:  size += 26
    if has_dig: size += 10
    if has_sym: size += len(set(SYMBOLS))
    return size if size else 1

def est_bits(pw):
    # naive entropy estimate: log2(charset_size^length)
    return math.log2(charset_size(pw)) * len(pw)

@lru_cache(None)
def base_score(pw):
    """0-100 heuristic score with interpretable pieces."""
    if not pw: return 0
    score = 0.0
    L = len(pw)

    # length
    score += min(L, 20) * 2.5  # max 50

    # diversity
    lowers, uppers, digits, symbols = count_classes(pw)
    diversity = sum(int(x > 0) for x in [lowers, uppers, digits, symbols])
    score += (diversity - 1) * 8  # up to +24

    # entropy
    bits = est_bits(pw)
    score += min(bits, 40) * 0.5  # up to +20

    # penalties
    if dictionary_hits(pw): score -= 20
    if has_sequence(pw):    score -= 15
    if has_repeats(pw):     score -= 10
    if re.search(r"^\d{4,}$", pw): score -= 25  # pure numbers

    # clamp
    return max(0, min(100, int(round(score))))

def strength_label(score):
    if score < 35:  return "weak"
    if score < 70:  return "medium"
    return "strong"

def suggestions(pw):
    tips = []
    L = len(pw)
    lowers, uppers, digits, symbols = count_classes(pw)
    diversity = sum(int(x > 0) for x in [lowers, uppers, digits, symbols])

    if L < 12: tips.append("Increase length to 12–16+ characters.")
    if diversity < 3: tips.append("Use a mix of uppercase, lowercase, digits, and symbols.")
    if dictionary_hits(pw): tips.append("Avoid common words or names.")
    if has_sequence(pw): tips.append("Avoid sequences like 'abcd', '1234', or keyboard runs.")
    if has_repeats(pw): tips.append("Avoid repeated characters like 'aaaa' or '1111'.")
    if re.search(r"^\d{4,}$", pw): tips.append("Do not use only numbers.")
    if not tips:
        tips.append("Great! Keep it long and unique. Consider a passphrase with 3–4 random words.")
    return tips
