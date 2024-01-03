# mini-amazon ecommerce website

## About
This was a final group project for my CS316 class on Database Systems. It emulates a typical ecommerce website similar to Amazon's shopping application with all features involving carts, orders, user authorization/creation, products, and inventory. The application was tested on synthetic data with 2,000 products, 2,000 orders, and 100 unique users. It is a fully functional fullstack application with user interaction on the front-end that connects to tested API endpoints on the backend. All relevant website data is stored securely in a custom-designed relational database, which we managed through a Docker container. To maintain the security of customer data, we handled transactions/user registration safely by preventing injection attacks and unauthorized access through cache reroutes.

My responsibilities involved carts/orders transactions. Each user has one shopping cart, and it is fully functional. You can add available items to your cart through the detailed Products pages, and within the cart page you can update each cart item’s quantity and delete the item from the cart. The total price of the cart is listed and changes dynamically depending on a user’s updates and deletions within the cart. If there are no items in the cart, the page does not display a table and tells you to go shop for items. 
User orders are stored and tracked. First, a user cannot place an order with no items in their cart. Once there are items, upon placing an order seller inventories and the user’s balance are checked. If the item quantities for any items in the cart are more than the available seller inventory, the order is not processed, and the page tells you that the order could not be placed. The same happens if your account balance is not enough to pay for the total price of the cart. For successfully processed orders, the page tells you the order went through, lists the date of the processing, and sends the order to the respective sellers of each product in the order, waiting for fulfillment. The buyer’s balance is decreased by the total price, the seller’s balance is increased by the item price*quantity of what they are selling, and seller inventories are decremented. Once all order items are fulfilled, the entire order is listed as fulfilled, and the date of fulfillment is changed on the order page. All orders (processed/fulfilled or not) are linked to see in the purchase history page of a user. 
Similarly, all parts of the website (Users, Products, Carts/Orders, Seller Inventory/Orders) are fully functional.

## Technologies/Languages used
Flask, Python
SQLAlchemy
PostgreSQL
Docker
HTML/CSS/Javascript

## A peek into the user interface

<img width="1320" alt="Screenshot 2024-01-03 at 4 15 31 PM" src="https://github.com/yashadoddabele/mini-amazon/assets/110857917/3e0a6756-783e-437a-8e2c-749b353b8700">
<img width="1317" alt="Screenshot 2024-01-03 at 4 16 02 PM" src="https://github.com/yashadoddabele/mini-amazon/assets/110857917/8f1c84a7-c2f0-4521-9931-79743f16c3de">
<img width="1311" alt="Screenshot 2024-01-03 at 4 15 11 PM" src="https://github.com/yashadoddabele/mini-amazon/assets/110857917/87284661-50ba-47e4-b153-478cd09c6e35">


