from datetime import datetime

import psycopg2
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sfmshop",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor
    )


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int = 0


class OrderCreate(BaseModel):
    user_id: int
    items: list[dict]


class UserCreate(BaseModel):
    name: str
    email: str


app = FastAPI()


@app.get("/products")
def get_products(limit: int = Query(10), offset: int = Query(0)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, quantity) VALUES (%s,%s,%s) RETURNING *",
        (product.name, product.price, product.quantity)
    )
    new_product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_product


@app.get("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *",
        (user.name, user.email)
    )
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_user


@app.get("/orders")
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY createdat DESC")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s", (order.user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")


    created_at = datetime.now()
    cur.execute(
        "INSERT INTO orders (userid, total, createdat) VALUES (%s, %s, %s) RETURNING id",
        (order.user_id, 0, created_at)
    )
    order_id = cur.fetchone()["id"]
    total = 0
    for item in order.items:
        product_id = item["product_id"]
        quantity = item["quantity"]

        cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cur.fetchone()
        if not product:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"Товар {product_id} не найден")

        item_total = product["price"] * quantity
        total += item_total

        cur.execute(
            "INSERT INTO order_items (orderid, productid, quantity) VALUES (%s,%s,%s)",
            (order_id, product_id, quantity)
        )
    cur.execute("UPDATE orders SET total=%s WHERE id=%s", (total, order_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"id": order_id, "user_id": order.user_id, "total": total, "created_at": created_at}


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    cur.execute("SELECT * FROM orders WHERE userid=%s ORDER BY createdat DESC", (user_id,))
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
