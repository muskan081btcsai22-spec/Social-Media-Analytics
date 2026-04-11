from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import login_required
import os, json
from modules.fakenews import classify_posts
import plotly.graph_objects as go
import plotly.utils
from flask import current_app as app
from modules.utils import get_posts_for_case

fakenews_bp = Blueprint('fakenews', __name__)


@fakenews_bp.route('/fakenews')
@login_required
def fakenews_page():
    # prefer posts for the active case (session), fallback to sample file
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

    # classify all posts and prepare counts, but only show first 5 posts in UI
    try:
        classified_all = classify_posts(posts)
    except Exception:
        classified_all = [{'text': p.get('text',''), 'label': 'Model missing'} for p in posts]

    counts = {'Fake': 0, 'Real': 0}
    for c in classified_all:
        if c['label'] in counts:
            counts[c['label']] += 1

    fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()))])
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # only show first 5 posts in UI
    classified = classified_all[:5]
    return render_template('fakenews.html', classified=classified, chart_json=chart_json)
