from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#Currently, only content-based filtering is implemented.
#Collaborative filtering can be added in the future using user interaction data like user liked post id and hashtags.
#User → Route → Module → Template → Screen

def content_based(input_text, all_posts, top_n=5):
    # Combine input text + all post texts
    texts = [input_text] + [
    post['text'] + " " + " ".join(post.get('hashtags', []))
    for post in all_posts
]

    # Convert text to vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute similarity scores
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get top N similar posts
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    # Prepare output
    recommendations = []
    for i in top_indices:
        recommendations.append({
            'id': all_posts[i]['id'],
            'text': all_posts[i]['text'],
            'username': all_posts[i]['username'],
            'likes': all_posts[i]['likes'],
            'score': round(float(similarity_scores[i]), 3)
        })

    return recommendations