from flask import Blueprint, redirect, render_template, jsonify, request, url_for, flash
from flask_login import login_required, current_user
from .models.sellerOrders import SellerOrders
from .models.order import Order, OrderItems
from .models.user import User
from flask import current_app as app
from datetime import datetime


bp = Blueprint('seller_orders', __name__, url_prefix='/seller/orders')

@bp.route('/')
@login_required
def orders(): #get all orders of a seller
    pending_orders = SellerOrders.get_pending_orders_by_seller(current_user.id)
    pending_info = []
    for pend in pending_orders:
        buyer_info = User.get(pend.buyer_id)
        pend.order_date = pend.order_date.strftime('%Y-%m-%d %H:%M:%S')
        pending_info.append(buyer_info)
    fulfilled_orders = SellerOrders.get_fulfilled_orders_by_seller(current_user.id)
    full_info = []
    for full in fulfilled_orders:
        buyer_info = User.get(full.buyer_id)
        full.order_date = full.order_date.strftime('%Y-%m-%d %H:%M:%S')
        full_info.append(buyer_info)

    p_info = zip(pending_orders, pending_info)
    f_info = zip(fulfilled_orders, full_info)
    return render_template('sellerOrders.html', p_info = p_info, f_info=f_info)

@bp.route('/<int:item_id>/fulfill', methods=['POST'])
@login_required
def fulfill_order_route(item_id): #fulfill an order
    try:
        if SellerOrders.fulfill_order(item_id, current_user.id):
            return jsonify({'success': True, 'message': 'Order fulfilled successfully', 'item_id': item_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to fulfill the order.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fulfill the order: ' + str(e)})

@bp.route('/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id): #delete an order
    try:
        if SellerOrders.delete_order(order_id, current_user.id):
            return jsonify({'success': True, 'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



@bp.route('/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order_route(order_id):
    try:
        if SellerOrders.delete_order(order_id, current_user.id):
            return jsonify({'success': True, 'message': 'Order deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to delete the order'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
