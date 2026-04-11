from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from bson.objectid import ObjectId
import feedparser, re
from datetime import datetime

cases_bp = Blueprint('cases', __name__)


@cases_bp.route('/')
@login_required
def dashboard():
    from flask import current_app as app
    user = current_user
    cases = list(app.db.cases.find({'owner': user.username}))
    active_case_id = session.get('active_case_id')
    return render_template('dashboard.html', cases=cases, active_case_id=active_case_id)


@cases_bp.route('/cases/create', methods=['POST'])
@login_required
def create_case():
    from flask import current_app as app
    name = request.form.get('name')
    platform = request.form.get('platform')
    keywords = request.form.get('keywords', '')
    time_range = request.form.get('time_range', '')
    feed_url = request.form.get('feed_url', '').strip()
    posts_count = int(request.form.get('posts_count') or 0)
    # store case with feed URL info
    case = {
        'name': name,
        'platform': platform,
        'keywords': [k.strip() for k in keywords.split(',') if k.strip()],
        'time_range': time_range,
        'feed_url': feed_url,
        'posts_count': posts_count,
        'owner': current_user.username,
        'created_at': datetime.utcnow(),
    }
    res = app.db.cases.insert_one(case)
    session['active_case_id'] = str(res.inserted_id)
    flash('Case created and set active', 'success')
    return redirect(url_for('cases.dashboard'))


@cases_bp.route('/cases/fetch/<case_id>', methods=['POST'])
@login_required
def fetch_case_posts(case_id):
    from flask import current_app as app
    try:
        oid = ObjectId(case_id)
    except Exception:
        flash('Invalid case id', 'danger')
        return redirect(url_for('cases.dashboard'))
    case = app.db.cases.find_one({'_id': oid})
    if not case:
        flash('Case not found', 'danger')
        return redirect(url_for('cases.dashboard'))

    feed_url = case.get('feed_url')
    posts_count = int(case.get('posts_count') or 0)
    if not feed_url:
        flash('No feed URL provided for this case', 'danger')
        return redirect(url_for('cases.dashboard'))

    # parse feed using feedparser
    try:
        parsed = feedparser.parse(feed_url)
        items = parsed.entries or []
    except Exception as e:
        flash(f'Failed to parse feed: {e}', 'danger')
        return redirect(url_for('cases.dashboard'))

    if not items:
        flash('No entries found in feed', 'warning')
        return redirect(url_for('cases.dashboard'))

    saved = []
    for i, it in enumerate(items[:posts_count or len(items)]):
        # build text from title + summary/content
        title = getattr(it, 'title', '') or it.get('title','') if isinstance(it, dict) else ''
        summary = getattr(it, 'summary', '') or it.get('summary','') if isinstance(it, dict) else ''
        content = ''
        if isinstance(it, dict):
            if 'content' in it and isinstance(it['content'], list) and len(it['content'])>0:
                content = it['content'][0].get('value','')
        else:
            if hasattr(it, 'content') and isinstance(it.content, list) and len(it.content)>0:
                content = getattr(it.content[0], 'value', '')

        text = ' '.join([s for s in (title, summary, content) if s]).strip()
        if not text:
            continue

        hashtags = re.findall(r'#(\w+)', text)
        mentions = re.findall(r'@(\w+)', text)

        author = getattr(it, 'author', '') or (it.get('author') if isinstance(it, dict) else '')
        published = getattr(it, 'published', '') or (it.get('published') if isinstance(it, dict) else '')

        doc = {
            'case_id': str(case['_id']),
            'text': text,
            'username': author or '',
            'created_at': published or datetime.utcnow().isoformat(),
            'hashtags': hashtags,
            'mentions': mentions,
            'source': feed_url,
        }
        saved.append(doc)

    if saved:
        app.db.posts.insert_many(saved)
        # ensure this case is marked active in the session
        session['active_case_id'] = str(case['_id'])
        flash(f'Inserted {len(saved)} posts for case', 'success')
    else:
        flash('No valid posts to insert', 'warning')

    # redirect to trending view for the active case so user can see classifications
    return redirect(url_for('trending.trending_page'))


@cases_bp.route('/cases/select/<case_id>')
@login_required
def select_case(case_id):
    try:
        oid = ObjectId(case_id)
    except Exception:
        flash('Invalid case id', 'danger')
        return redirect(url_for('cases.dashboard'))
    session['active_case_id'] = case_id
    flash('Active case set', 'info')
    return redirect(url_for('cases.dashboard'))
