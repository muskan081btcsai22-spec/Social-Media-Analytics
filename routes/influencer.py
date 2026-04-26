from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required
from flask import current_app as app
from modules.influencer import detect_influencers
import json

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/influencer')
@login_required
def influencer_page():
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

    results = detect_influencers(posts)

    return render_template('influencer.html', results=results)