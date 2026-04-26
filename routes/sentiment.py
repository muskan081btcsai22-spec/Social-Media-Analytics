from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required
from flask import current_app as app
import os, json
import plotly.graph_objects as go
import plotly.utils
from modules.sentiment import analyze_sentiment
from modules.utils import get_posts_for_case

sentiment_bp = Blueprint('sentiment', __name__)


@sentiment_bp.route('/sentiment')
@login_required
def sentiment_page():
    cid = session.get('active_case_id')
    posts = []
    if cid:
        try:
            posts = get_posts_for_case(app.db, cid)
        except Exception:
            posts = []

    if not posts:
        sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample_data.json'))
        with open(sample_path, 'r', encoding='utf-8') as f:
            posts = json.load(f)

    results = analyze_sentiment(posts)

    # Pie chart
    counts = results['counts']
    fig = go.Figure(data=[go.Pie(
        labels=list(counts.keys()),
        values=list(counts.values()),
        marker=dict(colors=['#28a745', '#dc3545', '#6c757d'])
    )])
    fig.update_layout(title='Sentiment Distribution')
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Most negative posts
    negative = sorted(
        [d for d in results['details'] if d['label'] == 'negative'],
        key=lambda x: x['score']
    )

    return render_template('sentiment.html', results=results, chart_json=chart_json, negative=negative)
