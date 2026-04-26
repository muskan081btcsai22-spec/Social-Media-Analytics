from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from flask import current_app as app
import plotly.graph_objects as go
import plotly.utils
import json
from modules.realtime import fetch_live_posts, get_monitoring_stats
from datetime import datetime

realtime_bp = Blueprint('realtime', __name__)


@realtime_bp.route('/realtime', methods=['GET', 'POST'])
@login_required
def realtime_page():
    cid = session.get('active_case_id')
    if not cid:
        flash('No active case selected. Create/select a case first.', 'info')
        return redirect(url_for('cases.dashboard'))

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        max_posts = int(request.form.get('max_posts', 50))
        if not keyword:
            flash('Please enter a keyword to search.', 'warning')
            return redirect(url_for('realtime.realtime_page'))

        posts = fetch_live_posts(keyword, max_posts, app.db, cid)
        flash(f'Successfully fetched {len(posts)} posts for "{keyword}".', 'success')
        return redirect(url_for('realtime.realtime_page'))

    posts = list(app.db.posts.find({'case_id': cid}))

    keyword = request.args.get('keyword', '').strip().lower()
    if keyword:
        posts = [p for p in posts if keyword in p.get('text','').lower() or keyword in ' '.join(p.get('hashtags',[])).lower()]

    stats = get_monitoring_stats(posts)

    fig = go.Figure()
    if posts:
        date_counts = {}
        for post in posts:
            created_at = post.get('created_at', '')
            if created_at:
                try:
                    date = datetime.fromisoformat(str(created_at).replace('Z', '+00:00')).date()
                    date_counts[date] = date_counts.get(date, 0) + 1
                except:
                    continue
        if date_counts:
            dates = sorted(date_counts.keys())
            counts = [date_counts[d] for d in dates]
            fig.add_trace(go.Scatter(
                x=[str(d) for d in dates],
                y=counts,
                mode='lines+markers'
            ))
            fig.update_layout(
                title="Post Volume Over Time",
                xaxis_title="Date",
                yaxis_title="Number of Posts",
                height=400
            )
        else:
            fig.update_layout(
                title="Post Volume Over Time (No valid dates found)",
                height=400
            )
    else:
        fig.update_layout(
            title="Post Volume Over Time (No posts to display)",
            height=400
        )
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('realtime.html', stats=stats, posts=posts, chart_json=chart_json, keyword=keyword)