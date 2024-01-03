from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product

from flask import Blueprint
from flask import request

bp = Blueprint('kproducts', __name__)

@bp.route('/kproducts', methods=['POST', 'GET'])
def kproducts():
    if request.method == 'POST':
        k = int(request.form.get('k', 1)) 
        top_products = Product.get_top_k_expensive(k)
        return render_template('kproducts.html', topproducts=top_products)


    avail_products = Product.get_all()
    return render_template('index.html', avail_products=avail_products)