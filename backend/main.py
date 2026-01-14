from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from textblob import TextBlob
from sklearn.base import BaseEstimator, TransformerMixin

# --- Define Classes for Pickle Loading ---
# These MUST match train_model.py exactly for joblib to load the pipeline

ps = PorterStemmer()

class TextTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self._clean_text(text) for text in X]

    def _clean_text(self, text):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        y = []
        for i in tokens:
            if i.isalnum():
                y.append(i)
        
        filtered = [i for i in y if i not in stopwords.words('english')]
        stemmed = [ps.stem(i) for i in filtered]
        return " ".join(stemmed)

class MetaFeatureExtractor(BaseEstimator, TransformerMixin):
    SPAM_KEYWORDS = {
        'free', 'win', 'winner', 'cash', 'prize', 'urgent', 'claim', 
        'congrats', 'guaranteed', 'call', 'loans', 'risk', 'investment'
    }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        # Handle single string input from API correctly
        iterable = X if isinstance(X, list) else [X]
        for text in iterable:
            features.append(self._extract_features(text))
        return np.array(features)

    def _extract_features(self, text):
        blob = TextBlob(text)
        length = len(text)
        if length == 0: length = 1
        
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / length
        punct_count = sum(1 for c in text if c in string.punctuation)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        words = text.lower().split()
        word_count = len(words) if len(words) > 0 else 1
        spam_word_count = sum(1 for w in words if w in self.SPAM_KEYWORDS)
        spam_density = spam_word_count / word_count

        return [length, caps_ratio, punct_count, sentiment, subjectivity, spam_density]

# Initialize App
app = FastAPI(title="Inbox Shield API", description="Advanced Spam Detection with SGD/SVM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Advanced Model
try:
    # We load the entire pipeline. No need to load vectorizer separately.
    model = joblib.load('advanced_model.pkl')
    print("Advanced SVM Pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class EmailRequest(BaseModel):
    text: str

class ReportRequest(BaseModel):
    text: str
    label: str # 'spam' or 'ham'

@app.get("/")
def read_root():
    return {"message": "Inbox Shield Advanced API is running"}

@app.post("/predict")
def predict_spam(request: EmailRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # The pipeline handles raw text transformation internally
    # But we need to pass it as an iterable (list)
    try:
        prediction = model.predict([request.text])[0]
        # SGDClassifier doesn't have predict_proba by default with 'hinge' loss
        # We use decision_function for confidence approximation or calibrate it
        # For simplicity in this iteration, we mock high confidence for SVM or use decision distance
        
        # If we need probability, we would need CalibratedClassifierCV, but let's stick to 
        # a simple heuristic: 
        # SVM decision function gives distance from hyperplane.
        dist = model.decision_function([request.text])[0]
        # Sigmoid approximation for confidence
        confidence = 1 / (1 + np.exp(-abs(dist))) 
        
        result = "spam" if prediction == 1 else "ham"
        
        return {
            "prediction": result,
            "confidence": round(confidence * 100, 2)
        }
    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report")
def report_missed(request: ReportRequest):
    """Feedback loop: User reports a missed spam/ham."""
    # In a real app, we would save this to a database or use partial_fit
    # For MVP, we'll log it to a CSV for future retraining
    try:
        with open("feedback_data.csv", "a") as f:
            f.write(f"{request.label}\t{request.text}\n")
        return {"message": "Feedback received. Model will learn from this."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

