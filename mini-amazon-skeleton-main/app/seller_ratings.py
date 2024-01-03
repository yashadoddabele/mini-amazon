from flask import app, jsonify, render_template, redirect, request, url_for, flash, current_app, session
from flask_login import current_user, login_required
from flask import Blueprint
from .models.productcategories import Category
from .models.sellerInventory import SellerInventory
from .models.product import Product
from  .models.sellerRating import SellerRating  

bp = Blueprint('seller_ratings', __name__)  # Create a Blueprint instance

@bp.route('/seller/<int:seller_id>/rate', methods=['POST'])
def rate_seller(seller_id):
    rating = request.form.get('rating')
    review = request.form.get('review')
    # Add check for current_user and add rating
    if current_user.is_authenticated:
        try:
            SellerRating.add_rating(seller_id, current_user.id, rating, review)
            return jsonify({'message': 'Rating added successfully'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 409
        except Exception as e:
            current_app.logger.error(f"Failed to add rating: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401


@bp.route('/seller/<int:seller_id>/ratings', methods=['GET'])
def get_seller_ratings(seller_id):
    ratings = SellerRating.get_ratings_and_reviews(seller_id)
    return jsonify(ratings)

@bp.route('/seller/<int:seller_id>/reviews', methods=['GET'])
@login_required  # Ensure only logged in users can access this page
def seller_reviews(seller_id):
        # Check if the current user is the seller or has permission to view this page
        if current_user.id != seller_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        anonymous_seller_reviews = SellerRating.get_anonymous_ratings_and_reviews(seller_id)
        anonymous_product_reviews = SellerInventory.get_anonymous_product_reviews_for_seller(seller_id)
        # Render a template passing the reviews and ratings
        return render_template('seller_ratings.html', anonymous_product_reviews=anonymous_product_reviews, anonymous_seller_reviews=anonymous_seller_reviews)
   