import os
import zipfile
import requests
import pandas as pd
import numpy as np
import joblib

# Scikit-Learn Imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, classification_report

# Import custom model classes specifically for correct pickling
try:
    from model_utils import TextTransformer, MetaFeatureExtractor
except ImportError:
    # Fallback for local run if path issues, but preferred matches deployment structure
    from backend.model_utils import TextTransformer, MetaFeatureExtractor

DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
DATA_ZIP = "sms_spam_collection.zip"
DATA_FILE = "SMSSpamCollection"

# --- Main Logic ---

def download_data():
    if not os.path.exists(DATA_FILE):
        print("Downloading dataset...")
        try:
            r = requests.get(DATA_URL)
            with open(DATA_ZIP, 'wb') as f:
                f.write(r.content)
            
            with zipfile.ZipFile(DATA_ZIP, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("Dataset downloaded and extracted.")
        except Exception as e:
            print(f"Failed to download: {e}")
            print("Please ensure 'SMSSpamCollection' is present.")
    else:
        print("Dataset already exists.")

def train_advanced():
    download_data()
    
    # Load Data
    try:
        df = pd.read_csv(DATA_FILE, sep='\t', names=['label', 'text'])
    except Exception:
        print("Error reading dataset.")
        return

    print(f"Loaded {len(df)} messages.")
    df['target'] = df['label'].map({'ham': 0, 'spam': 1})
    
    X = df['text']
    y = df['target']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Advanced Pipeline ---
    # 1. Text Pipeline: TF-IDF with N-Grams (1,3) to capture "not a winner" / "call now" using SGDClassifier (Linear SVM)
    # 2. Meta Pipeline: Caps, Sentiment, Density
    
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('text_pipeline', Pipeline([
                ('cleaner', TextTransformer()),
                ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 3))) 
            ])),
            ('meta_pipeline', MetaFeatureExtractor())
        ])),
        ('clf', SGDClassifier(loss='hinge', max_iter=1000, tol=1e-3, random_state=42))
    ])
    
    print("Training Advanced Model (SGD/SVM with Feature Union)...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save
    joblib.dump(pipeline, 'advanced_model.pkl')
    print("Advanced Mode saved as 'advanced_model.pkl'")

if __name__ == "__main__":
    train_advanced()
