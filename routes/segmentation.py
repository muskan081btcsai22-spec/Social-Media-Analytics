from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required
from flask import current_app as app
import os, json
import plotly.graph_objects as go
import plotly.utils
from modules.segmentation import segment_users
from modules.utils import get_posts_for_case

segmentation_bp = Blueprint('segmentation', __name__)


@segmentation_bp.route('/segmentation')
@login_required
def segmentation_page():
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

    results = segment_users(posts)

    # Bar chart
    counts = results['counts']
    fig = go.Figure(data=[go.Bar(
        x=list(counts.keys()),
        y=list(counts.values()),
        marker_color=['#0d6efd', '#198754', '#6c757d', '#dc3545'][:len(counts)]
    )])
    fig.update_layout(title='User Segments', yaxis_title='Number of Users')
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('segmentation.html', results=results, chart_json=chart_json)
