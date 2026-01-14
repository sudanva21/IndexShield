# Inbox Shield 🛡️
**Advanced AI-Powered Spam Detection System**

Inbox Shield is a production-grade web application designed to identify and filter spam messages with high precision. It moves beyond simple keyword matching by employing a **Hybrid NLP Pipeline** that analyzes both the *content* (context, sentiment) and *structure* (formatting, density) of messages.

---

## 🚀 Key Features

### 🧠 Advanced AI Engine
- **Hybrid Analysis**: Combines Textual Analysis (TF-IDF, N-Grams) with Structural Analysis (Spam Density, Metadata).
- **Context Awareness**: Understands negation and phrasing (e.g., "not a winner" vs "winner") using N-grams.
- **Adversarial Defense**: Detects "Bayesian Poisoning" (hiding spam in safe text) using specialized Density calculations.
- **Sentiment Detection**: Flags aggressive "salesy" or "urgent" tones typical of scams.
- **High Precision**: Uses a Linear Support Vector Machine (SGD) for varying decision boundaries.

### 🎨 Premium Frontend Experience
- **Modern UI**: Built with a "Glass & Slate" aesthetic using **Vanilla CSS**.
- **Real-Time Scanning**: Instant feedback with animated confidence meters.
- **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile.
- **Privacy First**: Client-server architecture ensures separation of concerns.

---

## 🛠️ Technology Stack

### Frontend Application
- **Framework**: React 18 (Vite)
- **Language**: TypeScript
- **Styling**: Pure **Vanilla CSS** (Custom Design System with CSS Variables)
- **Icons**: Lucide React
- **HTTP Client**: Native `fetch` with Vite Proxy

### Backend API
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn (ASGI)
- **Data Validation**: Pydantic
- **ML Libraries**: 
    - `scikit-learn` (Modeling, Pipelines)
    - `nltk` (Tokenization, Stemming)
    - `textblob` (Sentiment Analysis)
    - `pandas` & `numpy` (Data Manipulation)

---

## 🏗️ System Architecture & Logic

### 1. The AI Model (Hybrid Pipeline)
The core logic resides in `backend/train_model.py`. We use a `FeatureUnion` pipeline that splits processing into two parallel paths:

#### A. Textual Path (Context)
1.  **Preprocessing**: content is lowercased, tokenized (NLTK), cleaned of stopwords, and stemmed (PorterStemmer).
2.  **Vectorization**: `TfidfVectorizer` converts text to numbers.
3.  **N-Grams**: We use `ngram_range=(1, 3)` to capture sequences like "call now" or "apply for free".

#### B. Structural Path (Meta-Features)
A custom `MetaFeatureExtractor` calculates:
1.  **Spam Density**: Ratio of known spam triggers (e.g., "win", "free", "claim") to total words. *Crucial for detecting hidden spam.*
2.  **Caps Ratio**: Percentage of uppercase characters. Flags "screaming" messages.
3.  **Sentiment Score**: Uses `TextBlob` to detect high polarity (hype) or subjectivity.
4.  **Punctuation Count**: Detects excessive `!`, `$`, `?`.

#### C. Classification
The features from A and B are concatenated and fed into an **SGDClassifier (Linear SVM)**.
- **Why SVM?** It handles high-dimensional text data better than Naive Bayes and creates a robust decision boundary.
- **Training**: Trained on the UCI SMS Spam Collection (5574 messages).

### 2. Backend Logic (`main.py`)
- **Initialization**: Loads the trained pipeline (`advanced_model.pkl`) using `joblib`.
- **Pipeline Preservation**: Re-declares `TextTransformer` and `MetaFeatureExtractor` classes to ensure Pickle compatibility.
- **CORS**: Configured to allow all origins ensuring smooth frontend-backend communication.

### 3. Frontend Architecture
- **`Layout.tsx`**: The main wrapper. Handles the application shell, including the glass-effect background and persistent Navbar/Footer.
- **`Scanner.tsx`**: The core interactive component.
    - Maintains interaction state (`isLoading`, `result`).
    - Validates input (empty check).
    - Sends POST requests to `/api/predict`.
    - Renders the "Confidence Meter" visualization based on the API response.
- **Design System (`index.css`)**: Defines global variables (`--primary`, `--bg-gradient`) and utility classes.

---

## 📡 API Reference

### 1. Predict (Spam Check)
**Endpoint**: `POST /predict`
**Description**: Analyzes text using the Advanced AI Model and returns classification.

**Request Body**:
```json
{
  "text": "Congratulations! You won a free iPhone. Call now!"
}
```

**Response**:
```json
{
  "prediction": "spam",
  "confidence": 98.45
}
```

### 2. Report (Feedback Loop)
**Endpoint**: `POST /report`
**Description**: Collects user feedback for missed classifications to facilitate Online Learning.

**Request Body**:
```json
{
  "text": "This was actually a valid email from my bank.",
  "label": "ham" 
}
```

**Response**:
```json
{
  "message": "Feedback received. Model will learn from this."
}
```

---

## 💻 Installation & Setup

### Prerequisites
- Node.js & npm
- Python 3.8+

### 1. Backend Setup
Navigate to the `backend` folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install fastapi uvicorn scikit-learn nltk pandas numpy textblob joblib
```

**Train the Model (Required first time):**
This script downloads the dataset, trains the hybrid model, and saves `advanced_model.pkl`.
```bash
python train_model.py
```

Start the API Server:
```bash
uvicorn main:app --reload --port 8000
```
*Server runs at http://127.0.0.1:8000*

### 2. Frontend Setup
Open a new terminal and navigate to the `frontend` folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the Development Server:
```bash
npm run dev
```
*App runs at http://localhost:5173*

---

## 📂 Project Structure

```text
proj2/
├── backend/
│   ├── main.py              # FastAPI Application & Endpoints
│   ├── train_model.py       # ML Pipeline, Training & Evaluation Script
│   ├── advanced_model.pkl   # Serialized Trained Model
│   ├── SMSSpamCollection    # Dataset
│   └── feedback_data.csv    # User Feedback Log
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI (Navbar, Layout, Footer)
│   │   ├── pages/
│   │   │   ├── Home.tsx     # Landing Page
│   │   │   ├── Scanner.tsx  # Core Functionality Page
│   │   │   └── Technology.tsx # Explainer Page
│   │   ├── index.css        # Global Design System (Vanilla CSS)
│   │   └── main.tsx         # Entry Point
│   └── vite.config.ts       # Proxy Configuration
│
├── report.md                # Project Performance Report
└── README.md                # This Documentation
```

## 🔮 Future Improvements
- **Email Dataset**: Incorporate the Enron dataset for better long-form email support.
- **OCR Integration**: Add capability to scan text inside images.
- **User Feedback**: Fully implement the `/report` endpoint to retrain the model on live user feedback.
