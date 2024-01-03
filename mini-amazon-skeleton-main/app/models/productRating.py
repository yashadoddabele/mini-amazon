from flask import current_app as app
from datetime import datetime
from sqlalchemy import text
from . import sellerInventory as seller_inventory
from . import order as OrderItems
from sqlalchemy import text


class ProductRating:

    @staticmethod
    def add_rating(product_id, buyer_id, rating, review):
        try:
            app.db.execute('''
                INSERT INTO ProductRatings(product_id, buyer_id, rating, review)
                VALUES(:product_id, :buyer_id, :rating, :review)
            ''',
            product_id=product_id,
            buyer_id=buyer_id,
            rating=rating,
            review=review)
            app.db.commit()
        except Exception as e:
            app.logger.error(f"Failed to add rating to ProductRatings: {str(e)}")
            app.db.rollback()
            raise

        
    @staticmethod
    def get_average_rating(product_id):
        # SQL query to calculate the average rating for a product
        rows = app.db.execute('''
            SELECT AVG(rating)
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_reviews(product_id):
        # SQL query to get all reviews for a product
        rows = app.db.execute('''
            SELECT review
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_ratings(product_id):
        # SQL query to get all ratings for a product
        rows = app.db.execute('''
            SELECT rating
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_ratings():
        # SQL query to get all ratings for all products
        rows = app.db.execute('''
            SELECT product_id, rating
            FROM ProductRatings
        ''')
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_reviews():
        # SQL query to get all reviews for all products
        rows = app.db.execute('''
            SELECT product_id, review
            FROM ProductRatings
        ''')
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_ratings_and_reviews():
        # SQL query to get all ratings and reviews for all products
        rows = app.db.execute('''
            SELECT product_id, rating, review
            FROM ProductRatings
        ''')
        return rows[0][0] if rows else None
    @staticmethod  
    def get_all_ratings_and_reviews_for_product(product_id):
        # SQL query to get all ratings and reviews for a product
        rows = app.db.execute('''
            SELECT product_id, rating, review
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_ratings_and_reviews_for_buyer(buyer_id):
        # SQL query to get all ratings and reviews for a buyer
        rows = app.db.execute('''
            SELECT product_id, rating, review
            FROM ProductRatings
            WHERE buyer_id = :buyer_id
        ''',
        buyer_id=buyer_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_ratings_and_reviews_for_seller(seller_id):
        # SQL query to get all ratings and reviews for a seller
        rows = app.db.execute('''
            SELECT product_id, rating, review
            FROM ProductRatings
            WHERE seller_id = :seller_id
        ''',
        seller_id=seller_id)
        return rows[0][0] if rows else None
    @staticmethod
    def get_all_ratings_and_reviews_for_product_and_buyer(product_id, buyer_id):
        # SQL query to get all ratings and reviews for a product and buyer
        rows = app.db.execute('''
            SELECT product_id, rating, review
            FROM ProductRatings
            WHERE product_id = :product_id AND buyer_id = :buyer_id
        ''',
        product_id=product_id, buyer_id=buyer_id)
        return rows[0][0] if rows else None
    
    
    @staticmethod
    def get_product_rating(product_id):
        # SQL query to get a product rating
        rows = app.db.execute('''
            SELECT rating
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_product_review(product_id):
        # SQL query to get a product review
        rows = app.db.execute('''
            SELECT review
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_ratings_and_reviews(product_id):
        rows = app.db.execute('''
            SELECT rating, review
            FROM ProductRatings
            WHERE product_id = :product_id
        ''', product_id=product_id)
        return [{'rating': row[0], 'review': row[1]} for row in rows]