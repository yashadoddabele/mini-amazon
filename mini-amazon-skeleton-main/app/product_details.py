from flask import render_template, session
from flask_login import current_user
import datetime

from .models.product import Product
from .models.cart_items import CartItems
from .models.productcategories import Category
from .models.sellerInventory import SellerInventory
from .models.order import Order, OrderItems

from flask import Blueprint
from flask import request

bp = Blueprint('product_details', __name__, url_prefix='/product_details')

@bp.route('/<int:product_id>', methods=['GET', 'POST'])
def product_details(product_id):
    product = Product.get(product_id) #gets specific product
    categories = Category.get_all() #gets categories for nav bar 
    message = None
    reviews = Product.get_ratings_and_reviews(product_id) #gets reviews for specific product

    similar_products = Product.get_similar_products(product_id) #to populate the similar products scrolling view
    other_category_products = Product.get_other_products_in_this_category(product_id) #to populate the other products in category scrolling view
    category_name = Category.get_category_name_by_product_id(product_id)
    keyword = request.args.get('search_input') #gets keyword from search
    category_id = request.args.get('category_input')
    all_sellers = SellerInventory.get_all_sellers_for_product(product_id)

    #calculates average rating
    average_rating = Product.get_average_rating(product_id)
    print(average_rating)

    if average_rating is not None:
        avg_rating = average_rating
    else:
        avg_rating = "There are no reviews for this product"

    if current_user.is_authenticated:
        user_has_ordered_product = OrderItems.has_user_ordered_product(current_user.id, product_id)
    else: 
        user_has_ordered_product = False
    
    #handles adding to cart
    if current_user.is_authenticated:
        if request.method == 'POST':
            quantity = int(request.form['order_q'])
            result = CartItems.add_item_to_cart(current_user.id, product_id, quantity)
            if result == "success":
                message = "Successfully added to cart!"
            elif result == "no_inventory":
                message = "Unable to add product to cart. Product not being sold."
            elif result == "failure":
                message = "Unable to add product to cart. Product not available."

    else:
        message = "Sorry, you have to log in to add this to your cart."
    
    if product:
        return render_template('product_details.html', product=product, product_id=product_id, reviews=reviews, message=message, categories=categories, all_sellers=all_sellers, other_category_products=other_category_products, similar_products=similar_products, category_name=category_name, keyword=keyword, category_id=category_id, user_has_ordered_product=user_has_ordered_product, avg_rating=avg_rating)
    return "Product not found", 404  # Or handle it as you see fit
