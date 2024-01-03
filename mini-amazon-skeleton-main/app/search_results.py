from flask import Flask, render_template, session
from flask_login import current_user
import datetime
import random
from flask_paginate import Pagination, get_page_parameter


from .models.product import Product
from .models.productcategories import Category

from flask import Blueprint
from flask import request

bp = Blueprint('search_results', __name__)

@bp.route('/search_results', methods=['POST', 'GET'])
def search_results():        
    #gets keyword from search 
    keyword_from_route = request.args.get('search_input')
    if request.method == 'GET' and request.args.get('search_input'):
        session['search_input'] = request.args.get('search_input')
    if request.method == 'POST':
        keyword_from_form = request.form.get('search_input')
        keyword = keyword_from_form if keyword_from_form is not None else keyword_from_route
    else:
        keyword = keyword_from_route

    search_results = Product.search_by_keyword(keyword)
    categories = Category.get_all()

    #handles sorting
    sort_type = request.args.get('sort_category') or session.get('sort_type', 'default_sort')
    session['sort_type'] = sort_type
    sorted_results = search_results.copy()

    if sort_type == 'price_asc':
        sorted_results = sorted(sorted_results, key=lambda x: x.price)
    elif sort_type == 'price_desc':
        sorted_results = sorted(sorted_results, key=lambda x: x.price, reverse=True)

    session['sort_type'] = sort_type

    #calculates avg rating
    avg_rating = {}
    for product in sorted_results:
        average_rating = Product.get_average_rating(product.id)
        avg_rating[product.id] = average_rating if average_rating is not None else "No reviews"


    #pagination
    per_page = int(request.args.get('results_per_page', session.get('results_per_page', 24)))
    session['results_per_page'] = per_page

    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = len(sorted_results)
    pagination = Pagination(page=page, per_page = per_page, total=total, search_type='bootstrap')

    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = sorted_results[start:end]


    return render_template('search_results.html', search_results=paginated_results, keyword = keyword, categories = categories, pagination=pagination, avg_rating=avg_rating)