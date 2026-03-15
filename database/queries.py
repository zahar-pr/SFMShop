from psycopg2 import Error

from connection import PostgresConnection


def get_orders_with_products(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                orders.id AS order_id,
                products.name AS product_name,
                order_items.quantity,
                products.price
            FROM orders
            INNER JOIN order_items ON orders.id = order_items.order_id
            INNER JOIN products ON order_items.product_id = products.id
            WHERE orders.user_id = %s
            ORDER BY orders.id
        """, (user_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Ошибка при получении заказов и товаров: {e}")
        return None


def get_order_statistics(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                users.id,
                COUNT(orders.id) AS orders_count,
                SUM(order_items.quantity * products.price) AS total_sum
            FROM users
            JOIN orders ON users.id = orders.userid
            JOIN order_items ON orders.id = order_items.orderid
            JOIN products ON order_items.productid = products.id
            GROUP BY users.id;
        """)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Ошибка при получении статистики заказов: {e}")
        return None


def get_top_products(conn, limit=5):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                products.name, 
                SUM(order_items.quantity)
            FROM orders
            INNER JOIN order_items ON orders.id = order_items.order_id
            INNER JOIN products ON order_items.product_id = products.id
            GROUP BY products.name
            ORDER BY SUM(order_items.quantity) DESC
            LIMIT %s;
        """, (limit,))
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Ошибка при получении популярных заказов: {e}")
        return None


def get_user_order_history(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                users.name AS "Имя пользователя", 
                products.name AS "Продукт", 
                products.price AS "Цена за единицу",
                products.quantity AS "Количество",
                products.price * products.quantity AS "Итоговая сумма"
            FROM users
            INNER JOIN orders ON orders.userid = users.id
            INNER JOIN order_items ON order_items.orderid = orders.id
            INNER JOIN products ON order_items.productid = products.id
            WHERE users.id = %s
            ORDER BY createdat ASC
        """, (user_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Ошибка при получении истории заказов пользователя: {e}")
        return None


def main():
    try:
        with PostgresConnection("localhost", "sfmshop", "postgres", "postgres") as conn:

            # print(get_orders_with_products(conn=conn, user_id=1))
            # print(get_user_order_history(conn=conn, user_id=2))
            # print(get_order_statistics(conn=conn))
            # print(get_top_products(conn))

            print(get_user_order_history(conn, 2))

            print(get_order_statistics(conn))
    except Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None


if __name__ == "__main__":
    main()
