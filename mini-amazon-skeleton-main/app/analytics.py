from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from .models.analytics import Analytics

bp = Blueprint('analytics', __name__, url_prefix='/seller/analytics')

@bp.route('/')
@login_required
def analytics_dashboard():
    seller_id = current_user.id
    inventory_data = Analytics.get_inventory_status(seller_id)
    pending_order_items_count = Analytics.get_pending_order_items_count(seller_id)
    fulfilled_order_items_count = Analytics.get_fulfilled_order_items_count(seller_id)

    # Make sure the data is being retrieved correctly
    print("Inventory Data:", inventory_data)
    print("Pending Order Items Count:", pending_order_items_count)
    print("Fulfilled Order Items Count:", fulfilled_order_items_count)

    return render_template('analytics.html',
                           inventory_data=inventory_data,
                           pending_order_items_count=pending_order_items_count,
                           fulfilled_order_items_count=fulfilled_order_items_count)

@bp.route('/total_revenue')
@login_required
def total_revenue():
    seller_id = current_user.id
    revenue = Analytics.get_total_revenue(seller_id)
    return jsonify({'total_revenue': revenue})