\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY ProductCategories FROM 'ProductCategories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.productcategories_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

-- \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.purchases_id_seq',
--                          (SELECT MAX(id)+1 FROM Purchases),
--                          false);

-- \COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.carts_id_seq',
--                          (SELECT MAX(id)+1 FROM Carts),
--                          false);

\COPY ItemInCart FROM 'ItemInCart.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.itemincart_id_seq',
                         (SELECT MAX(id)+1 FROM ItemInCart),
                         false);

-- Load data for the SellerInventory table (adjust file name and delimiter as needed)
\COPY SellerInventory FROM 'SellerInventory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerinventory_id_seq',
                         (SELECT MAX(id)+1 FROM SellerInventory),
                         false);

-- Load data for the SellerOrders table (adjust file name and delimiter as needed)
\COPY SellerOrders FROM 'SellerOrders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerorders_id_seq',
                         (SELECT MAX(id)+1 FROM SellerOrders),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);
                         
\COPY OrderItems FROM 'OrderItems.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orderitems_id_seq',
                         (SELECT MAX(id)+1 FROM OrderItems),
                         false);