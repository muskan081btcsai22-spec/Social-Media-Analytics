from flask import Blueprint, render_template, session, flash, redirect, url_for, send_file
from flask_login import login_required
from flask import current_app as app
import os, json
from modules.network import build_network
from modules.utils import get_posts_for_case

network_bp = Blueprint('network', __name__)


@network_bp.route('/network_viz')
@login_required
def network_viz():
    viz_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'network_viz.html'))
    if os.path.exists(viz_path):
        return send_file(viz_path)
    return 'Graph not generated yet.', 404


@network_bp.route('/network')
@login_required
def network_page():
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

    results = build_network(posts)
    return render_template('network.html', results=results)
