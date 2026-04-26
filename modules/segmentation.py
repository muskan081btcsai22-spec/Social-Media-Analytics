from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

LABELS = {0: 'Power Users', 1: 'Casual Users', 2: 'Lurkers', 3: 'Bots/Spam'}


def segment_users(posts):
    df = pd.DataFrame(posts)
    features = df[['follower_count', 'likes', 'retweets']].fillna(0)
    n_clusters = min(4, len(df))
    X = StandardScaler().fit_transform(features)
    df['segment'] = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit_predict(X)
    df['label'] = df['segment'].map(LABELS)
    return {
        'counts': df['label'].value_counts().to_dict(),
        'users': df[['username', 'label']].to_dict('records'),
    }
