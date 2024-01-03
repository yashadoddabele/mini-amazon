from flask import current_app as app
from .productcategories  import Category

# A wrapper class for the Products database
class Product:
    def __init__(self, id, name, price, available, short_description, long_description, category_id):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.short_description = short_description
        self.long_description = long_description
        self.category_id = category_id

    # this function gets the product information for a given product id
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            WHERE id = :id
            ''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    # this method just gets the product name given a product id
    @staticmethod
    def get_product_name(id):
        rows = app.db.execute('''
            SELECT name
            FROM Products
            WHERE id = :id
        ''', id=id)
        
        return rows[0][0] if rows else None

    # this method gets all products
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            WHERE available = :available
            ''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_top_k_expensive(k):
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            ORDER BY price DESC
            LIMIT :k
            ''', 
                            k = k )
        return [Product(*row) for row in rows]
    

    @staticmethod
    def add_new_product(name, price):
        try:
            sql_query = """
                INSERT INTO Products (name, price)
                VALUES (:name, :price)
                RETURNING id
            """
            result = app.db.execute(sql_query, name=name, price=price)
            app.db.commit()
            return result[0][0]
        except Exception as e:
            app.db.rollback()
            print(str(e))
            return None


    @staticmethod
    def search_by_keyword(keyword):
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            WHERE name ILIKE :keyword
        ''', keyword=f"%{keyword}%")

        return [Product(*row) for row in rows]

    @staticmethod
    def get_products_by_category(category_id):
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            WHERE available = TRUE AND category_id = :category_id
        ''', category_id=category_id)

        return [Product(*row) for row in rows]

    # this method gets 10 products in the same category as a given product
    @staticmethod
    def get_other_products_in_this_category(product_id):
        current_product = Product.get(product_id)
        if current_product is None:
            return None
        category_id = current_product.category_id
        rows = app.db.execute('''
            SELECT id, name, price, available, short_description, long_description, category_id
            FROM Products
            WHERE available = TRUE AND category_id = :category_id AND id != :product_id
            LIMIT 10
        ''', category_id=category_id, product_id=product_id)
        return [Product(*row) for row in rows]

    # this method gets 10 products that are similar to a given product based on the words used in the product name, similar meaning one or more words match the keywords
    @staticmethod
    def get_similar_products(product_id):
        current_product = Product.get(product_id)
        if current_product is None:
            return None
        keywords = current_product.name.split()
        query = ' OR '.join(['name ILIKE :keyword{}'.format(i) for i in range(len(keywords))])
        where_clause = f"({' AND '.join([query] * len(keywords))}) AND available = TRUE AND id != :current_product_id"
        rows = app.db.execute(f'''
        SELECT id, name, price, available, short_description, long_description, category_id
        FROM Products
        WHERE {where_clause}
        LIMIT 10
        ''', **{f'keyword{i}': f"%{keyword}%" for i, keyword in enumerate(keywords)}, current_product_id=current_product.id)
        return [Product(*row) for row in rows]
    
    # this product gets all the product categories
    @staticmethod
    def get_all_categories():
        rows = app.db.execute('''
            SELECT id, name
            FROM Categories
        ''')
        return [Category(*row) for row in rows]
    
    @staticmethod
    def get_ratings(product_id):
        rows = app.db.execute('''
            SELECT rating
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_reviews(product_id):
        rows = app.db.execute('''
            SELECT review
            FROM ProductRatings
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def get_seller(product_id):
        rows = app.db.execute('''
            SELECT seller_id
            FROM SellerInventory
            WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return rows[0][0] if rows else None
    

    @staticmethod
    def get_ratings_and_reviews(product_id):
        rows = app.db.execute('''
            SELECT pr.rating, pr.review, u.firstname, u.lastname, pr.buyer_id
            FROM ProductRatings pr  -- Make sure this matches the actual table name
            JOIN Users u ON pr.buyer_id = u.id
            WHERE product_id = :product_id
        ''', product_id=product_id)

        app.logger.info('Retrieved rows: %s', rows)  # Log the fetched rows for debugging

        return [{'rating': row[0], 'review': row[1], 'buyer': f"{row[2]} {row[3]}", 'buyer_id': row[4]} for row in rows]

    # this method gets all of the reviews for a specific products and returns the average rating
    @staticmethod
    def get_average_rating(product_id):
        rows = app.db.execute('''
            SELECT ROUND(AVG(rating), 1) as average_rating
            FROM ProductRatings
            WHERE product_id = :product_id
        ''', product_id=product_id)

        return rows[0][0] if rows and rows[0][0] is not None else None

    @staticmethod
    def update_availability(product_id, new_available):
        try:
            app.db.execute('''
                UPDATE Products
                SET available = :new_available
                WHERE id = :product_id
            ''', product_id=product_id, new_available=new_available)
            app.db.commit()
            return True
        except Exception as e:
            app.logger.error(f"Failed to update availability: {str(e)}")
            return False