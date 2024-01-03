from flask import jsonify, request, current_app
from flask_login import current_user
from .models.productRating import ProductRating
from flask import Blueprint

bp = Blueprint('product_ratings', __name__)

@bp.route('/product/<int:product_id>/rate', methods=['POST'])
def rate_product(product_id):
    rating = request.form.get('rating')
    review = request.form.get('review')
    if current_user.is_authenticated:
        try:
            ProductRating.add_rating(product_id, current_user.id, rating, review)
            return jsonify({'message': 'Product rating added successfully'}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to add product rating: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401


@bp.route('/product/<int:product_id>/ratings', methods=['GET'])
def get_product_ratings(product_id):
    ratings = ProductRating.get_ratings_and_reviews(product_id)
    return jsonify(ratings)


@bp.route('/product/<int:product_id>/rating', methods=['GET'])
def get_product_rating(product_id):
    if current_user.is_authenticated:
        try:
            rating = ProductRating.get_product_rating(product_id)
            return jsonify({'message': 'Rating retrieved successfully'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 409
        except Exception as e:
            current_app.logger.error(f"Failed to get rating: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401