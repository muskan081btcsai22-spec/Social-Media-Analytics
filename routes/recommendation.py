from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required
from flask import current_app as app
from modules.recommendation import content_based
import json

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendations', methods=['GET','POST'])
@login_required
def recommendation_page():
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

    results = []

    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            results = content_based(text, posts)

    return render_template('recommendation.html', results=results)