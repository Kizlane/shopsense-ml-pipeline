DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS order_item CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customer_event CASCADE;
DROP TABLE IF EXISTS support_ticket CASCADE;

/*--------------------*/
CREATE TABLE customer (
    customer_id SERIAL NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    address_line VARCHAR(100) NOT NULL,
    created_date DATE DEFAULT CURRENT_DATE,
    region VARCHAR(100),
    acquisition_channel VARCHAR(100)
);

ALTER TABLE customer 
    ADD CONSTRAINT customer_pk PRIMARY KEY (customer_id);

/*--------------------*/
CREATE TABLE product (
    product_id SERIAL NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

ALTER TABLE product
    ADD CONSTRAINT product_pk PRIMARY KEY (product_id);


/*--------------------*/
CREATE TABLE orders (
    order_id SERIAL NOT NULL,
    customer_id INTEGER NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    total_amount DECIMAL NOT NULL,
    order_status VARCHAR NOT NULL
);

ALTER TABLE orders
    ADD CONSTRAINT orders_pk PRIMARY KEY (order_id);

ALTER TABLE orders
    ADD CONSTRAINT orders_customer_fk FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id);

/*--------------------*/
CREATE TABLE order_item (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL NOT NULL
);

ALTER TABLE order_item
    ADD CONSTRAINT order_item_pk PRIMARY KEY (order_id, product_id);

ALTER TABLE order_item
    ADD CONSTRAINT order_item_order_id_fk FOREIGN KEY (order_id)
        REFERENCES orders(order_id);

ALTER TABLE order_item
    ADD CONSTRAINT order_item_product_id_fk FOREIGN KEY (product_id)
        REFERENCES product(product_id);

/*--------------------*/
CREATE TABLE customer_event (
    event_id SERIAL NOT NULL,
    customer_id INTEGER NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    session_id INTEGER
);

ALTER TABLE customer_event
    ADD CONSTRAINT customer_event_pk PRIMARY KEY (event_id);

ALTER TABLE customer_event
    ADD CONSTRAINT customer_event_customer_id_fk FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id);
/*--------------------*/

CREATE TABLE support_ticket (
    ticket_id SERIAL NOT NULL,
    customer_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    category VARCHAR(50) NOT NULL,
    resolution_days INTEGER,
    satisfaction_score INTEGER
);

ALTER TABLE support_ticket
    ADD CONSTRAINT support_ticket_pk PRIMARY KEY(ticket_id);

ALTER TABLE support_ticket
    ADD CONSTRAINT support_ticket_customer_id_fk FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id);
/*--------------------*/