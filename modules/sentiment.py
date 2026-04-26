from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiment(posts):
    analyzer = SentimentIntensityAnalyzer()
    counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    details = []
    for post in posts:
        score = analyzer.polarity_scores(post['text'])['compound']
        label = 'positive' if score >= 0.05 else 'negative' if score <= -0.05 else 'neutral'
        counts[label] += 1
        details.append({'text': post['text'], 'label': label, 'score': round(score, 3)})
    return {'counts': counts, 'details': details}
