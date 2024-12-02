from flask import Flask, request, jsonify, render_template
import joblib

# Load the model and vectorizer
model_path = 'final_model.joblib'  # Ensure this matches your file path
models = joblib.load(model_path)

# Extract individual components
vectorizer = models['vectorizer']
rf_classifier_escalation = models['rf_classifier_escalation']
rf_classifier_category = models['rf_classifier_category']
rf_classifier_sentiment = models['rf_classifier_sentiment']

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    data = request.form.get('query')
    
    if data and data.strip():
        query_tfidf = vectorizer.transform([data])
        
        # Make predictions
        escalation_prediction = rf_classifier_escalation.predict(query_tfidf)[0]
        category_prediction = rf_classifier_category.predict(query_tfidf)[0]
        sentiment_prediction = rf_classifier_sentiment.predict(query_tfidf)[0]

        # Return predictions
        result = {
            "Escalation Required": "Yes" if escalation_prediction == 1 else "No",
            "Category": category_prediction,
            "Sentiment": sentiment_prediction
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Please provide a valid query."}), 400

if __name__ == '__main__':
    app.run(debug=True)
