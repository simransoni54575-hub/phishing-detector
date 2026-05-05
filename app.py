from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')

    if not url:
        return render_template('index.html', result="No URL entered ⚠️")

    # SIMPLE DEMO LOGIC
    if url.startswith("https"):
        result = "Safe Website ✅"
    else:
        result = "Phishing Website ❌"

    return render_template('index.html', result=result)


if __name__ == "__main__":
    app.run()
