CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    account_balance DECIMAL(12,2) NOT NULL DEFAULT 0.0,
    is_seller BOOLEAN DEFAULT FALSE,
    uaddress VARCHAR(255) NOT NULL
);

CREATE TABLE ProductCategories (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    category_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    short_description VARCHAR(255) NOT NULL,
    long_description TEXT NOT NULL,
    category_id INT REFERENCES ProductCategories(id)
);

CREATE TABLE Orders (
    id SERIAL PRIMARY KEY, 
    uid INT NOT NULL REFERENCES Users(id),
    date_fulfilled timestamp without time zone, 
    fulfilled BOOLEAN DEFAULT FALSE, --Signifies if the all items of the order have been fulfilled
    processed BOOLEAN DEFAULT FALSE -- Signifies if the order has been successfully placed
);

CREATE TABLE OrderItems (
    id SERIAL PRIMARY KEY,
    oid INT NOT NULL REFERENCES Orders(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL, 
    fulfilled BOOLEAN DEFAULT FALSE -- Signifies if the associated seller has fulfilled the order item
);

CREATE TABLE ItemInCart (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE SellerInventory (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    seller_id INT NOT NULL REFERENCES Users(id), -- Reference to the seller
    product_id INT NOT NULL REFERENCES Products(id), -- Reference to the product
    quantity INT NOT NULL
);

CREATE TABLE SellerOrders (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    item_id INT NOT NULL REFERENCES OrderItems(id),
    seller_id INT NOT NULL REFERENCES Users(id), -- Reference to the seller
    order_date timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    total_amount DECIMAL(12,2) NOT NULL,
    total_items INT NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    buyer_id INT NOT NULL REFERENCES Users(id)
);

CREATE TABLE ProductRatings (
    id INT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    product_id INT NOT NULL REFERENCES Products(id),
    buyer_id INT NOT NULL REFERENCES Users(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);
