from flask import app, jsonify, render_template, redirect, request, url_for, flash, current_app, session
from flask_login import current_user, login_required
from flask import Blueprint
from .models.productcategories import Category
from .models.sellerInventory import SellerInventory
from .models.product import Product  

bp = Blueprint('sellerInventory', __name__)

@bp.route('/seller/inventory')
def inventory(): #inventory of a seller
    if current_user.is_authenticated:
        inventory_data = SellerInventory.get_all_by_seller(current_user.id)
        categories = Category.get_all()  
        return render_template('sellerInventory.html', inventory_data=inventory_data, categories=categories)
    else:
        return redirect(url_for('users.login'))

def get_seller_id_from_session():
    return session.get('seller_id')

@bp.route('/seller/inventory/add', methods=['POST'])
def add_inventory_item(): #add item to seller inventory
    if current_user.is_authenticated:
        try:
            product_id = int(request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))
            SellerInventory.add_item(current_user.id, product_id, quantity)
            return jsonify({'message': 'Inventory item added successfully'}), 200
        except ValueError as e:  
            return jsonify({'error': str(e)}), 409  
        except Exception as e:
            current_app.logger.error(f"Failed to add inventory item: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('/seller/inventory/update', methods=['POST'])
def update_inventory_item(): #update quantity of item in seller inventory
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401

    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    if not product_id or not quantity:
        return jsonify({'error': 'Product ID and quantity are required.'}), 400

    try:
        product_id = int(product_id)
        quantity = int(quantity)
        updated_rows = SellerInventory.update_item(current_user.id, product_id, quantity)
        if updated_rows is None:
            return jsonify({'error': 'Inventory item does not exist.'}), 404
        elif updated_rows > 0:
            return jsonify({'message': 'Inventory updated successfully'}), 200
        else:
            return jsonify({'error': 'No inventory was updated. Please check your input.'}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating inventory: {str(e)}")
        return jsonify({'error': str(e)}), 500


@bp.route('/seller/inventory/delete', methods=['POST'])
def delete_inventory_item(): #delete item from seller inventory
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is required.'}), 400

    try:
        product_id = int(product_id)
        rows_deleted = SellerInventory.delete_item(current_user.id, product_id)
        
        if rows_deleted is None:
            return jsonify({'error': 'Failed to delete inventory item.'}), 500
        elif rows_deleted > 0:
            return jsonify({'message': 'Item deleted successfully.', 'status': 'success'})
        else:
            return jsonify({'message': 'No item found to delete.', 'status': 'fail'})
    except Exception as e:
        current_app.logger.error(f"Error deleting inventory item: {str(e)}")
        return jsonify({'error': str(e)}), 500



@bp.route('/seller/inventory/add_new_product', methods=['POST'])
def add_new_product(): #add new product to seller inventory
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized', 'status': 'fail'}), 401
    
    name = request.form.get('name')
    price = request.form.get('price')
    available = request.form.get('available') == 'true'
    short_description = request.form.get('short_description')
    long_description = request.form.get('long_description')
    category_id = request.form.get('category_id')
    
    try:
        new_product_id = SellerInventory.create_new_product(
            name, float(price), available, short_description, long_description, category_id)
        
        if new_product_id is not None:
            SellerInventory.add_item(current_user.id, new_product_id, 0)
            return jsonify({'message': 'New product added successfully', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Failed to add new product', 'status': 'fail'}), 400
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400
    

@bp.route('/seller/inventory/product-sales-data')
@login_required
def product_sales_data(): #get sales data for a product
    sales_data = SellerInventory.get_product_sales_data(current_user.id)
    return jsonify(sales_data)


