from flask import current_app as app
from datetime import datetime
from sqlalchemy import text
from . import sellerInventory as seller_inventory
from sqlalchemy import text
from .order import OrderItems, Order

class SellerOrders:
    def __init__(self, id, item_id, seller_id, order_date, total_amount, total_items, fulfilled, buyer_id):
        self.id = id
        self.item_id = item_id #references OrderItems
        self.seller_id = seller_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.total_items = total_items
        self.fulfilled = fulfilled
        self.buyer_id = buyer_id
        # self.buyer_address = buyer_address

    #get all orders for a seller
    @staticmethod
    def get_all_by_seller(seller_id):
        rows = app.db.execute('''
            SELECT so.id, so.item_id, so.seller_id, so.order_date, so.total_amount, so.total_items, so.fulfilled
            FROM SellerOrders so
            JOIN Users u ON so.buyer_id = u.id
            WHERE so.seller_id = :seller_id
            ORDER BY so.order_date DESC
        ''',
        seller_id=seller_id)
        return [SellerOrders(*row) for row in rows]

    # get buyer info from buyer id
    @staticmethod
    def get_buyer_info(buyer_id):
            row = app.db.execute('''
                SELECT firstname, lastname, email, uaddress
                FROM Users
                WHERE id = :buyer_id
            ''',
            buyer_id=buyer_id)
            return row if row else None


    # get a product id for a given order
    @staticmethod
    def get_product_ids_for_order(item_id):
        rows = app.db.execute('''
            SELECT pid
            FROM OrderItems
            WHERE id = :item_id
        ''', {'id': item_id})
        return [row[0] for row in rows]


    # function to get all orders for a seller
    @staticmethod
    def update_fulfill(item_id, seller_id):
        try: 
            app.db.execute('''UPDATE SellerOrders SET fulfilled = TRUE 
                                    WHERE item_id = :item_id AND seller_id = :seller_id''',
                            item_id=item_id, seller_id=seller_id)
            return True
        except Exception as e:
            app.logger.error(f"Failed to update: {e}")
            return False

    # function for sellers to fulfill orders
    @staticmethod
    def fulfill_order(item_id, seller_id):
        try:
            order = Order.get_order_from_item(item_id)
            order_id = order.id
            seller_items = OrderItems.get_items_by_seller(order_id, seller_id)
            order = Order.get_ord(order_id)
            items = OrderItems.get_items(order_id)
            fulfilled_ids = []

            all_fulfilled = True

            for sell in seller_items:
                iid = sell.id
                SellerOrders.update_fulfill(iid, seller_id)
                OrderItems.update_fulfillment(iid, True)
                sell.fulfilled = True     
                fulfilled_ids.append(iid)
                app.db.execute('''UPDATE SellerOrders SET fulfilled = TRUE 
                                WHERE item_id = :iid AND seller_id = :seller_id''',
                        iid=iid, seller_id=seller_id)

            ful = len(fulfilled_ids)

            for ids in fulfilled_ids:
                print(ids)
                print("yuh")

            items = OrderItems.get_items(order_id)
            if len(fulfilled_ids) != len(items):
                for item in items: 
                    if not item.fulfilled:
                        print(item.fulfilled)
                        all_fulfilled = False

            if all_fulfilled:
                Order.update_fulfillment(order_id, True)
                Order.update_date(order_id, datetime.now())
            return True
        except Exception as e:
            app.logger.error(f"Failed to fulfill order: {e}")
            return False


    
    @staticmethod 
    #gets order ITEMS from seller
    def get_all_orders_with_seller_products(seller_id):
        try:
            rows = app.db.execute('''
                SELECT DISTINCT si.id, oi.id, so.order_date, total_amount, total_items, so.fulfilled, so.buyer_id
                FROM OrderItems oi JOIN SellerOrders so ON oi.id = so.item_id
                WHERE so.seller_id = :seller_id''', seller_id=seller_id)
            return [SellerOrders(row[0], row[1], seller_id, row[2], row[3], row[4], row[5], row[6]) for row in rows]
        except Exception as e:
            app.logger.error(f"Failed to get orders: {str(e)}")
            app.db.rollback()


    #create an order entry for seller in SellerOrders table
    @staticmethod
    def create_seller_order_entry(seller_id, item_id, order_date, total_amount, total_items, buyer_id):
        try:
            app.db.execute('''
                INSERT INTO SellerOrders (item_id, seller_id, order_date, total_amount, total_items, fulfilled, buyer_id)
                VALUES (:item_id, :seller_id, :order_date, :total_amount, :total_items, FALSE, :buyer_id)
            ''',
            seller_id=seller_id, item_id=item_id, order_date=order_date, total_amount=total_amount, total_items=total_items, buyer_id=buyer_id)
            app.db.commit()
            return True
        except Exception as e:
            app.logger.error(f"Failed to create seller order entry: {str(e)}")
            app.db.rollback()
            return False



    # get all the orders that sellers have fulfilled
    @staticmethod
    def get_fulfilled_orders_by_seller(seller_id):
        try:
            sql_query = '''
                SELECT DISTINCT id, item_id, order_date, total_amount, total_items, fulfilled, buyer_id
                FROM SellerOrders
                WHERE seller_id = :seller_id
                AND fulfilled = TRUE
            '''
            rows = app.db.execute(sql_query, seller_id=seller_id)
            if not rows:  # Simplified check for empty result set
                return []
            return [SellerOrders(row[0], row[1], seller_id, row[2], row[3], row[4], row[5], row[6]) for row in rows]
        except Exception as e:
            app.logger.error(f"Failed to get fulfilled orders: {str(e)}")
            app.db.rollback()
            return []
        

    # get all the orders that sellers have not beenfulfilled
    @staticmethod
    def get_pending_orders_by_seller(seller_id):
        try:
            sql_query = '''
                SELECT DISTINCT id, item_id, order_date, total_amount, total_items, fulfilled, buyer_id
                FROM SellerOrders
                WHERE seller_id = :seller_id
                AND fulfilled = FALSE
            '''
            rows = app.db.execute(sql_query, seller_id=seller_id)
            print(rows)
            if rows is None or len(rows) == 0:  # Check if rows is None or empty
                return []  # Return an empty list if no rows are found
            return [SellerOrders(row[0], row[1], seller_id, row[2], row[3], row[4], row[5], row[6]) for row in rows]
        except Exception as e:
            app.logger.error(f"Failed to get pending orders: {str(e)}")
            app.db.rollback()
            return []  # Return an empty list in case of an exception



    


    