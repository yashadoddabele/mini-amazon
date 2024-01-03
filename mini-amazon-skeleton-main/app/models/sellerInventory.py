from flask import current_app as app
from .product import Product

class SellerInventory:
    def __init__(self, id, seller_id, product_id, quantity):
        self.id = id
        self.seller_id = seller_id
        self.product_id = product_id
        self.quantity = quantity
    
    # get all sellers of a product
    @staticmethod
    def get_seller_for_product(product_id):
        rows = app.db.execute('''
            SELECT seller_id
            FROM SellerInventory
            WHERE product_id = :product_id
        ''', product_id=product_id)

        return rows[0][0] if rows else None        

    #get all products of a seller and a product
    @staticmethod
    def get_by_seller_and_product(seller_id, product_id):
        rows = app.db.execute('''
            SELECT id, seller_id, product_id, quantity
            FROM SellerInventory
            WHERE seller_id = :seller_id
            AND product_id = :product_id
        ''',
        seller_id=seller_id,
        product_id=product_id)
        return SellerInventory(*(rows[0])) if rows else None

    #get all products of a seller
    @staticmethod
    def get_all_by_seller(seller_id):
        rows = app.db.execute('''
            SELECT id, seller_id, product_id, quantity
            FROM SellerInventory
        WHERE seller_id = :seller_id
        ''',
        seller_id=seller_id)
        return [SellerInventory(*row) for row in rows]

    #get product reviews 
    @staticmethod
    def get_product_reviews_for_seller(seller_id):
        rows = app.db.execute('''
            SELECT pr.product_id, p.name, pr.rating, pr.review
            FROM ProductRatings pr
            JOIN Products p ON pr.product_id = p.id
            JOIN SellerInventory si ON p.id = si.product_id
            WHERE si.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'product_id': row[0], 'product_name': row[1], 'rating': row[2], 'review': row[3]} for row in rows]

    # add item to seller inventory
    @staticmethod
    def add_item(seller_id, product_id, quantity):
        try:
            existing_item = SellerInventory.get_by_seller_and_product(seller_id, product_id)
            if existing_item:
                existing_item.quantity += quantity
                return existing_item.update_item(seller_id, product_id, existing_item.quantity)
            else:
                rows = app.db.execute('''
                    INSERT INTO SellerInventory(seller_id, product_id, quantity)
                    VALUES(:seller_id, :product_id, :quantity)
                ''',
                seller_id=seller_id,
                product_id=product_id,
                quantity=quantity)

                b=Product.update_availability(product_id, True)
                app.db.commit()

                return True  # Indicate success
        except Exception as e:
            app.logger.error(f"Failed to add item to SellerInventory: {str(e)}")
            app.db.rollback()
            return False  # Indicate failure

    @property
    def product_name(self):
        result = app.db.execute('''
            SELECT name 
            FROM Products 
            WHERE id = :product_id''', 
        product_id=self.product_id)
        return result[0][0] if result else None

    #update quantity of item in seller inventory
    @staticmethod
    def update_item(seller_id, product_id, new_quantity):
        try:
            existing_item = SellerInventory.get_by_seller_and_product(seller_id, product_id)
            if not existing_item:
                return None  # Indicate that the item does not exist for this seller

            result = app.db.execute('''
                UPDATE SellerInventory
                SET quantity = :quantity
                WHERE seller_id = :seller_id AND product_id = :product_id
            ''',
            seller_id=seller_id,
            product_id=product_id,
            quantity=new_quantity)
            app.db.commit()
            return result  
        except Exception as e:
            app.logger.error(f"Failed to update SellerInventory: {str(e)}")
            app.db.rollback()
            raise

    #delete item from seller inventory        
    @staticmethod
    def delete_item(seller_id, product_id):
        try:
            result = app.db.execute('''
                DELETE FROM SellerInventory
                WHERE seller_id = :seller_id AND product_id = :product_id
            ''', seller_id=seller_id, product_id=product_id)
            app.db.commit()
            return result  
        except Exception as e:
            app.logger.error(f"Failed to delete item from SellerInventory: {e}")
            app.db.rollback()
            raise

    #get all products of a seller        
    @staticmethod
    def find_seller_for_item(pid):
        rows = app.db.execute('''
            SELECT seller_id, quantity
            FROM SellerInventory
            WHERE product_id = :pid
        ''', pid=pid)
        info = [SellerInventory(None, row.seller_id, None, row.quantity) for row in rows]
        if info:
            return info[0]
    
    #create a new product
    @staticmethod
    def create_new_product(name, price, available, short_description, long_description, category_id):
        rows = app.db.execute('''
            INSERT INTO Products (name, price, available, short_description, long_description, category_id)
            VALUES (:name, :price, :available, :short_description, :long_description, :category_id)
            RETURNING id
        ''',
        name=name,
        price=price,
        available=available,
        short_description=short_description,
        long_description=long_description,
        category_id=category_id
        )
        app.db.commit()
        return rows[0][0] if rows else None

    #get all sellers with inventory 
    @staticmethod
    def get_sellers_with_inventory(product_id):
        rows = app.db.execute('''
            SELECT si.seller_id, u.firstname, u.lastname, si.quantity
            FROM SellerInventory si
            JOIN Users u ON si.seller_id = u.id
            WHERE si.product_id = :product_id
            AND si.quantity > 0
        ''', product_id=product_id)
        return [{'seller_id': row[0], 'seller_name': f"{row[1]} {row[2]}", 'quantity': row[3]} for row in rows]

    #get all sellers of a product
    @staticmethod
    def get_all_sellers_for_product(product_id):
        """
        Gets all the sellers for a given product by product_id.
        """
        rows = app.db.execute('''
            SELECT u.id, u.firstname, u.lastname, si.quantity, u.email
            FROM Users u
            JOIN SellerInventory si ON u.id = si.seller_id
            WHERE si.product_id = :product_id
            AND si.quantity > 0
        ''',
        product_id=product_id)
        sellers = []
        for row in rows:
            seller = {
                'seller_id': row[0],
                'seller_name': f"{row[1]} {row[2]}",
                'quantity': row[3],
                'email': row[4]
            }
            sellers.append(seller)
        return sellers
    

    @staticmethod
    def get_anonymous_product_reviews_for_seller(seller_id):
        rows = app.db.execute('''
            SELECT p.name, pr.rating, pr.review, 'A customer' as customer
            FROM Products p
            JOIN ProductRatings pr ON p.id = pr.product_id
            JOIN SellerInventory si ON p.id = si.product_id
            WHERE si.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'product_name': row[0], 'rating': row[1], 'review': row[2], 'reviewer': row[3]} for row in rows]

    @staticmethod
    def get_anonymous_product_reviews_for_seller(seller_id):
        rows = app.db.execute('''
            SELECT p.name, pr.rating, pr.review, 'A customer' as customer
            FROM Products p
            JOIN ProductRatings pr ON p.id = pr.product_id
            JOIN SellerInventory si ON p.id = si.product_id
            WHERE si.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'product_name': row[0], 'rating': row[1], 'review': row[2], 'reviewer': row[3]} for row in rows]
    
    @staticmethod
    def get_product_sales_data(seller_id):
        sql_query = '''
            SELECT p.id, p.name, SUM(oi.quantity) as total_sold, COUNT(DISTINCT o.id) as total_orders
            FROM Products p
            JOIN OrderItems oi ON p.id = oi.pid
            JOIN Orders o ON oi.oid = o.id
            JOIN SellerInventory si ON p.id = si.product_id
            WHERE si.seller_id = :seller_id
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
        '''
        rows = app.db.execute(sql_query, seller_id=seller_id)
        return [{'product_id': row[0], 'product_name': row[1], 'total_sold': row[2], 'total_orders': row[3]} for row in rows]


    @staticmethod
    def find_seller_for_item(pid):
        rows = app.db.execute('''
            SELECT seller_id, quantity
            FROM SellerInventory
            WHERE product_id = :pid
            AND quantity > 0
            ORDER BY quantity DESC
        ''', pid=pid)
        return rows[0] if rows else None



    @staticmethod
    def update_product_availability(product_id):
        rows = app.db.execute('''
            SELECT COUNT(*)
            FROM SellerInventory
            WHERE product_id = :product_id
            AND quantity > 0
        ''', product_id=product_id)
        available = rows[0][0] > 0

        app.db.execute('''
            UPDATE Products
            SET available = :available
            WHERE id = :product_id
        ''', available=available, product_id=product_id)
        app.db.commit()



   
    