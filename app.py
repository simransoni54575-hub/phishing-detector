from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        url = request.form.get('url')

        if not url:
            return render_template('index.html', result="No URL entered ⚠️")

        # TEMP LOGIC
        if "https" in url:
            prediction = 0
        else:
            prediction = 1

        if prediction == 1:
            result = "Phishing Website ❌"
        else:
            result = "Safe Website ✅"

        return render_template('index.html', result=result)

    except Exception as e:
        print("ERROR:", e)   # logs me dikhega
        return render_template('index.html', result="Error occurred ⚠️")

if __name__ == "__main__":
    app.run()
