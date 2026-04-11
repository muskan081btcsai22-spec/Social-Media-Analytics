import re
from collections import Counter
from .utils import get_posts_for_case

def classify_case(case_id, db, top_n=20):
    posts = get_posts_for_case(db, case_id)
    return get_trending(posts, top_n=top_n)

def get_trending(posts, top_n=20):
    hashtags, mentions, keywords = [], [], []
    for post in posts:
        text = post.get('text', '')
        hashtags += re.findall(r'#\w+', text.lower())
        mentions += re.findall(r'@\w+', text.lower())
        keywords += [w.lower() for w in re.findall(r"\b[\w']{5,}\b", text.lower()) if not w.startswith(('#','@'))]
    return {
        'top_hashtags': Counter(hashtags).most_common(top_n),
        'top_mentions': Counter(mentions).most_common(10),
        'top_keywords': Counter(keywords).most_common(10),
    }
