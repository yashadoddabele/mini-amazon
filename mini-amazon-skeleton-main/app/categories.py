from flask import render_template, redirect, url_for, session
from flask_login import current_user
import datetime
import random
from flask_paginate import Pagination, get_page_parameter

from .models.productcategories import Category
from .models.product import Product


from flask import Blueprint
from flask import request

bp = Blueprint('category', __name__)

@bp.route('/category', methods=['POST', 'GET'])
def category():        
    category_id_from_route = request.args.get('category_input') #gets category id that was passed through route
    if request.method == 'GET' and request.args.get('category_input'):
        session['category_input'] = request.args.get('category_input')
    if request.method == 'POST':
        category_id_from_form = request.form.get('category_input')
        category_id = category_id_from_form if category_id_from_form is not None else category_id_from_route
    else:
        category_id = category_id_from_route

    category_results = Product.get_products_by_category(category_id) 
    category_name = Category.get_category_name(category_id)
    categories = Category.get_all()

    #handles sorting 
    sort_type = request.args.get('sort_category') or session.get('sort_type', 'default_sort')
    session['sort_type'] = sort_type
    sorted_results = category_results.copy()

    if sort_type == 'price_asc':
        sorted_results = sorted(sorted_results, key=lambda x: x.price)
    elif sort_type == 'price_desc':
        sorted_results = sorted(sorted_results, key=lambda x: x.price, reverse=True)

    session['sort_type'] = sort_type
    # calculates avg rating for each product
    avg_rating = {}
    for product in sorted_results:
        average_rating = Product.get_average_rating(product.id)
        avg_rating[product.id] = average_rating if average_rating is not None else "No reviews"
        
    #handles pagination
    per_page = int(request.args.get('results_per_page', session.get('results_per_page', 24)))
    session['results_per_page'] = per_page

    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = len(sorted_results)
    pagination = Pagination(page=page, per_page = per_page, total=total, search_type='bootstrap')

    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = sorted_results[start:end]


    return render_template('category.html', category_results=paginated_results, category_id = category_id, categories = categories, pagination=pagination, category_name = category_name, avg_rating=avg_rating)