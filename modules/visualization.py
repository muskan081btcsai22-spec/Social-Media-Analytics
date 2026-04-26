import plotly.graph_objects as go
import plotly.utils
import json
from collections import defaultdict

# 1. Line chart: engagement over time
def engagement_over_time(posts):
    by_date = defaultdict(lambda: {'likes': 0, 'retweets': 0})

    for p in posts:
        date = p['created_at'][:10]
        by_date[date]['likes'] += p.get('likes', 0)
        by_date[date]['retweets'] += p.get('retweets', 0)

    dates = sorted(by_date)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=[by_date[d]['likes'] for d in dates],
        name='Likes',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=dates,
        y=[by_date[d]['retweets'] for d in dates],
        name='Retweets',
        mode='lines+markers'
    ))

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# 2. Bar chart: likes vs retweets
def likes_vs_retweets(posts):
    users = [p['username'] for p in posts]
    likes = [p.get('likes', 0) for p in posts]
    retweets = [p.get('retweets', 0) for p in posts]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=users, y=likes, name='Likes'))
    fig.add_trace(go.Bar(x=users, y=retweets, name='Retweets'))

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# 3. Pie chart: hashtag distribution (reach)
def hashtag_distribution(posts):
    tag_count = defaultdict(int)

    for p in posts:
        for tag in p.get('hashtags', []):
            tag_count[tag] += 1

    fig = go.Figure(data=[go.Pie(
        labels=list(tag_count.keys()),
        values=list(tag_count.values())
    )])

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# 4. Top posts table (data only)
def top_posts(posts, top_n=5):
    sorted_posts = sorted(posts, key=lambda x: x.get('likes', 0), reverse=True)
    return sorted_posts[:top_n]