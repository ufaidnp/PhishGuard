from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Get URL safely
    url = data.get("url", "")

    # Simple rule-based detection
    if "@" in url or len(url) > 75 or "login" in url:
        result_text = "Phishing"
        confidence = 80.0
        details_text = "Rule-based detection: suspicious URL pattern."
    else:
        result_text = "Legitimate"
        confidence = 90.0
        details_text = "URL appears safe based on simple checks."

    return jsonify({
        "result": result_text,
        "confidence": round(confidence, 2),
        "details": details_text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
