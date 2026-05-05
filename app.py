from flask import Flask, request, render_template

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# PREDICT ROUTE
@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # simple working logic (no ML crash)
    if "https" in url:
        result = "Safe Website ✅"
    else:
        result = "Phishing Website ⚠️"

    return f"<h2>{result}</h2><br><a href='/'>Go Back</a>"


if __name__ == "__main__":
    app.run()
