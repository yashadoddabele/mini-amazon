from flask import current_app as app
from datetime import datetime
from .order import Order, OrderItems

class Purchase:
    def __init__(self, id, uid, oid, time_purchased, fulfilled, num_items, total_price):
        self.id = id
        self.oid = oid
        self.uid = uid
        self.time_purchased = time_purchased
        self.fulfilled = fulfilled   
        self.num_items = num_items    
        self.total_price = total_price 
        self.formatted_time_purchased = self.format_purchase_date(time_purchased)

    @staticmethod
    def format_purchase_date(time_purchased):
        # Convert the timestamp to a formatted string
        return datetime.strftime(time_purchased, "%B %d, %Y")

    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None
# get past orders and their attributes
    @staticmethod
    def get_all_by_uid_since(uid, since, sort_by='time_purchased'):
        orders, count = Order.get_all_by_uid(uid, since)
        purchase_history = []

        for order in orders:
            oid = order.id
            uid = order.uid
            date = order.date
            fulfilled = order.fulfilled
            purchase_date = date.date()
            num_items = OrderItems.get_num_items(oid)
            total = OrderItems.get_totalprice(oid)

            current_order = Purchase(None, uid, oid, date, fulfilled, num_items, total)
            purchase_history.append(current_order)
        
        if sort_by == 'time_purchased':
            purchase_history.sort(key=lambda purchase: purchase.time_purchased, reverse=True)
        elif sort_by == 'total_price':
            purchase_history.sort(key=lambda purchase: purchase.total_price)  # Sort by low to high total price
        elif sort_by == 'total_price_high_to_low':
            purchase_history.sort(key=lambda purchase: purchase.total_price, reverse=True)  # Sort by high to low total price
        else:
            app.logger.warning(f"Unsupported sorting criteria: {sort_by}")
        return purchase_history

#filter the total price so you can choose what to view in your purchase history                
    @staticmethod
    def filter_by_total_price(purchases, filter_type):
        if filter_type == 'lt10':
            return [purchase for purchase in purchases if purchase.total_price < 10]
        elif filter_type == 'lt50':
            return [purchase for purchase in purchases if 10 <= purchase.total_price < 50]
        elif filter_type == 'lt100':
            return [purchase for purchase in purchases if 50 <= purchase.total_price < 100]
        elif filter_type == 'gt100':
            return [purchase for purchase in purchases if purchase.total_price >= 100]
        elif filter_type != 'all':
            app.logger.warning(f"Unsupported filter criteria: {filter_type}")

        return purchases

    #the purchase gets stored
    @staticmethod
    def complete_purchase(oid):
        try:
            order = Order.get_ord(oid)
            if not order:
                raise ValueError("Order not found.")

            if order.fulfilled:
                app.db.execute('''
                    INSERT INTO Purchases (uid, oid, fulfilled)
                    VALUES (:uid, :oid, TRUE)
                ''', {'uid': order.uid, 'oid': oid})
                app.db.commit()
                return True
            else:
                raise ValueError("Order not fulfilled.")
        except Exception as e:
            app.logger.error(f"Failed to complete purchase: {e}")
            app.db.rollback()
            return False




                
            




