PRAGMA foreign_keys = OFF;


DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS ingredient_deliveries;
DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS ing_cookies;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS transports;
DROP TABLE IF EXISTS order_transports;
DROP TABLE IF EXISTS customers;


PRAGMA foreign_keys = ON;


CREATE TABLE ingredient_deliveries(
  ing_del_id      TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  delivery_date   INTEGER NOT NULL,
  amount          INT NOT NULL CHECK(amount >= 0),
  ing_id          TEXT NOT NULL,
  FOREIGN KEY (ing_id) REFERENCES ingredients(ing_id)
);


CREATE TABLE ingredients(
  ing_id          TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  ing_name        TEXT NOT NULL,
  ing_unit        TEXT NOT NULL,
  storage_amount  INT DEFAULT 0 CHECK(storage_amount >= 0)
);


CREATE TABLE ing_cookies(
  ing_cookie_id   TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  cookie_id       TEXT NOT NULL,
  ing_id          TEXT NOT NULL,
  amount          INT,
  FOREIGN KEY (cookie_id) REFERENCES cookies(cookie_id),
  FOREIGN KEY (ing_id) REFERENCES ingredients(ing_id)
);


CREATE TABLE cookies(
  cookie_id     TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  cookie_name   TEXT,
  blocked       BOOLEAN
);


CREATE TABLE pallets(
  pallet_id       TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  cookie_id       TEXT NOT NULL,
  order_id        TEXT,
  prod_time       INTEGER,
  blocked         BOOLEAN,
  delivery_date   INTEGER,
  FOREIGN KEY (cookie_id) REFERENCES cookies(cookie_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);


CREATE TABLE orders(
  order_id                  TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  customer_id               TEXT NOT NULL,
  cookie_id                 TEXT NOT NULL,
  delivery_date             INTEGER,
  expected_delivery_date    INTEGER,
  ready                     BOOLEAN,
  n_pallets          INT,
  FOREIGN KEY (cookie_id) REFERENCES cookies(cookie_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE transports(
  transport_id    TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY);


CREATE TABLE order_transports(
  ord_trans_id    TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  order_id TEXT   NOT NULL,
  transport_id    TEXT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (transport_id) REFERENCES transport(transport_id)
);


CREATE TABLE customers(
  customer_id       TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  customer_name     TEXT,
  customer_address  TEXT
);

DROP TRIGGER IF EXISTS delivery_of_ingredients;
DROP TRIGGER IF EXISTS produced_pallet;
DROP TRIGGER IF EXISTS block_blocked;


-- Update storage on delivery
CREATE TRIGGER delivery_of_ingredients
AFTER INSERT ON ingredient_deliveries
BEGIN
  UPDATE ingredients
  SET storage_amount = storage_amount + NEW.amount
  WHERE ingredients.ing_id = NEW.ing_id ;
END;


-- Update storage on pallet production
CREATE TRIGGER produced_pallet
BEFORE INSERT ON pallets
BEGIN
  UPDATE ingredients 
  -- 54 because there are 15*10*36 cookies on each pallet and each recipe is for
  -- 100 cookies
  SET storage_amount = ingredients.storage_amount - 54 * (
    SELECT amount
    FROM ing_cookies
    WHERE ing_cookies.ing_id = ingredients.ing_id 
      AND ing_cookies.cookie_id = new.cookie_id
  )
  WHERE EXISTS(
    SELECT * 
    FROM ing_cookies
    WHERE ing_cookies.ing_id = ingredients.ing_id 
      AND ing_cookies.cookie_id = new.cookie_id
  ); 
END;

-- Any pallet created with a blocked cookie is automatically blocked
CREATE TRIGGER block_blocked
AFTER INSERT ON pallets
BEGIN 
  UPDATE pallets
  SET blocked = (
    SELECT cookies.blocked
    FROM cookies
    WHERE cookies.cookie_id = NEW.cookie_id
  )
  WHERE pallet_id = NEW.pallet_id;
END;
