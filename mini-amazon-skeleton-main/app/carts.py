from flask import app, render_template
from .models.cart_items import CartItems
from flask_login import current_user
from flask import jsonify
from flask import request, redirect, url_for, make_response

from flask import Blueprint
bp = Blueprint('cart', __name__)

# Route to get and display all cart items
@bp.route('/cart')
def get_user_cart():
    if current_user.is_authenticated:
        items = CartItems.get_items(current_user.id)
        total_price = CartItems.get_totalprice(current_user.id)
        #Makes sure an unauthorized user cannot access the carts page with the back button
        response = make_response(render_template('cart.html', items=items, total_price=total_price))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    else:
        return redirect(url_for('users.login'))

# Updates the contents of the cart
@bp.route('/cart/update/', methods=['POST'])
def update_cart():
    if current_user.is_authenticated:
        try:
            id = request.form.get('id')
            # Gets the quantity input by the user
            new_quantity = int(request.form.get('new_quantity'))

            #call update method
            CartItems.update_quantity(id, new_quantity)
            new_total = CartItems.get_totalprice(current_user.id)
            return jsonify({'message': 'Successfully updated', 'total_price': new_total})
        except Exception as e:
            app.db.rollback()
            return jsonify({'message': 'Error updating'})

# Deletes item from cart
@bp.route('/cart/delete/', methods=['POST'])
def delete_cart_item():
    if current_user.is_authenticated:
        try:
            # Finds which item the user pressed the delete button for
            id = request.form.get('id')
            if id:
                deleted = CartItems.delete_row(id)
                if deleted:
                    return jsonify({'message': 'Item deleted successfully.', 'status': 'success'})
            else:
                return jsonify({'message': 'No item found to delete.', 'status': 'fail'})
        except Exception as e:
            app.db.rollback()
            return jsonify({'message': 'Error deleting'})