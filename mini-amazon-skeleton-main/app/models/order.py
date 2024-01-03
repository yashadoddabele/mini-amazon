from flask import current_app as app
from . import cart_items

# A wrapper class for the Orders database
class Order: 
    def __init__(self, id, uid, date, fulfilled, processed):
        self.id = id
        self.uid = uid
        self.date = date
        self.fulfilled = fulfilled
        self.processed= processed

    @staticmethod
    # Gets all orders for a specified user since a specified date
    def get_all_by_uid(uid, since):
        rows = app.db.execute('''
        SELECT id, uid, date_fulfilled, fulfilled, processed
        FROM Orders
        WHERE uid= :uid
        AND date_fulfilled >= :since
        ORDER BY date_fulfilled DESC
        ''',
        uid=uid,
        since=since)

        orders = []
        count = 0
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4]))
            count += 1

        return orders, count

    @staticmethod
    # Gets an order with the specified order id
    def get_ord(oid):
        rows = app.db.execute('''
            SELECT id, uid, date_fulfilled, fulfilled, processed
            FROM Orders
            WHERE id = :oid
        ''', oid=oid)

        if rows:
            row = rows[0] 
            order = Order(row[0], row[1], row[2], row[3], row[4])
            return order
        else:
            return None

    # Gets the date of a specified Order
    @staticmethod
    def get_date(oid):
        rows = app.db.execute('''
            SELECT date_fulfilled
            FROM Orders
            WHERE id = :oid
        ''', oid=oid)
        if rows:
            row = rows[0]
            date = Order(None, None, row[2], None)
            return date
        else:
            return None

    @staticmethod
    # Updates the date associated with a specified Order
    def update_date(oid, new_date):
        try:
            app.db.execute('''
                UPDATE Orders
                SET date_fulfilled = :new_date
                WHERE id = :oid
            ''', oid=oid, new_date=new_date)
            return True
        except Exception as e:
            app.logger.error(f"Failed to update fulfillment: {str(e)}")
            return False

    @staticmethod
    # Creates an order for the specified user: does not populate it here
    def create_order(uid):
        try:
            rows = app.db.execute('''
                    INSERT INTO Orders (uid)
                    VALUES (:uid)
                    RETURNING id as oid
            ''', uid=uid)
            app.db.commit()
            if rows:
                row = rows[0] 
                oid = row[0]
                return oid
            else:
                app.db.rollback()
                return None
        except Exception as e:
            app.logger.error(f"Failed to create order: {str(e)}")
            app.db.rollback()
            return None

    @staticmethod
    # Updates the fulfillment status of the specified order
    def update_fulfillment(oid, new_fulfillment):
        try:
            app.db.execute('''
                UPDATE Orders
                SET fulfilled = :new_fulfillment
                WHERE id = :oid
            ''', oid=oid, new_fulfillment=new_fulfillment)
            return True
        except Exception as e:
            app.logger.error(f"Failed to update fulfillment: {str(e)}")
            return False

    @staticmethod
    # Updates the processing status of the specified order
    def update_processed(oid, new_processed):
        try:
            app.db.execute('''
                UPDATE Orders
                SET processed = :new_processed
                WHERE id = :oid
            ''', oid=oid, new_processed=new_processed)
            return True
        except Exception as e:
            app.logger.error(f"Failed to update processed: {str(e)}")
            return False

    @staticmethod
    # Gets an order from a specified order item's ID
    def get_order_from_item(item_id):
        try:
            print("hi")
            print(item_id)
            rows = app.db.execute('''
                SELECT o.id, o.uid, o.date_fulfilled, o.fulfilled, o.processed
                FROM Orders o 
                JOIN OrderItems oi ON o.id = oi.oid
                WHERE oi.id = :item_id;
            ''', item_id=item_id)
            return [Order(row[0], row[1], row[2], row[3], row[4])for row in rows][0]
        except Exception as e:
            app.logger.error(f"Failed to get order: {str(e)}")
            return False

