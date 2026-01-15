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
from sklearn.preprocessing import StandardScaler

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
    # 1. Load SMS Data
    try:
        df_sms = pd.read_csv(DATA_FILE, sep='\t', names=['label', 'text'])
        df_sms['source'] = 'sms'
    except Exception:
        print("Error reading SMS dataset.")
        return

    # 2. Load Enron Email Data
    enron_path = "../enron-spam-datasets/enron_spam_data.csv"
    df_enron = pd.DataFrame()
    if os.path.exists(enron_path):
        try:
            # Enron CSV: Subject, Message, Spam/Ham, Date
            # We combine Subject + Message for training
            df_enron = pd.read_csv(enron_path, usecols=['Subject', 'Message', 'Spam/Ham'])
            df_enron['text'] = df_enron['Subject'].fillna('') + " " + df_enron['Message'].fillna('')
            df_enron['label'] = df_enron['Spam/Ham'] # Already 'spam'/'ham'
            df_enron = df_enron[['label', 'text']]
            df_enron['source'] = 'enron'
            print(f"Loaded {len(df_enron)} Enron emails.")
            
            # Optimization: Downsample Enron to 1000 samples to balance with SMS (4800) 
            # and allow reasonable training time on local machine.
            if len(df_enron) > 1000:
                df_enron = df_enron.sample(n=1000, random_state=42)
                print("Downsampled Enron to 1000 random samples for speed.")

        except Exception as e:
            print(f"Error reading Enron dataset: {e}")

    # 3. Load Custom User Data (Human-in-the-Loop)
    custom_path = "custom_data.csv"
    df_custom = pd.DataFrame()
    if os.path.exists(custom_path):
        try:
            df_custom = pd.read_csv(custom_path)
            # Ensure text/label columns exist
            if 'text' in df_custom.columns and 'label' in df_custom.columns:
                 df_custom['source'] = 'custom'
                 print(f"Loaded {len(df_custom)} custom samples.")
        except Exception as e:
            print(f"Error reading custom data: {e}")

    # Combine All
    df = pd.concat([df_sms, df_enron, df_custom], ignore_index=True)
    print(f"Total Combined Training Data: {len(df)} samples.")

    # Convert Labels: ham -> 0, spam -> 1
    df['target'] = df['label'].map({'ham': 0, 'spam': 1})
    
    # Drop NaNs
    df.dropna(subset=['text', 'target'], inplace=True)

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
            ('meta_pipeline', Pipeline([
                ('extractor', MetaFeatureExtractor()),
                ('scaler', StandardScaler())
            ]))
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
