import re

EFFECT_PAT = re.compile(
    r"\b("
    r"what did .* lead to|"
    r"lead to\b|"
    r"result(ed)? in\b|"
    r"as a result\b|"
    r"consequence(s)?\b|"
    r"outcome(s)?\b|"
    r"effect(s)?\b|"
    r"impact\b|"
    r"implication(s)?\b|"
    r"bring about\b|"
    r"brought about\b|"
    r"what happened\b|"
    r"benefit(s)?\b"
    r")\b",
    re.IGNORECASE,
)

CAUSE_PAT = re.compile(
    r"\b("
    r"reason\b|"
    r"main reason\b|"
    r"why\b|"
    r"factor(s)?\b|"
    r"contribut(e|ed|es|ing)\b|"
    r"drove\b|"
    r"driven by\b|"
    r"led to\b|"
    r"prompt(ed|s|ing)\b|"
    r"motiv(at|ated|ates|ating)\b|"
    r"explain(s|ed)?\b|"
    r"explanation\b|"
    r"stem(s)? from\b|"
    r"account(s)? for\b|"
    r"behind\b|"
    r"responsible for\b|"
    r"due to\b|"
    r"because\b|"
    r"caus(e|ed|es|ing)\b|"
    r"trigger(ed|s|ing)\b|"
    r"attribut(ed|able) to\b|"
    r"result(ed)? from\b|"
    r"foster(s|ed|ing)?\b"
    r")\b",
    re.IGNORECASE,
)



def get_template(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "OTHER"
    if EFFECT_PAT.search(q):
        return "EFFECT"
    if CAUSE_PAT.search(q):
        return "CAUSE"
    return "OTHER"
