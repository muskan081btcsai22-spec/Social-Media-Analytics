from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required
from flask import current_app as app
from modules.visualization import (
    engagement_over_time,
    likes_vs_retweets,
    hashtag_distribution,
    top_posts
)
import json

visualization_bp = Blueprint('visualization', __name__)

@visualization_bp.route('/visualization')
@login_required
def visualization_page():
    cid = session.get('active_case_id') or request.args.get('case_id')

    if cid and hasattr(app, "db"):
        try:
            posts = list(app.db.posts.find({'case_id': cid}))
        except Exception:
            with open('sample_data.json') as f:
                posts = json.load(f)
    else:
        with open('sample_data.json') as f:
            posts = json.load(f)
        flash('No active case selected. Using sample data for testing.', 'info')

    return render_template(
        'visualization.html',
        engagement_chart=engagement_over_time(posts),
        bar_chart=likes_vs_retweets(posts),
        pie_chart=hashtag_distribution(posts),
        top_posts=top_posts(posts)
    )