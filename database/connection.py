import psycopg2


class PostgresConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        self.conn.close()


def add_product(conn, name, price, quantity):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO products (name, price, quantity) VALUES {(name, price, quantity)}")
    print(f"Товар добавлен: {name}, {price}, {quantity}")


def get_all_products(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return products


def update_product_price(conn, product_id, new_price):
    with conn.cursor() as cursor:
        cursor.execute(f"UPDATE products SET price = {new_price} WHERE id = {product_id}")
    print(f"Цена обновлена: {new_price}")


def get_user_by_id(conn, user_id) -> dict | None:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = %s
        """, (user_id,))
        result = cursor.fetchall()
        return result if result != [] else ValueError(f"Пользователь с id = {user_id} не найден")


def delete_order(conn, order_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM orders
            WHERE id = %s
        """, (order_id,))
        result = cursor.fetchall()
        return result if result != [] else ValueError(f"Заказ с id = {order_id} не найден")


def main():
    with PostgresConnection("localhost", "sfmshop", "postgres", "postgres") as conn:
        print(get_user_by_id(conn, 100))
        delete_order(conn, 2)



if __name__ == "__main__":
    main()


"""
Товар добавлен: Ноутбук, 50000, 10
(2, 'Мышь', Decimal('1500.00'), 20)
(4, 'Ноутбук', Decimal('50000.00'), 10)
(5, 'Ноутбук', Decimal('1000000.00'), 10)
(6, 'Ноутбук', Decimal('1000000.00'), 10)
(1, 'Ноутбук', Decimal('45000.00'), 10)
(7, 'Ноутбук', Decimal('50000.00'), 10)
Цена обновлена: 45000

Process finished with exit code 0
"""











