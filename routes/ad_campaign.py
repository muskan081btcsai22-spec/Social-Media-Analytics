from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from flask import current_app as app
import plotly.graph_objects as go
import plotly.utils
import json
from modules.ad_campaign import calculate_metrics

ad_bp = Blueprint('ad', __name__)


@ad_bp.route('/ads', methods=['GET', 'POST'])
@login_required
def ads_page():
    metrics = {}
    chart_json = None

    if request.method == 'POST':
        try:
            impressions = float(request.form.get('impressions', 0))
            clicks = float(request.form.get('clicks', 0))
            conversions = float(request.form.get('conversions', 0))
            ad_spend = float(request.form.get('ad_spend', 0))
            revenue = float(request.form.get('revenue', 0))

            metrics = calculate_metrics(impressions, clicks, conversions, ad_spend, revenue)

            if metrics:
                # Create bar chart for metrics
                labels = list(metrics.keys())
                values = list(metrics.values())
                colors = ['green' if metrics['ROI'] > 0 else 'red'] + ['blue'] * 4

                fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors))
                fig.update_layout(
                    title="Campaign Metrics",
                    xaxis_title="Metric",
                    yaxis_title="Value",
                    height=400
                )
                chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            else:
                flash('Invalid input: Impressions and clicks must be greater than 0.', 'danger')

        except ValueError:
            flash('Invalid input: Please enter valid numbers.', 'danger')

    return render_template('ad_campaign.html', metrics=metrics, chart_json=chart_json)