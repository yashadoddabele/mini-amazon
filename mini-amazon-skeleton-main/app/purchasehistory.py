from flask import render_template, redirect, url_for, flash
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.order import Order, OrderItems


from flask import Blueprint
from flask import request

bp = Blueprint('purchasehistory', __name__)

@bp.route('/purchasehistory')
def purchasehistory():
    if current_user.is_authenticated:
        # Get the sort_by and filter_type parameters from the request
        sort_by = request.args.get('sort_by', 'time_purchased')
        filter_type = request.args.get('filter_type', 'all')

        # Retrieve purchase history with the specified sort and filter criteria
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0), sort_by=sort_by)
        
        # Filter purchases based on total price
        purchases = Purchase.filter_by_total_price(purchases, filter_type)

        #handles populating the scrolling view for similar products
        most_recent_product_id = OrderItems.get_most_recent_purchase(current_user.id)
        similar_products = Product.get_similar_products(most_recent_product_id)
        most_recent_product_name = Product.get_product_name(most_recent_product_id)
        
    else:
        return redirect(url_for('users.login'))
    
    return render_template('history.html',
                           purchase_history=purchases, similar_products=similar_products, most_recent_product_name=most_recent_product_name)
