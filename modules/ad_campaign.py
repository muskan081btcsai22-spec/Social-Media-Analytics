"""
Ad Campaign Optimization Module

This module provides functions to calculate key performance metrics for ad campaigns
and compare multiple campaigns.
"""


def calculate_metrics(impressions, clicks, conversions, ad_spend, revenue):
    """
    Calculate key ad campaign metrics.

    Args:
        impressions (float): Number of ad impressions
        clicks (float): Number of ad clicks
        conversions (float): Number of conversions
        ad_spend (float): Total ad spend in currency units
        revenue (float): Total revenue generated in currency units

    Returns:
        dict: Dictionary containing CTR, Conversion_Rate, ROI, CPA, CPM
              Returns empty dict if impressions or clicks are 0
    """
    if impressions == 0 or clicks == 0:
        return {}

    ctr = (clicks / impressions) * 100
    conversion_rate = (conversions / clicks) * 100
    roi = ((revenue - ad_spend) / ad_spend) * 100 if ad_spend != 0 else 0
    cpa = ad_spend / conversions if conversions != 0 else 0
    cpm = (ad_spend / impressions) * 1000

    return {
        'CTR': round(ctr, 2),
        'Conversion_Rate': round(conversion_rate, 2),
        'ROI': round(roi, 2),
        'CPA': round(cpa, 2),
        'CPM': round(cpm, 2)
    }


def compare_campaigns(campaign_a, campaign_b):
    """
    Compare two ad campaigns by calculating their metrics.

    Args:
        campaign_a (dict): Campaign data with keys: name, impressions, clicks, conversions, ad_spend, revenue
        campaign_b (dict): Campaign data with keys: name, impressions, clicks, conversions, ad_spend, revenue

    Returns:
        dict: Dictionary with metrics for both campaigns
    """
    metrics_a = calculate_metrics(
        campaign_a['impressions'],
        campaign_a['clicks'],
        campaign_a['conversions'],
        campaign_a['ad_spend'],
        campaign_a['revenue']
    )
    metrics_b = calculate_metrics(
        campaign_b['impressions'],
        campaign_b['clicks'],
        campaign_b['conversions'],
        campaign_b['ad_spend'],
        campaign_b['revenue']
    )

    return {
        'campaign_a': {
            'name': campaign_a['name'],
            'metrics': metrics_a
        },
        'campaign_b': {
            'name': campaign_b['name'],
            'metrics': metrics_b
        }
    }