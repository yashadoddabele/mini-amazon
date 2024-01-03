from flask import current_app as app, render_template
from datetime import datetime
from flask_login import current_user, login_required
from sqlalchemy import text
from . import sellerInventory as seller_inventory
from . import order as OrderItems
from sqlalchemy import text
from .order import OrderItems


class SellerRating:
    def __init__(self, seller_id, buyer_id, rating, review):
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.rating = rating
        self.review = review
   
    @staticmethod
    def add_rating(seller_id, buyer_id, rating, review):
        # SQL query to insert a seller rating into the database
        try:
            app.db.execute('''
                INSERT INTO SellerRating(seller_id, buyer_id, rating, review)
                VALUES(:seller_id, :buyer_id, :rating, :review)
            ''',
            seller_id=seller_id,
            buyer_id=buyer_id,
            rating=rating,
            review=review)
            # Assuming app.db.execute does not auto-commit
            app.db.commit()
        except Exception as e:
            app.logger.error(f"Failed to add rating to SellerRating: {str(e)}")
            app.db.rollback()
            raise
        
            
    @staticmethod
    def get_average_rating(seller_id):
            # SQL query to calculate the average rating for a seller
            rows = app.db.execute('''
                SELECT AVG(rating)
                FROM SellerRating
                WHERE seller_id = :seller_id
            ''',
            seller_id=seller_id)
            return rows[0][0] if rows else None
    
    @staticmethod
    def get_reviews(seller_id):
        # SQL query to get all reviews for a seller
        rows = app.db.execute('''
            SELECT review
            FROM SellerRating
            WHERE seller_id = :seller_id
        ''',
        seller_id=seller_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_ratings(seller_id):
        # SQL query to get all ratings for a seller
        rows = app.db.execute('''
            SELECT rating
            FROM SellerRating
            WHERE seller_id = :seller_id
        ''',
        seller_id=seller_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_ratings_and_reviews(seller_id):
        rows = app.db.execute('''
            SELECT rating, review
            FROM SellerRatings
            WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'rating': row[0], 'review': row[1]} for row in rows]
    
            
    @staticmethod
    def get_ratings_and_reviews(seller_id):
        # SQL query to get all seller ratings and reviews
        rows = app.db.execute('''
            SELECT rating, review
            FROM SellerRatings
            WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'rating': row[0], 'review': row[1]} for row in rows]
    
    @staticmethod
    def get_anonymous_ratings_and_reviews(seller_id):
        rows = app.db.execute('''
            SELECT rating, review, 'A buyer' as buyer
            FROM SellerRatings
            WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'rating': row[0], 'review': row[1], 'buyer': row[2]} for row in rows]

    

    