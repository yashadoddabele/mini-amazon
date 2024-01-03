from flask import current_app as app
from datetime import datetime, timedelta

class Analytics:
    @staticmethod
    def get_inventory_status(seller_id):
        # Fetch inventory status for a seller
        rows = app.db.execute('''
            SELECT p.name, si.quantity
            FROM SellerInventory si
            JOIN Products p ON si.product_id = p.id
            WHERE si.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [{'product_name': row[0], 'quantity': row[1]} for row in rows]

    @staticmethod
    def get_order_data_for_charts(seller_id):
        # Fetch order data for chart visualization
        rows = app.db.execute('''
            SELECT p.name, SUM(oi.quantity) as total_quantity
            FROM OrderItems oi
            JOIN Products p ON oi.pid = p.id
            JOIN Orders o ON oi.oid = o.id
            WHERE o.uid = :seller_id AND o.fulfilled = TRUE
            GROUP BY p.name
        ''', seller_id=seller_id)
        return [{'product_name': row[0], 'total_quantity': row[1]} for row in rows]

    @staticmethod
    def get_fulfilled_orders_data(seller_id):
        # Fetch data about fulfilled orders
        rows = app.db.execute('''
            SELECT DATE(o.date_fulfilled) as date, COUNT(*) as total_orders
            FROM Orders o
            WHERE o.uid = :seller_id AND o.fulfilled = TRUE
            GROUP BY DATE(o.date_fulfilled)
        ''', seller_id=seller_id)
        return [{'date': row[0], 'total_orders': row[1]} for row in rows]

    @staticmethod
    def get_pending_order_items_count(seller_id):
        rows = app.db.execute('''
            SELECT p.name, COUNT(*) as total_items
            FROM OrderItems oi
            JOIN Products p ON oi.pid = p.id
            JOIN Orders o ON oi.oid = o.id
            JOIN SellerOrders so ON oi.id = so.item_id
            WHERE so.seller_id = :seller_id AND o.fulfilled = FALSE
            GROUP BY p.name
        ''', seller_id=seller_id)  # Pass seller_id as a named argument
        return [{'product_name': row[0], 'total_items': row[1]} for row in rows]

    @staticmethod
    def get_fulfilled_order_items_count(seller_id):
        rows = app.db.execute('''
            SELECT p.name, COUNT(*) as total_items
            FROM OrderItems oi
            JOIN Products p ON oi.pid = p.id
            JOIN Orders o ON oi.oid = o.id
            JOIN SellerOrders so ON oi.id = so.item_id
            WHERE so.seller_id = :seller_id AND o.fulfilled = TRUE
            GROUP BY p.name
        ''', seller_id=seller_id)  # Pass seller_id as a named argument
        return [{'product_name': row[0], 'total_items': row[1]} for row in rows]
