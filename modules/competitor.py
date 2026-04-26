"""
Functions for comparing competitor brands based on social media posts.
"""

def compare_brands(posts_a, posts_b, name_a, name_b):
    """
    Compare two sets of posts for brands A and B, calculating key metrics.

    Args:
        posts_a (list): List of post dicts for brand A.
        posts_b (list): List of post dicts for brand B.
        name_a (str): Name of brand A.
        name_b (str): Name of brand B.

    Returns:
        dict: {name_a: stats_a, name_b: stats_b}, where each stats dict contains:
              post_count, total_likes, total_retweets, avg_engagement, top_post, most_used_hashtag.
    """
    def calculate_stats(posts):
        if not posts:
            return {
                'post_count': 0,
                'total_likes': 0,
                'total_retweets': 0,
                'avg_engagement': 0.0,
                'top_post': None,
                'most_used_hashtag': None
            }
        post_count = len(posts)
        total_likes = sum(post.get('likes', 0) for post in posts)
        total_retweets = sum(post.get('retweets', 0) for post in posts)
        avg_engagement = (total_likes + total_retweets) / post_count if post_count > 0 else 0.0
        top_post = max(posts, key=lambda p: p.get('likes', 0), default=None)
        hashtags = [h for post in posts for h in post.get('hashtags', [])]
        most_used_hashtag = max(set(hashtags), key=hashtags.count, default=None) if hashtags else None
        return {
            'post_count': post_count,
            'total_likes': total_likes,
            'total_retweets': total_retweets,
            'avg_engagement': round(avg_engagement, 2),
            'top_post': top_post,
            'most_used_hashtag': most_used_hashtag
        }
    
    stats_a = calculate_stats(posts_a)
    stats_b = calculate_stats(posts_b)
    return {name_a: stats_a, name_b: stats_b}

def get_winner(stats_a, stats_b, name_a, name_b):
    """
    Determine the winner for each metric based on higher values.

    Args:
        stats_a (dict): Stats for brand A.
        stats_b (dict): Stats for brand B.
        name_a (str): Name of brand A.
        name_b (str): Name of brand B.

    Returns:
        dict: {metric: winner_name} for each comparable metric.
    """
    metrics = ['post_count', 'total_likes', 'total_retweets', 'avg_engagement']
    winners = {}
    for metric in metrics:
        val_a = stats_a.get(metric, 0)
        val_b = stats_b.get(metric, 0)
        winners[metric] = name_a if val_a > val_b else (name_b if val_b > val_a else 'Tie')
    return winners