# A wrapper class for the OrderItems database
class OrderItems:
    def __init__(self, id, oid, pid, quantity, price, name, fulfilled):
        self.id = id
        self.oid = oid
        self.pid = pid
        self.quantity = quantity
        self.price = price
        self.name = name
        # Represents the fulfillment status of the order item
        self.fulfilled = fulfilled

    @staticmethod
    # Adds a list of items to the specified order
    def add_items_to_order(oid, items):
        try:
            for item in items:
                app.db.execute('''
                        INSERT INTO OrderItems (oid, pid, quantity)
                        VALUES (:oid, :pid, :quantity)
                ''', oid=oid, pid=item.pid, quantity=item.quantity)
            app.db.commit()
            return True
        except Exception as e:
            app.logger.error(f"Failed to create order: {str(e)}")
            app.db.rollback() 
            return False
        
    @staticmethod
    # Gets the total price of all items in a specified order
    def get_totalprice(oid):
        rows = app.db.execute('''
                SELECT Products.price, OrderItems.quantity
                FROM (OrderItems JOIN Orders ON OrderItems.oid = Orders.id) JOIN Products ON Products.id=OrderItems.pid
                WHERE Orders.id = :oid
        ''', oid=oid)
        tp = 0
        for row in rows:
            price, quantity = row
            tp = tp + (price * quantity)
        return tp

    @staticmethod
    # Gets the total number of items in a specified order
    def get_num_items(oid):
        rows = app.db.execute('''
            SELECT quantity
            FROM OrderItems
            WHERE oid = :oid
        ''', oid=oid)
        count = 0
        for row in rows:
            quantity = row[0]
            count = count + quantity
        return count
        

    @staticmethod
    # Gets all order items of an order
    def get_items(oid):
        try:
            rows = app.db.execute('''
                SELECT OrderItems.id, OrderItems.pid, OrderItems.quantity, Products.price, Products.name, OrderItems.fulfilled
                FROM OrderItems JOIN Products ON OrderItems.pid=Products.id
                WHERE OrderItems.oid = :oid    
            ''', oid=oid)
            items_in_order = [OrderItems(row[0], oid, row[1], row[2], row[3], row[4], row[5]) for row in rows]
            return items_in_order
        except Exception as e:
            app.logger.error(f"Failed to get items: {str(e)}")
            app.db.rollback() 

    @staticmethod
    # Updates the fulfillment status of an order
    def update_fulfillment(id, new_fulfillment):
        try:
            app.db.execute('''
                UPDATE OrderItems
                SET fulfilled = :new_fulfillment
                WHERE id = :id
            ''', id=id, new_fulfillment=new_fulfillment)
            return True
        except Exception as e:
            app.logger.error(f"Failed to update fulfillment: {str(e)}")
            return False

    # @static
    # def get_fulfillment(id):
    #     try:
    #         rows = app.db.execute('''
    #             SELECT id, fulfilled FROM OrderItems
    #             WHERE id = :id
    #         ''', id=id)
    #         return [Order(row[0],row[4])for row in rows][0]
    #     except Exception as e:
    #         app.logger.error(f"Failed to getfulfillment: {str(e)}")
    #         return False


    @staticmethod
    # Gets all items in a specified order that are sold by a specified seller
    def get_items_by_seller(oid, seller_id):
        """
        Get items from an order that are provided by a specific seller.
        """
        sql_query = '''
            SELECT oi.id, oi.oid, oi.pid, oi.quantity, p.price, p.name, oi.fulfilled
            FROM OrderItems oi
            JOIN Products p ON oi.pid = p.id
            JOIN SellerInventory si ON p.id = si.product_id
            WHERE oi.oid = :oid AND si.seller_id = :seller_id
        '''
        rows = app.db.execute(sql_query, oid=oid, seller_id=seller_id)
        return [OrderItems(*row) for row in rows]


    @staticmethod
    # Checks if a specified user has ordered a specified product before
    def has_user_ordered_product(user_id, product_id):
        rows = app.db.execute('''
            SELECT *
            FROM Orders o
            JOIN OrderItems oi ON o.id = oi.oid
            WHERE oi.pid = :product_id AND o.uid = :user_id
        ''', user_id=user_id, product_id=product_id)

        return bool(rows) if rows else None

    @staticmethod
    # Finds the most recent purchased item of a specified user
    def get_most_recent_purchase(user_id):
        rows = app.db.execute('''
            SELECT oi.pid
            FROM Orders o
            JOIN OrderItems oi ON o.id = oi.oid
            WHERE o.uid = :user_id
            ORDER BY o.date_fulfilled DESC
            LIMIT 1
        ''', user_id=user_id)

        return rows[0][0] if rows else None