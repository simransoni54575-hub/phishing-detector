@app.route('/predict', methods=['POST'])
def predict():
    try:
        url = request.form['url']

        # TEMP LOGIC (demo)
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
        return render_template('index.html', result="Error occurred ⚠️")
