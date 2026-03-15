import psycopg2
from connection import PostgresConnection


def get_orders_with_products(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            orders.id AS order_id,
            products.name AS product_name,
            order_items.quantity,
            products.price
        FROM orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        INNER JOIN products ON order_items.product_id = products.id
        WHERE orders.user_id = {user_id}
        ORDER BY orders.id
    """)
    results = cursor.fetchall()
    return results


def get_order_statistics(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(orders), SUM(order_items.quantity)
        FROM orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        INNER JOIN products ON order_items.product_id = products.id
        GROUP BY orders.user_id
    """)
    result = cursor.fetchall()
    return result


def get_top_products(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            products.name, 
            SUM(order_items.quantity)
        FROM orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        INNER JOIN products ON order_items.product_id = products.id
        GROUP BY products.name
        ORDER BY SUM(order_items.quantity) DESC
        LIMIT {limit};
    """)
    result = cursor.fetchall()
    return result


def get_user_order_history(conn, user_id):
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
        ORDER BY products.price DESC
    """, (user_id,))
    result = cursor.fetchall()
    return result


def main():
    with PostgresConnection("localhost", "sfmshop", "postgres", "postgres") as conn:

        # print(get_orders_with_products(conn=conn, user_id=1))
        # print(get_user_order_history(conn=conn, user_id=2))
        # print(get_order_statistics(conn=conn))
        # print(get_top_products(conn))

        print(get_user_order_history(conn, 2))


if __name__ == "__main__":
    main()
