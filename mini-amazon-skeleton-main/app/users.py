from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.csrf import CSRFProtect


from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Incorrect email or password. Please try again.')
            return redirect(url_for('users.login'))  # Use the correct blueprint name here
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    uaddress = StringField('Address', validators=[DataRequired()])
    is_seller = BooleanField('Register as Seller')
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        is_seller = form.is_seller.data  

        uaddress = form.uaddress.data
        if User.register(form.email.data, form.password.data, form.firstname.data, form.lastname.data, is_seller=is_seller, uaddress = uaddress):
            return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)




@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



@bp.route('/account')
def account_balance():
    if current_user.is_authenticated:
    # Get the user's account balance using the get_account_balance method
        user = current_user
        balance = user.get_account_balance()
        print("balance")
        print(balance)
        print("Address:", user.uaddress)


        if balance is not None:
            return render_template('accounts.html', balance=balance, user=user)
    else:
        # Handle the case where the balance couldn't be retrieved
        return "Error: Unable to retrieve account balance"



@bp.route('/add_money', methods=['POST'])
def add_money():
        if current_user.is_authenticated:
            user = current_user
            amount = request.form.get('amount')
            
            if not amount or not amount.isdigit():
                flash('Please enter a valid amount.', 'error')
            else:
                amount = int(amount)

                # Use the change_account_balance method to add the amount to the user's balance
                user.change_account_balance(amount)
                print(current_user.account_balance)

                
        return redirect('/account')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    def validate_email(self, email):
        if email.data != current_user.email and User.email_exists(email.data):
            raise ValidationError('Email is already in use by another user.')

    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    uaddress = StringField('Address', validators=[DataRequired()])
    is_seller = BooleanField('Register as Seller')
    submit = SubmitField('Save Changes')



@bp.route('/update_account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Assuming you have a method to get a user by ID
        user = User.get(current_user.id)
        if user:
            # Update the user's information
            if user.update_user_information(form.email.data, form.firstname.data, form.lastname.data, form.is_seller.data, form.uaddress.data):
                return redirect(url_for('users.account_balance'))

    return render_template('updateInfo.html', title='Update', form=form)


class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    #ensure both passwords are the same
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update Password')
    
@bp.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if current_user.is_authenticated:
        form = UpdatePasswordForm()  
        if form.validate_on_submit():
            #update the user's password
            current_user.update_password(form.new_password.data)
            flash('Password updated successfully!', 'success')
            return redirect(url_for('users.account_balance'))  # Redirect back to the account page
        
        return render_template('update_password.html', title='Update Password', form=form)
    
    return redirect(url_for('users.login'))



@bp.route('/seller/<int:seller_id>')
def seller_info(seller_id):
    #get seller info to display
    seller_info = User.get_seller_info_by_id(seller_id)

    return render_template('seller_info.html', seller_info=seller_info)

@bp.route('/buyer/<int:buyer_id>')
def buyer_page(buyer_id):
    #get buyer info to display
    buyer_info = User.get_buyer_info_by_id(buyer_id)
    buyer = User.get(buyer_id)

    if buyer:
        buyer_reviews = buyer.get_product_ratings()
    else:
        buyer_reviews = []

    return render_template('user_info.html', buyer_info=buyer_info, buyer_reviews=buyer_reviews)
