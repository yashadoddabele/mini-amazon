from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, account_balance, is_seller=False, uaddress=None):
        self.email = email
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.uaddress = uaddress 
        self.is_seller = is_seller
        self.account_balance = account_balance 

    def get_id(self):
        return str(self.id)
    #update the password function
    def update_password(self, new_password):
        # Hash the new password before storing it
        hashed_password = generate_password_hash(new_password)

        try:
            app.db.execute("""
                UPDATE Users
                SET password = :password
                WHERE id = :id
            """, password=hashed_password, id=self.id)

            return True  # Successful update
        except Exception as e:
            # Handle the error (e.g., log or return an error message)
            print(str(e))
            return False  # Update failed


    #update user attributes except account id
    def update_user_information(self, email, firstname, lastname, is_seller, uaddress):
        try:
            app.db.execute("""
                UPDATE Users
                SET email = :email, firstname = :firstname, lastname = :lastname, is_seller = :is_seller, uaddress = :uaddress
                WHERE id = :id
            """, email=email, firstname=firstname, lastname=lastname, is_seller = is_seller, uaddress=uaddress, id=self.id)

            # Update the object properties with the new values
            self.email = email
            self.firstname = firstname
            self.lastname = lastname
            self.is_seller = is_seller
            self.uaddress = uaddress

            return True  # Successful update
        except Exception as e:
            # Handle the error (e.g., log or return an error message)
            print(str(e))
            return False  # Update failed

#password verify
    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, account_balance, uaddress
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))
#check if email in use already
    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

#register a new user
    @staticmethod
    def register(email, password, firstname, lastname, account_balance = 0.0, is_seller = False, uaddress = None):  # Updated with is_seller parameter
        try:
            rows = app.db.execute("""
                INSERT INTO Users(email, password, firstname, lastname, is_seller, account_balance, uaddress)
                VALUES(:email, :password, :firstname, :lastname, :is_seller, :account_balance, :uaddress)
                RETURNING id
            """, email=email, password=generate_password_hash(password),
               firstname=firstname, lastname=lastname, account_balance = account_balance, is_seller=is_seller, uaddress=uaddress)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # Handle the error (e.g., log or return an error message)
            print(str(e))
            return None


    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, account_balance, is_seller, uaddress
FROM Users
WHERE id = :id

""",
                              id=id)
        return User(*(rows[0])) if rows else None
#retirives account balance of specific user
    def get_account_balance(self):
            rows = app.db.execute("""
                SELECT account_balance
                FROM Users
                WHERE id = :id
            """, id=self.id)
            if rows:
                self.account_balance = rows[0][0]
                return self.account_balance
            else:
                return None
#able to add money to account
    def change_account_balance(self, amount):
            try:
                app.db.execute("""
                    UPDATE Users
                    SET account_balance = account_balance + :amount
                    WHERE id = :id
                """, amount=amount, id=self.id)
                self.account_balance += amount
                return self.account_balance
            except Exception as e:
                # Handle the error (e.g., log or return an error message)
                print(str(e))
                return None
    
#get the seller's name
    def get_seller_name(self):
        if self.is_seller:
            rows = app.db.execute("""
                SELECT firstname, lastname
                FROM Users
                WHERE id = :id
            """, id=self.id)
            if rows:
                return rows[0]
        return None
 #get seller info to display publicly   
    @staticmethod
    def get_seller_info_by_id(seller_id):
        rows = app.db.execute("""
            SELECT id, email, firstname, lastname, uaddress
            FROM Users
            WHERE id = :seller_id AND is_seller = TRUE
        """, seller_id=seller_id)
        sellers = []
        for row in rows:
            seller = {
                'seller_id': row[0],
                'email': row[1],
                'seller_name': f"{row[2]} {row[3]}",
                'uaddress': row[4],
            }
            sellers.append(seller)
        return sellers
#get buyer info to diplsay publicly
    def get_buyer_info_by_id(buyer_id):
        rows = app.db.execute("""
            SELECT u.id, u.email, u.firstname, u.lastname, u.uaddress, u.is_seller
            FROM Users u
            WHERE u.id = :buyer_id
        """, buyer_id=buyer_id)
        sellers = []
        for row in rows:
            seller = {
                'buyer_id': row[0],
                'email': row[1],
                'buyer_name': f"{row[2]} {row[3]}",
                'uaddress': row[4],
                'is_seller': row[5]
            }
            sellers.append(seller)
        return sellers
 #get product ratings to display publicly   
    def get_product_ratings(self):
        rows = app.db.execute("""
            SELECT pr.product_id, pr.rating, pr.review, pr.created_at, p.name
            FROM ProductRatings pr
            JOIN Products p ON pr.product_id = p.id
            WHERE pr.buyer_id = :buyer_id
        """, buyer_id=self.id)

        ratings = []
        for row in rows:
            rating = {
                'product_id': row[0],
                'rating': row[1],
                'review': row[2],
                'created_at': row[3],
                'product_name': row[4]
            }
            ratings.append(rating)

        return ratings

