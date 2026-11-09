"""Report untranslated literal Streamlit copy without changing app behavior.

Usage: python scripts/report_untranslated_ui.py
This is a discovery report, not a clinical translation validator. It flags
literal user-facing strings in Streamlit calls which have not been routed
through t()/ui(), including content in conditional expressions.
"""
import ast
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ("app.py", "mamacare.py", "adaptivecare.py", "babycare.py", "find_care.py")
UI_CALLS = {
    "write", "caption", "info", "warning", "error", "success",
    "markdown", "title", "header", "subheader", "button", "checkbox",
    "text_input", "text_area", "selectbox", "radio", "expander",
}
EXCLUDED = ("<style", "<script", "<div", "<span", "<p ", "<svg", "data:", "http")


def literal_strings(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
    elif isinstance(node, (ast.JoinedStr, ast.BinOp, ast.IfExp)):
        for child in ast.iter_child_nodes(node):
            yield from literal_strings(child)


def main():
    found = defaultdict(list)
    for name in MODULES:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if not isinstance(node.func.value, ast.Name) or node.func.value.id != "st":
                continue
            if node.func.attr not in UI_CALLS or not node.args:
                continue
            for phrase in literal_strings(node.args[0]):
                phrase = phrase.strip()
                if len(phrase) < 12 or phrase.startswith(EXCLUDED):
                    continue
                found[name].append((node.lineno, phrase.replace("\n", " ")[:140]))
    count = sum(map(len, found.values()))
    print(f"Potential untranslated literals: {count} (review manually; HTML and dynamic content may be false positives)")
    for name in MODULES:
        entries = found[name]
        print(f"\n{name}: {len(entries)} candidate(s)")
        for line, phrase in entries:
            print(f"  {line}: {phrase}")
    print("\nThis report does not indicate that all other text is translated or clinically reviewed.")


if __name__ == "__main__":
    main()
