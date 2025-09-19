from flask import Flask, render_template, request
import pickle
from Feature import featureExtraction, feature_names

#MongoDB connection
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)

# Load RandomForestClassifier model
rf_model = pickle.load(open('RandomForestClassifier.pickle.dat', 'rb'))
# Load XGBoostClassifier model
xgb_model = pickle.load(open('XGBoostClassifier.pickle.dat', 'rb'))

# #MongoDB ClientConnection
# client = MongoClient("mogodb://localhost:27017/")
# db = client["phishing_db"]
# collection = db["checked_urls"]






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    features = featureExtraction(url)
    rf_prediction = predict_label(url, rf_model)
    xgb_prediction = predict_label(url, xgb_model)
    feature_tuples = list(zip(feature_names, features))  # Zip feature names and values into tuples
    return render_template('result.html', url=url, rf_prediction=rf_prediction, xgb_prediction=xgb_prediction, features=feature_tuples)

def predict_label(url, model):
    # Extract features from the URL
    features = featureExtraction(url)

    # Use the model to predict the label based on the features
    prediction = model.predict([features])[0]

    # Classify the URL based on the prediction
    if prediction == 1:
        label = "Phishing"
    else:
        label = "Legitimate"

    return label

if __name__ == '__main__':
    app.run(debug=True)
