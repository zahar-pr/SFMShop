

CREATE TABLE users (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(100) UNIQUE
);
CREATE TABLE products (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(200) NOT NULL, 
	price DECIMAL(10,2) NOT NULL, 
	quantity INTEGER DEFAULT 0
);
CREATE TABLE orders (
	id SERIAL PRIMARY KEY, 
	userid INTEGER REFERENCES users(id), 
	total DECIMAL(10,2), 
	createdat TIMESTAMP DEFAULT NOW()
);
CREATE TABLE order_items (
	id SERIAL PRIMARY KEY, 
	orderid INTEGER REFERENCES orders(id), 
	productid INTEGER REFERENCES products(id), 
	quantity INTEGER
);
INSERT INTO users (name, email) VALUES
('Иван Иванов', 'ivan@example.com'),
('Мария Петрова', 'maria@example.com'),
('Алексей Смирнов', 'aleksey@example.com');

INSERT INTO products (name, price, quantity) VALUES
('Ноутбук', 50000.00, 10),
('Мышь', 1500.00, 20),
('Клавиатура', 3000.00, 15),
('Монитор', 12000.00, 5),
('Наушники', 3500.00, 25);

INSERT INTO orders (userid, total) VALUES
(1, 51500.00),
(2, 15500.00);

INSERT INTO order_items (orderid, productid, quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 4, 1),
(2, 5, 1);











