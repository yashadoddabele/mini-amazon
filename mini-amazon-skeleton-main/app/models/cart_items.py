from flask import current_app as app
from . import product, sellerInventory

# A wrapper class for the ItemInCart database
class CartItems:
    def __init__(self, name, quantity, price, pid, id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.pid = pid
        self.id = id
        
    @staticmethod
    # Adds an item to the ItemInCart database
    def add_item_to_cart(uid, pid, quantity):
        try: 
            item = product.Product.get(pid)

            if item and item.available:
                # Check if there is a seller for the product
                seller = sellerInventory.SellerInventory.get_seller_for_product(pid)
                if seller:
                    app.db.execute('''
                    INSERT INTO ItemInCart(uid, pid, quantity)
                    VALUES(:uid, :pid, :quantity)
                    ''', uid=uid, pid=pid, quantity=quantity)

                    app.db.commit()
                    print("success")
                    return "success"  # Successfully added to cart
                else:
                    # No seller found for the product
                    return "no_inventory"
            else:
                # Product not found or not available
                return "failure"
        except Exception as e:
                    app.logger.error(f"Failed to add item to cart: {str(e)}")
                    app.db.rollback()
                    return "failure"


    @staticmethod
    #Gets total price of all items in the cart
    def get_totalprice(uid):
        rows = app.db.execute('''
                SELECT Products.price, ItemInCart.quantity
                FROM ItemInCart JOIN Products ON ItemInCart.pid = Products.id
                WHERE ItemInCart.uid = :uid
        ''', uid=uid)
        tp = 0
        for row in rows:
            price, quantity = row
            tp = tp + (price * quantity)
        return tp

    @staticmethod
    # Get all cart items for a specified user
    def get_items(uid):
        rows = app.db.execute('''
            SELECT Products.name, ItemInCart.quantity, Products.price, ItemInCart.pid, ItemInCart.id
            FROM ItemInCart JOIN Products ON ItemInCart.pid=Products.id
            WHERE ItemInCart.uid = :uid      
        ''', uid=uid)
        items_in_cart = [CartItems(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return items_in_cart

    @staticmethod
    # Updates quantity for a specified cart item
    def update_quantity(id, newQuantity):
        try:
            rows = app.db.execute('''
                UPDATE ItemInCart
                SET quantity = :new_quantity
                WHERE id = :id
            ''', id=id, new_quantity=newQuantity)
        except Exception as e:
            print(str(e))
            app.db.rollback()

    @staticmethod
    # Deletes an item from the cart
    def delete_row(id):
        try:
            result = app.db.execute('''
                DELETE FROM ItemInCart
                WHERE id = :id
            ''', id=id)
            app.db.commit()
            return result
        except Exception as e:
            app.logger.error(f"Failed to delete item from ItemInCart: {e}")
            app.db.rollback()
            raise
            
    @staticmethod
    # Deletes all cart contents
    def delete_all_rows(uid):
        try:
            result = app.db.execute('''
                DELETE FROM ItemInCart
                WHERE uid = :uid
            ''', uid=uid)
            app.db.commit()
            return result
        except Exception as e:
            app.logger.error(f"Failed to delete items from ItemInCart: {e}")
            app.db.rollback()
            raise