from flask import app, render_template, redirect
from flask_login import current_user, login_required
from flask import Blueprint
from .models.order import Order, OrderItems
from .models.cart_items import CartItems
from .models.sellerInventory import SellerInventory
from .models.sellerOrders import SellerOrders
from .models.user import User
from flask import jsonify, request, url_for, current_app as app
from flask import session
from datetime import datetime

from flask import Blueprint
bp = Blueprint('order', __name__)

# Facilitates getting all items from the order, and putting the correct results
@bp.route('/cart/order/<int:oid>', methods=['GET'])
def get_order(oid):
    if current_user.is_authenticated:
        try: 
            order = Order.get_ord(oid)
            status = []
            toUpdate = []
            updateInventory = True
            fulfilled = order.fulfilled
            processed = order.processed

            # the order has already been placed: don't run the retrieval again
            if processed or fulfilled:
                return redirect(url_for('order.show_order', oid=oid))
            elif order.date is not None:
                return redirect(url_for('order.show_order', oid=oid))

            items = OrderItems.get_items(oid)
            total_price = OrderItems.get_totalprice(oid)
            
            # if the user doesn't have the funds to pay the cart
            if current_user.account_balance < total_price:
                print(current_user.account_balance)
                print("less")
                fulfilled = False
                date = "Not Fulfilled"
                # set processed and fulfilled status to false
                processed = False
                status.append("Insufficient account balance to fulfill this order.")
                Order.update_date(oid, datetime.now())
                return render_template('order.html',
                    items=items, total_price=total_price, fulfilled=fulfilled, date=date, status=status)

             
            fulfilled = True
            processed = True

            for item in items:
                name = item.name
                quantity = item.quantity
                price = item.price
                pid = item.pid
                item_id = item.id
                seller_info = SellerInventory.find_seller_for_item(pid)

                # Finds seller for the item
                if seller_info:
                    seller = seller_info.seller_id
                    sell_quant = seller_info.quantity

                    # If quantity of the item is more than the inventory of the seller, cannot fulfill/process order
                    if quantity > sell_quant and updateInventory:
                        fulfilled = False
                        date = "Not Fulfilled"
                        status.append("We're sorry, but your item: " + name + " is not available in your requested quantity.")
                        processed = False

                    # Else, we can update the inventory
                    else:
                        toUpdate.append([seller, pid, sell_quant, item_id, price, quantity]) 
                else:
                    fulfilled = False
                    date = "Not Fulfilled"
                    status.append("We're sorry, but your item: " + name + " is not currently being sold.")
                    processed = False
            

            if fulfilled:
                fulfilled = False
                status.append("Order placed, thank you!")
                #Order has been processed by this point
                processed = True
                # Decrease the user's balance by the total price
                current_user.change_account_balance(-total_price)
                # Update order date to be the process date
                Order.update_date(oid, datetime.now())
                order = Order.get_ord(oid)
                date = "Placed on " + order.date.strftime("%Y-%m-%d")

                # Delete cart items
                CartItems.delete_all_rows(current_user.id)
                # Remove items from inventory
                if updateInventory:
                    for update in toUpdate:
                        SellerInventory.update_item(update[0], update[1], update[2]-update[5])
                        # Update seller's balance
                        seller = SellerInventory.find_seller_for_item(update[1])
                        seller_id = seller.seller_id
                        seller_user = User.get(seller_id)
                        seller_user.change_account_balance(update[5]*update[4])
                        # Upon ordering/updating item, create a seller order
                        buyer_info = User.get(current_user.id)

                        p = SellerOrders.create_seller_order_entry(update[0], update[3], order.date, 
                        OrderItems.get_totalprice(oid), OrderItems.get_num_items(oid), current_user.id)
                        print(p)


            Order.update_date(oid, datetime.now())
            Order.update_processed(oid, processed)

            # Finally, display page
            return render_template('order.html',
                                   items=items, total_price=total_price,
                                   fulfilled=fulfilled, date=date, status=status)
        except Exception as e:
            app.db.rollback()
            app.logger.error(f"Failed to retrieve order: {str(e)}")
            return jsonify({'error': str(e)}), 400

    else:
        return redirect('/login')

# Route to show the cart orders after it has been processed, preventing duplicate inventory/balance changes
@bp.route('/cart/order/<int:oid>/details', methods=['GET'])
def show_order(oid):
    if current_user.is_authenticated:
        try:
            order = Order.get_ord(oid)
            items = OrderItems.get_items(oid)
            total_price = OrderItems.get_totalprice(oid)
            fulfilled = order.fulfilled
            processed = order.processed
            if fulfilled:
                status = ["Order fulfilled, thank you!"]
                date = "Fulfilled on " + order.date.strftime("%Y-%m-%d")
            elif processed:
                 status = ["Order processed, thank you!"]
                 date = "Placed on " + order.date.strftime("%Y-%m-%d")
            else:
                status = ["We're sorry, your order could not be placed."]
                date = "Not fulfilled"

            return render_template('order.html',
                                   items=items, total_price=total_price,
                                   fulfilled=fulfilled, date=date, status=status)
        except Exception as e:
            app.logger.error(f"Failed to retrieve order: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return redirect('/login')

# Route that creates an order after the Place Order button is pressed
@bp.route('/cart/place_order', methods=['POST'])
def place_order():
    print("placing")
    try:
        if current_user.is_authenticated:
            items = CartItems.get_items(current_user.id) 
            # Create order
            oid = Order.create_order(current_user.id)

            # Add cart items to the order
            bol = OrderItems.add_items_to_order(oid, items)

            if oid:
                print("good")
                # Redirect to populate the order information
                return redirect(url_for('order.get_order', oid=oid))
            else:
                
                return jsonify({'message': 'Unable to place order'}), 200

        else:
            return redirect('/login')
    except Exception as e:
        print("bad")
        app.db.rollback()
        app.logger.error(f"Failed to retrieve order: {str(e)}")
        return jsonify({'error': str(e)}), 400

