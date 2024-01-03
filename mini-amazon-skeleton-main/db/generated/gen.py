from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from random import randint, choice, shuffle
import random

num_users = 100
num_products = 2000
num_purchases = 2500
num_carts = num_users  # assuming each user has one cart
num_items_in_cart = 1000
num_seller_inventory = 500
num_seller_orders = 1000
num_orders = 2500
order_items = 5000

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    available_users = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            account_balance = 0.0
            is_seller = False
            writer.writerow([uid, email, password, firstname, lastname, account_balance, is_seller])
            available_users.append(uid)
        print(f'{num_users} generated')
    return available_users

def gen_product_categories(num_categories):
    category_names = [
        "Electronics",
        "Clothing",
        "Home & Garden",
        "Toys & Games",
        "Health & Beauty",
        "Sports & Outdoors",
        "Books",
        "Music",
        "Movies",
        "Pet Supplies"
    ]
    
    with open('ProductCategories.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        print('Product Categories...', end=' ', flush=True)
        for category_id in range(num_categories):
            if category_id % 100 == 0:
                print(f'{category_id}', end=' ', flush=True)
                
            category_name = category_names[category_id] if category_id < len(category_names) else 'Other'
            writer.writerow([category_id, category_name])
        
        print(f'{num_categories} generated')
    return

def gen_products(num_products, num_categories):
    available_pids = []
    categories = list(range(0, num_categories)) 

    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            
            short_description = ""
            while not short_description:
                short_description = fake.sentence(nb_words=10)[:-1]
 
            long_description = ""
            while not long_description:
                long_description = fake.sentence(nb_words=50)[:-1]
                
            category_id = random.choice(categories)
            writer.writerow([pid, name, price, available, short_description, long_description, category_id])
            
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(min=0, max=num_users-1)
            pid = fake.random_element(available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for cart_id in range(num_carts):
            if cart_id % 10 == 0:
                print(f'{cart_id}', end=' ', flush=True)
            # Assuming each user has a cart, the cart_id is the same as the user_id
            total_price = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            writer.writerow([cart_id, total_price])
        print('Carts generated')
    return

def gen_item_in_cart(num_items_in_cart, available_users, available_products):
    with open('ItemInCart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ItemInCart...', end=' ', flush=True)
        random.shuffle(available_users)
        random.shuffle(available_products)
        for item_id in range(num_items_in_cart):
            user_id = fake.random_element(available_users)
            pid = fake.random_element(available_products)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([item_id, user_id, pid, quantity])
        print('ItemInCart generated')
    return

def gen_orders(num_orders, available_users):
    available_orders = []
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for oid in range(num_orders):
            if oid % 10 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = fake.random_element(elements=available_users)
            available_orders.append(oid)
            date = fake.date_time()
            fulfilled = fake.random_element(elements=(True, False))
            processed = fake.random_element(elements=(True, False))
            writer.writerow([oid, uid, date, fulfilled, processed])
        print('Orders generated')
    return available_orders

def gen_items_in_order(available_orders, order_items, available_pids):
    with open('OrderItems.csv', 'w') as f:
        available_items = []
        writer = get_csv_writer(f)
        print('OrderItems...', end=' ', flush=True)
        for item_id in range(order_items):
            available_items.append(item_id)
            oid = fake.random_element(elements=available_orders)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([item_id, oid, pid, quantity, False])
        print('OrderItem generated')
    return available_items

def gen_seller_inventory(num_seller_inventory, available_users, available_pids):
    with open('SellerInventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerInventory...', end=' ', flush=True)
        for num_sell in range(num_seller_inventory):
            seller_id = fake.random_element(elements=available_users)
            product_id = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=1, max=100)
            writer.writerow([num_sell, seller_id, product_id, quantity])
        print('SellerInventory generated')
    return

def gen_seller_orders(num_seller_orders, available_items, 
available_users):
    with open('SellerOrders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerOrders...', end=' ', flush=True)
        for id in range(num_seller_orders):
            #need to make sure the item is acc sold by the seller
            item_id = random.choice(available_items)
            seller_id = fake.random_element(elements=available_users)
            buyer_id = random.choice(available_users)
            while buyer_id == seller_id:
                buyer_id = random.choice(available_users)
            order_date = fake.date_time()
            total_amount = f'{str(fake.random_int(max=10000))}.{fake.random_int(max=99):02}'
            total_items = fake.random_int(min=1, max=10)
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, item_id, seller_id, buyer_id, order_date, total_amount, total_items, fulfilled])
        print('SellerOrders generated')
    return

# Call the functions here
available_users = gen_users(num_users)
gen_product_categories(10)
available_pids = gen_products(num_products, 10)
# gen_purchases(num_purchases, available_pids)
# gen_carts(num_carts)
gen_item_in_cart(num_items_in_cart, available_users, available_pids)
available_orders = gen_orders(num_orders, available_users)
available_items = gen_items_in_order(available_orders, order_items, available_pids)
gen_seller_inventory(num_seller_inventory, available_users, available_pids)
gen_seller_orders(num_seller_orders, available_items, available_users)