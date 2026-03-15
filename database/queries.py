import psycopg2


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
    cursor.close()
    return results


def get_user_order_history(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            orders.id AS order_id,
            products.name AS product_name,
            order_items.quantity,
            products.price,
            (order_items.quantity * products.price) AS total_price_per_item
        FROM orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        INNER JOIN products ON order_items.product_id = products.id
        WHERE orders.user_id = {user_id}
        ORDER BY user_id
    """)
    result = cursor.fetchall()
    cursor.close()
    return result


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
    cursor.close()
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
    cursor.close()
    return result


def main():
    connection = psycopg2.connect(host="localhost", database="sfmshop", user="postgres", password="postgres")

    print(get_orders_with_products(conn=connection, user_id=1))
    print(get_user_order_history(conn=connection, user_id=2))
    print(get_order_statistics(conn=connection))
    print(get_top_products(connection))

    connection.close()

if __name__ == "__main__":
    main()
