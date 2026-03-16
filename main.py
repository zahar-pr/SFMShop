from product import Product
from user import User
from order import Order
from payment import CardPayment, PayPalPayment
from exceptions import ValidationError
from database.queries import *
from database.connection import *


def main():
    try:
        with PostgresConnection("localhost", "sfmshop", "postgres", "postgres") as conn:
            if not conn:
                print("Не удалось подключиться к БД")
                return

            print("Создаем пользователя...")
            user_id = create_user(conn, "Сергей Филичкин", "sergo@example.com")
            print("Создан пользователь номер:", user_id)
            user = get_user_by_id(conn, user_id)
            print("Полученный пользователь:", user)

            products = get_all_products(conn)
            print("\nВсе товары:")
            for p in products:
                print(p)

            stats = get_order_statistics(conn)
            print("\nСтатистика заказов:")
            for s in stats:
                print(s)

            top_products = get_top_products(conn)
            print("\nТоп товаров:")
            for tp in top_products:
                print(tp)

            history = get_user_order_history(conn, user_id)
            print("\nИстория заказов пользователя:")
            for h in history:
                print(h)

    except Exception as e:
        print(f"Ошибка работы программы: {e}")



def process_order_system():
    user = User("Иван", "ivan@test.com") # hi

    product1 = Product("Ноутбук", 50000, 2)
    product2 = Product("Мышь", 1500, 3)

    order = Order(user, [product1, product2])
    print(order)

    total = order.calculate_total()
    print("Общая стоимость заказа:", total)

    payments = [
        CardPayment(1000, "1234 5678 9012 3456"),
        PayPalPayment(2000, "test@paypal.com")
    ]

    for payment in payments:
        print(payment.process_payment())

    sorted_products = sorted([product1, product2])
    for product in sorted_products:
        print(product)

    try:
        product1.set_price(-1000)
    except ValidationError as e:
        print("Ошибка валидации:", e)


if __name__ == "__main__":
    # process_order_system()
    main()