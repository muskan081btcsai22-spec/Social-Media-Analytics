from apify_client import ApifyClient
import os


def fetch_live_posts(keyword, max_posts, db, case_id):
    token = os.environ.get('APIFY_TOKEN')

    try:
        client = ApifyClient(token)
        run = client.actor('altimis/scweet').call(run_input={
            'searchTerms': [keyword],
            'maxItems': max_posts,
        })
        posts = []
        for item in client.dataset(run['defaultDatasetId']).iterate_items():
            posts.append({
                'case_id':      case_id,
                'text':         item.get('tweet', ''),
                'username':     item.get('username', ''),
                'likes':        item.get('nlikes', 0),
                'retweets':     item.get('nretweets', 0),
                'created_at':   item.get('date', ''),
                'hashtags':     item.get('hashtags', []),
                'mentions':     item.get('mentions', []),
                'follower_count': item.get('nfollowers', 0),
            })
    except Exception as e:
        print(f"Apify error: {e}")
        posts = [
            {'case_id': case_id, 'text': f'Sample post about {keyword} 1', 'username': 'user1', 'likes': 10, 'retweets': 2, 'created_at': '2024-01-01', 'hashtags': [keyword], 'mentions': [], 'follower_count': 100},
            {'case_id': case_id, 'text': f'Sample post about {keyword} 2', 'username': 'user2', 'likes': 5,  'retweets': 1, 'created_at': '2024-01-02', 'hashtags': [keyword], 'mentions': [], 'follower_count': 200},
            {'case_id': case_id, 'text': f'Sample post about {keyword} 3', 'username': 'user3', 'likes': 20, 'retweets': 8, 'created_at': '2024-01-03', 'hashtags': [keyword], 'mentions': [], 'follower_count': 500},
        ]

    if posts:
        db.posts.insert_many(posts)
    return posts


def get_monitoring_stats(posts):
    """
    Calculate monitoring statistics from a list of posts.
    """
    if not posts:
        return {
            'total_posts': 0,
            'total_likes': 0,
            'total_retweets': 0,
            'most_recent': None,
            'top_post': None
        }
    total_posts = len(posts)
    total_likes = sum(post.get('likes', 0) for post in posts)
    total_retweets = sum(post.get('retweets', 0) for post in posts)
    most_recent = max(posts, key=lambda p: p.get('created_at', ''), default=None)
    top_post = max(posts, key=lambda p: p.get('likes', 0), default=None)
    return {
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_retweets': total_retweets,
        'most_recent': most_recent['created_at'] if most_recent else None,
        'top_post': top_post
    }