import re

EFFECT_PAT = re.compile(
    r"\b(consequence(s)?|outcome(s)?|effect(s)?|impact|implication(s)?|benefit(s)?|"
    r"what did .* lead to|bring about|brought about|what happened as a result|result(ed)? in)\b",
    re.IGNORECASE,
)
CAUSE_PAT = re.compile(
    r"\b(reason|main reason|why|factor(s)?|contribut(e|ed|es|ing)|drove|driven by|led to|"
    r"prompt(ed|s|ing)|motiv(at|ated|ates|ating)|explain(s|ed)?|explanation|stem(s)? from|"
    r"account(s)? for|behind|responsible for|due to|because|caus(e|ed|es|ing)|trigger(ed|s|ing)|"
    r"attribut(ed|able) to|result(ed)? from|foster(s|ed|ing)?)\b",
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
