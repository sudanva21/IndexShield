import os
import zipfile
import requests
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import joblib
from textblob import TextBlob

# Scikit-Learn Imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, classification_report

# Setup
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
ps = PorterStemmer()

DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
DATA_ZIP = "sms_spam_collection.zip"
DATA_FILE = "SMSSpamCollection"

# --- Feature Engineering Classes ---

class TextTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer to clean and stem text."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self._clean_text(text) for text in X]

    def _clean_text(self, text):
        text = text.lower()
        # Keep basic punctuation for n-gram context, but here we strip for the 'clean' bag of words
        # Logic: We have separate meta features for structure. 
        # Standard stemming pipeline:
        tokens = nltk.word_tokenize(text)
        y = []
        for i in tokens:
            if i.isalnum():
                y.append(i)
        
        filtered = [i for i in y if i not in stopwords.words('english')]
        stemmed = [ps.stem(i) for i in filtered]
        return " ".join(stemmed)

class MetaFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extracts structural features: Length, Caps Ratio, Punctuation, Spam Density."""
    
    # Keyword list for "Spam Density" calculation (Adversarial Defense)
    # Even if buried in safe words, high density of these flags spam.
    SPAM_KEYWORDS = {
        'free', 'win', 'winner', 'cash', 'prize', 'urgent', 'claim', 
        'congrats', 'guaranteed', 'call', 'loans', 'risk', 'investment'
    }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for text in X:
            features.append(self._extract_features(text))
        return np.array(features)

    def _extract_features(self, text):
        blob = TextBlob(text)
        length = len(text)
        if length == 0: length = 1
        
        # 1. Caps Ratio (Yelling)
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / length

        # 2. Punctuation Count
        punct_count = sum(1 for c in text if c in string.punctuation)
        
        # 3. Sentiment (Salesy/Hype detection)
        # Spam often has extreme sentiment (Very positive promises or Urgent threats)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # 4. Spam Density (Adversarial Defense)
        words = text.lower().split()
        word_count = len(words) if len(words) > 0 else 1
        spam_word_count = sum(1 for w in words if w in self.SPAM_KEYWORDS)
        spam_density = spam_word_count / word_count

        return [length, caps_ratio, punct_count, sentiment, subjectivity, spam_density]

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
