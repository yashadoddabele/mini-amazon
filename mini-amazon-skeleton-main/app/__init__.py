from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .kproducts import bp as kproducts_bp
    app.register_blueprint(kproducts_bp)

    from .purchasehistory import bp as purchasehistory_bp
    app.register_blueprint(purchasehistory_bp)

    from .sellerInventory import bp as seller_inventory_bp  
    app.register_blueprint(seller_inventory_bp)

    from .sellerOrders import bp as seller_order_bp  
    app.register_blueprint(seller_order_bp)

    from .accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp) 

    from .search_results import bp as search_results_bp
    app.register_blueprint(search_results_bp) 

    from .product_details import bp as product_details_bp
    app.register_blueprint(product_details_bp) 

    from .order import bp as order_bp
    app.register_blueprint(order_bp)

    from .categories import bp as category_bp
    app.register_blueprint(category_bp)

    from .product_ratings import bp as product_ratings_bp
    app.register_blueprint(product_ratings_bp)

    from .seller_ratings import bp as seller_ratings_bp
    app.register_blueprint(seller_ratings_bp)

    from .analytics import bp as analytics_bp
    app.register_blueprint(analytics_bp)


    return app

