from flask import render_template, redirect
from flask_login import current_user
from flask import Blueprint

bp = Blueprint('accounts', __name__)

@bp.route('/account')
def account():
    if current_user.is_authenticated:
        # You can pass user-specific data to the template if needed
        user_data = {
            'firstname': current_user.firstname,
            'lastname': current_user.lastname,
            
        }
        
        return render_template('accounts.html', user_data=user_data)
    else:
        # Handle the case when the user is not authenticated (e.g., redirect to the login page)
        return redirect('/login')  # You need to define the login route

    # If you want to return JSON data instead, you can use jsonify
    # return jsonify({'message': 'User is not authenticated'})











