from flask import Blueprint, render_template, request, session
from flask_login import login_required
from modules.prediction import train, predict
from config import db

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction_page():
    case_id = session.get('active_case_id')
    posts = list(db.posts.find({'case_id': case_id}))
    accuracy = train(posts) if posts else 0
    result = None
    if request.method == 'POST':
        post = {
            'text': request.form.get('text', ''),
            'has_media': request.form.get('has_media') == 'on',
            'created_at': request.form.get('hour', '12'),
            'follower_count': int(request.form.get('follower_count', 0)),
        }
        result = predict(post)
    return render_template('prediction.html', accuracy=accuracy, result=result)