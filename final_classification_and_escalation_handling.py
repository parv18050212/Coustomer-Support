import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib  # Importing joblib for saving/loading models

# Sample synthetic data for classification and sentiment analysis

# Correct file path with raw string or forward slashes
data = pd.read_csv(r"D:\Coding\Coustomer Support\balanced_customer_support_data.csv")

# Creating DataFrame
df = pd.DataFrame(data)

# Split the data into training and testing sets
X = df['query']
y_category = df['category']
y_sentiment = df['sentiment']
y_escalation = df['escalation']

X_train, X_test, y_train_category, y_test_category = train_test_split(X, y_category, test_size=0.3, random_state=42)
X_train, X_test, y_train_sentiment, y_test_sentiment = train_test_split(X, y_sentiment, test_size=0.3, random_state=42)
X_train, X_test, y_train_escalation, y_test_escalation = train_test_split(X, y_escalation, test_size=0.3, random_state=42)

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the training data, transform the test data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Random Forest for escalation handling
rf_classifier_escalation = RandomForestClassifier()
rf_classifier_escalation.fit(X_train_tfidf, y_train_escalation)

# Train Random Forest for category classification
rf_classifier_category = RandomForestClassifier()
rf_classifier_category.fit(X_train_tfidf, y_train_category)

# Train Random Forest for sentiment classification
rf_classifier_sentiment = RandomForestClassifier()
rf_classifier_sentiment.fit(X_train_tfidf, y_train_sentiment)

# Package all models and the vectorizer into a dictionary
models = {
    'rf_classifier_escalation': rf_classifier_escalation,
    'rf_classifier_category': rf_classifier_category,
    'rf_classifier_sentiment': rf_classifier_sentiment,
    'vectorizer': vectorizer
}

# Save all components as a single Joblib file
joblib.dump(models, 'final_model.joblib')

# Make predictions for escalation
y_pred_escalation = rf_classifier_escalation.predict(X_test_tfidf)

# Print the classification report for escalation handling
print("Escalation Handling Classification Report:\n", classification_report(y_test_escalation, y_pred_escalation))

# Predictions for category classification
y_pred_category = rf_classifier_category.predict(X_test_tfidf)

# Classification report for category prediction
print("Category Classification Report:\n", classification_report(y_test_category, y_pred_category))

# Predictions for sentiment classification
y_pred_sentiment = rf_classifier_sentiment.predict(X_test_tfidf)

# Classification report for sentiment prediction
print("Sentiment Classification Report:\n", classification_report(y_test_sentiment, y_pred_sentiment))
