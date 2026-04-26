from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from flask import current_app as app
import plotly.graph_objects as go
import plotly.utils
import json
from modules.trending import get_trending

trending_bp = Blueprint('trending', __name__)

@trending_bp.route('/trending', methods=['GET', 'POST'])
@login_required
def trending_page():
    cid = session.get('active_case_id') or request.args.get('case_id')
    if not cid:
        flash('No active case selected. Create/select a case first.', 'info')
        return redirect(url_for('cases.dashboard'))

    posts = list(app.db.posts.find({'case_id': cid}))

    keyword = request.values.get('keyword', '').strip().lower()
    if keyword:
        posts = [p for p in posts if keyword in p.get('text', '').lower()
                 or keyword in ' '.join(p.get('hashtags', [])).lower()]

    results = get_trending(posts)
    top_hashtags = results['top_hashtags'][:5]

    labels = [item[0] for item in top_hashtags]
    values = [item[1] for item in top_hashtags]

    fig = go.Figure()
    if labels and values:
        fig.add_trace(go.Bar(x=values[::-1], y=labels[::-1], orientation='h'))
        fig.update_layout(height=400, margin=dict(l=100))
    else:
        fig.update_layout(title="No trending hashtags found", height=400)

    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('trending.html', results=results, chart_json=chart_json, keyword=keyword)