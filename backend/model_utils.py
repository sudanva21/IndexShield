import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import numpy as np
from textblob import TextBlob
from sklearn.base import BaseEstimator, TransformerMixin

# Initialize Stemmer
ps = PorterStemmer()

# Ensure NLTK data is available (safe check for imports)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer to clean and stem text."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Handle list vs string input
        if isinstance(X, str):
            X = [X]
        return [self._clean_text(text) for text in X]

    def _clean_text(self, text):
        text = str(text).lower()
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
    
    SPAM_KEYWORDS = {
        'free', 'win', 'winner', 'cash', 'prize', 'urgent', 'claim', 
        'congrats', 'guaranteed', 'call', 'loans', 'risk', 'investment'
    }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Handle single string input (inference) vs list/Series (training)
        if isinstance(X, str):
            X = [X]
            
        features = []
        for text in X:
            features.append(self._extract_features(str(text)))
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
