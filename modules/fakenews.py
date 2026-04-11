import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'fakenews.pkl')

def train_model(csv_path, save_path=None):
    df = pd.read_csv(csv_path)[['text','label']].dropna()
    vec = TfidfVectorizer(max_features=5000, stop_words='english')
    X = vec.fit_transform(df['text'])
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, df['label'])
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    path = save_path or MODEL_PATH
    with open(path, 'wb') as f:
        pickle.dump((vec, clf), f)
    return 'Trained and saved to ' + path

def predict(text, model_path=None):
    path = model_path or MODEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError('Model not found. Train and save first.')
    with open(path, 'rb') as f:
        vec, clf = pickle.load(f)
    pred = clf.predict(vec.transform([text]))[0]
    return 'Fake' if pred == 1 else 'Real'

def classify_posts(posts):
    return [{'text': p.get('text',''), 'label': predict(p.get('text',''))} for p in posts]
