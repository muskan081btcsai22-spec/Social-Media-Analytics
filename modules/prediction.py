from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle, os

def extract_features(post):
    text = post.get('text', '')
    return [
        len(text),
        text.count('#'),
        text.count('@'),
        1 if post.get('has_media') else 0,
        int(str(post.get('created_at', '12'))[:2] or 12),
        post.get('follower_count', 0),
    ]

def train(posts):
    X = [extract_features(p) for p in posts]
    y = [p.get('likes', 0) for p in posts]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    os.makedirs('models', exist_ok=True)
    pickle.dump(model, open('models/predictor.pkl', 'wb'))
    return round(model.score(X_test, y_test), 3)

def predict(post):
    model = pickle.load(open('models/predictor.pkl', 'rb'))
    return int(model.predict([extract_features(post)])[0])