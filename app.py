from flask import Flask, render_template, request, jsonify
import Levenshtein
import re
import unicodedata


app = Flask(__name__)

DESCRIPTIONS = [
    "Nazwa",
    "Nazwa 2",
    "Kod 1",
    "Kod 2",
    "Kod 3",
    "Biopreparat",
    "Substancja czynna"
]

DEFAULT_VALUES_1 = ["SUBSTRAL Naturen MULTI-INSECT", "marvik vita 240 ew", "1. bas 9314 6 f", "adm.03500.f.2.b (soratel; soratel 250 ec)", "119446- 68-3", "szczep beauveria bassana strain gha beauveria bassana strain gha 10 - 30", "mesotrione , mesetrione"]
DEFAULT_VALUES_2 = ["substral naturen multi-insekt", "marvik vita 240 ew", "BAS® 93146F", "ADM.00051.F.8.B", "119446-\n68-3", "Beauveria bassana strain GHA", "mesotrione"]

@app.route("/")
def index():
    return render_template("index.html", descriptions=DESCRIPTIONS, values1=DEFAULT_VALUES_1, values2=DEFAULT_VALUES_2)


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    results = []
    for pair in data["pairs"]:
        val1 = normalize_text(pair.get("val1", ""))
        val2 = normalize_text(pair.get("val2", ""))
        distance = Levenshtein.distance(val1, val2)
        results.append(distance)

    min_index = max_index = None
    if results:
        min_value = min(results)
        max_value = max(results)
        min_index = results.index(min_value)
        max_index = results.index(max_value)

    avg = 0
    if len(results) > 2:
        sorted_results = sorted(results)
        trimmed = sorted_results[1:-1]
        avg = round(sum(trimmed) / len(trimmed), 2)
    elif results:
        avg = round(sum(results) / len(results), 2)

    return jsonify({"results": results, "average": avg, "min_index": min_index, "max_index": max_index})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
