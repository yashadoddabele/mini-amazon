from flask import current_app as app

# A wrapper class for the ProductCategories database
class Category:
    def __init__(self, id, category_name):
        self.id = id
        self.category_name = category_name

    # given a category id, this method gets the category information
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, category_name
            FROM ProductCategories
            WHERE id = :id
            ''',
            id=id)
        return Category(*(rows[0])) if rows else None

    # based on a category id this method returns the category name
    @staticmethod
    def get_category_name(id):
        rows = app.db.execute('''
            SELECT category_name
            FROM ProductCategories
            WHERE id = :id
            ''',
            id=id)
        return rows[0][0] if rows else None

    # this method gets all the product categories
    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT id, category_name
            FROM ProductCategories
            ''')
        return [Category(*row) for row in rows]
    
    # this method gets the name of a category that a given product belongs to 
    @staticmethod
    def get_category_name_by_product_id(product_id):
        rows = app.db.execute('''
            SELECT c.category_name
            FROM ProductCategories c
            JOIN Products p ON c.id = p.category_id
            WHERE p.id = :product_id
        ''', product_id=product_id)

        return rows[0][0] if rows else None