from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required
from flask import current_app as app
import plotly.graph_objects as go
import plotly.utils
import json
import re
from modules.competitor import compare_brands, get_winner

competitor_bp = Blueprint('competitor', __name__)

@competitor_bp.route('/competitor', methods=['GET', 'POST'])
@login_required
def competitor_page():
    cid = session.get('active_case_id')
    if not cid:
        flash('No active case selected. Create/select a case first.', 'info')
        return redirect(url_for('cases.dashboard'))

    results = None
    chart_json = None
    pie_charts = {}
    winners = {}

    if request.method == 'POST':
        keyword_a = request.form.get('keyword_a', '').strip()
        keyword_b = request.form.get('keyword_b', '').strip()

        if not keyword_a or not keyword_b:
            flash('Please enter both keywords to compare.', 'warning')
        else:
            posts_a = list(app.db.posts.find({
                'case_id': cid,
                'text': {'$regex': re.escape(keyword_a), '$options': 'i'}
            }))
            posts_b = list(app.db.posts.find({
                'case_id': cid,
                'text': {'$regex': re.escape(keyword_b), '$options': 'i'}
            }))

            results = compare_brands(posts_a, posts_b, keyword_a, keyword_b)
            winners = get_winner(results[keyword_a], results[keyword_b], keyword_a, keyword_b)

            metrics = ['post_count', 'total_likes', 'total_retweets', 'avg_engagement']
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=keyword_a,
                x=metrics,
                y=[results[keyword_a][m] for m in metrics]
            ))
            fig.add_trace(go.Bar(
                name=keyword_b,
                x=metrics,
                y=[results[keyword_b][m] for m in metrics]
            ))
            fig.update_layout(
                title=f"Comparison: {keyword_a} vs {keyword_b}",
                barmode='group',
                height=400
            )
            chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            for brand, stats in results.items():
                if stats['total_likes'] + stats['total_retweets'] > 0:
                    pie_fig = go.Figure(go.Pie(
                        labels=['Likes', 'Retweets'],
                        values=[stats['total_likes'], stats['total_retweets']],
                        title=f"{brand} Engagement Breakdown"
                    ))
                    pie_charts[brand] = json.dumps(pie_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('competitor.html',
        results=results,
        chart_json=chart_json,
        pie_charts=pie_charts,
        winners=winners
    )