@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    if "https" in url:
        result = "Safe Website ✅"
    else:
        result = "Phishing Website ⚠️"

    return render_template("index.html", result=result)
