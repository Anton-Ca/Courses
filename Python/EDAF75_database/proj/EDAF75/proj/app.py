import bottle
import hashlib
import sqlite3
from ast import literal_eval

from urllib.parse import quote, unquote

db = sqlite3.connect("krusty.sqlite")


def hash(msg):
    return hashlib.sha256(msg.encode("utf-8")).hexdigest()


@bottle.get("/ping")
def get_ping():
    bottle.response.status = 200
    return "pong"


@bottle.post("/reset")
def post_reset():
    c = db.cursor()
    with open("./create-schema.sql") as f:
        sql = f.read()
        c.executescript(sql)
    bottle.response.status = 205
    return {"location": "/"}


@bottle.post("/customers")
def post_customers():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON"

    expected_params = ("name", "address")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    insert_query = """
        INSERT
        INTO customers(customer_name, customer_address)
        VALUES( ? , ? )
    """

    insert_params = tuple(postdata[param] for param in expected_params)

    c.execute(insert_query, insert_params)

    bottle.response.status = 201
    return {"location": f"/customers/{quote(postdata['name'])}"}


@bottle.get("/customers")
def get_customers():
    c = db.cursor()
    c.execute(
        """
        SELECT  customer_name, customer_address
        FROM    customers
    """
    )

    found = [
        {"name": customer_name, "address": customer_address}
        for customer_name, customer_address in c
    ]

    bottle.response.status = 200
    return {"data": found}


@bottle.post("/ingredients")
def post_ingredients():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("ingredient", "unit")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    insert_query = """
        INSERT
        INTO ingredients(ing_name, ing_unit, storage_amount)
        VALUES( ? , ? , ? )
    """
    insert_params = tuple(postdata[param] for param in expected_params)

    c.execute(insert_query, insert_params + (0,))

    bottle.response.status = 201
    return {"location": f"/ingredients/{quote(postdata['ingredient'])}"}


@bottle.post("/ingredients/<ingredient>/deliveries")
def post_ingredient_delivery(ingredient):
    ingredient = unquote(ingredient)

    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("deliveryTime", "quantity")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    id_query = """
        SELECT ing_id, storage_amount, ing_unit
        FROM ingredients
        WHERE ing_name = ?
    """
    id_params = (ingredient,)

    c.execute(id_query, id_params)
    (ing_id, storage_amount, ing_unit) = c.fetchall()[0]

    insert_query = """
        INSERT
        INTO ingredient_deliveries(ing_id, delivery_date,  amount)
        VALUES( ? , STRFTIME('%s', ?) , ? )
    """
    insert_params = (ing_id,) + tuple(
        postdata[param] for param in expected_params
    )

    c.execute(insert_query, insert_params)

    response_data = {
        "ingredient": ingredient,
        "quantity": int(storage_amount) + int(postdata["quantity"]),
        "unit": ing_unit,
    }

    bottle.response.status = 201
    return {"data": response_data}


@bottle.get("/ingredients")
def get_ingredients():
    c = db.cursor()
    c.execute(
        """
        SELECT  ing_name, storage_amount, ing_unit
        FROM    ingredients
    """
    )

    found = [
        {"ingredient": ing_name, "quantity": storage_amount, "unit": ing_unit,}
        for ing_name, storage_amount, ing_unit in c
    ]

    bottle.response.status = 200
    return {"data": found}


@bottle.post("/cookies")
def post_cookies():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_cookie_params = ("name", "recipe")
    for param in expected_cookie_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_cookie_params)

    expected_recipe_params = ("ingredient", "amount")
    for param in expected_recipe_params:
        for recipe_item in postdata["recipe"]:
            if param not in expected_recipe_params:
                bottle.response.status = 400
                return "Bad parameters, need: " + ", ".join(
                    expected_recipe_params
                )

    c = db.cursor()

    cookie_insert_query = """
        INSERT
        INTO cookies(cookie_name, blocked)
        VALUES( ? , 0 )
    """
    c.execute(cookie_insert_query, (postdata["name"],))

    id_query = """
        SELECT cookie_id
        FROM   cookies
        WHERE  rowid = last_insert_rowid()
    """

    c.execute(id_query)
    cookie_id = c.fetchall()[0][0]

    for recipe_item in postdata["recipe"]:

        id_query = """
            SELECT ing_id
            FROM   ingredients
            WHERE  ing_name = ?
        """

        c.execute(id_query, (recipe_item["ingredient"],))
        ing_id = c.fetchall()[0][0]

        insert_recipe_item_query = """
            INSERT 
            INTO ing_cookies(cookie_id, ing_id, amount)
            VALUES( ? , ? , ? )
        """

        c.execute(
            insert_recipe_item_query,
            (cookie_id, ing_id, recipe_item["amount"]),
        )

    bottle.response.status = 201
    return {"location": f"/cookies/{quote(postdata['name'])}"}


@bottle.get("/cookies")
def get_cookies():
    c = db.cursor()
    c.execute(
        """
        SELECT  cookie_name, COUNT(
            CASE
            WHEN pallets.blocked = 0 THEN 1
            END
        ) as n_pallets
        FROM    cookies
        LEFT JOIN pallets
        USING   (cookie_id)
        GROUP BY cookie_name
        """
    )

    found = [
        {"name": cookie_name, "n_pallets": n_pallets}
        for cookie_name, n_pallets in c
    ]
    bottle.response.status = 200
    return {"data": found}


@bottle.get("/cookies/<cookie_name>/recipe")
def get_cookie_recipe(cookie_name):

    cookie_name = unquote(cookie_name)

    c = db.cursor()

    id_query = """
        SELECT cookie_id
        FROM   cookies
        WHERE  cookie_name = ?
    """

    c.execute(id_query, (cookie_name,))

    cookie_id = c.fetchall()[0][0]

    c.execute(
        """
        SELECT  ing_name, amount, ing_unit
        FROM    ing_cookies
        WHERE   cookie_id = ?
        JOIN    ingredients
        ON      (ing_id)
        """,
        (cookie_id,),
    )

    found = [
        {"ingredient": ing_name, "amount": amount, "unit": ing_unit}
        for ing_name, amount, ing_unit in c
    ]

    bottle.response.status = 200
    return {"data": found}


@bottle.post("/pallets")
def post_pallets():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ["cookie"]
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    cookie_id_query = """
        SELECT cookie_id
        FROM   cookies
        WHERE  cookie_name = ?
    """

    c.execute(cookie_id_query, (postdata["cookie"],))

    cookie_id = c.fetchall()[0][0]

    insert_pallet_query = """
        INSERT
        INTO pallets(cookie_id, order_id, prod_time, blocked, delivery_date)
        VALUES (?, NULL, strftime('%s','now'), 0, NULL)
    """

    try:
        c.execute(insert_pallet_query, (cookie_id,))

        pallet_id_query = """
            SELECT pallet_id
            FROM   pallets
            WHERE  rowid = last_insert_rowid()
        """

        c.execute(pallet_id_query)
        pallet_id = c.fetchall()[0][0]

        bottle.response.status = 201

        return {"location": pallet_id}

    except sqlite3.IntegrityError:

        bottle.response.status = 422

        return {"location": ""}


@bottle.get("/pallets")
def get_pallets():

    query_params = bottle.request.query.decode()

    query = """
        SELECT  pallet_id, cookie_name, DATETIME(prod_time, 'unixepoch'), pallets.blocked
        FROM    pallets
        INNER JOIN cookies
        USING (cookie_id)
    """

    if "before" in query_params:
        query += (
            f"WHERE prod_time <= STRFTIME('%s', '{query_params['before']}')"
        )
        if "after" in query_params:
            query += (
                f" AND prod_time >= STRFTIME('%s', '{query_params['after']}')"
            )
    elif "after" in query_params:
        query += (
            f"WHERE prod_time >= STRFTIME('%s', '{query_params['after']}')"
        )

    c = db.cursor()
    c.execute(query)

    found = [
        {
            "id": pallet_id,
            "cookie": cookie_name,
            "productionDate": prod_time,
            "blocked": blocked,
        }
        for pallet_id, cookie_name, prod_time, blocked in c
    ]

    bottle.response.status = 200
    return {"data": found}


@bottle.post("/cookies/<cookie_name>/block")
def post_block(cookie_name):

    query_params = bottle.request.query.decode()

    c = db.cursor()

    cookie_id_query = """
        SELECT cookie_id
        FROM   cookies
        WHERE  cookie_name = ?
    """

    c.execute(cookie_id_query, (cookie_name,))

    cookie_id = c.fetchall()[0][0]

    block_pallets_query = """
        UPDATE  pallets
        SET     blocked = 1
        WHERE   cookie_id = ?
    """

    if "after" in query_params:
        block_pallets_query += (
            f"AND prod_time >= STRFTIME('%s', '{query_params['after']}') "
        )

    if "before" in query_params:
        block_pallets_query += (
            f"AND prod_time >= STRFTIME('%s', '{query_params['before']}')"
        )
    else:
        # Block indefinetly by setting block on the cookie

        cookie_block_query = """
            UPDATE  cookies
            SET     blocked = 1
            WHERE   cookie_id = ?
        """

        c.execute(cookie_block_query, (cookie_id,))

    c.execute(block_pallets_query, (cookie_id,))

    bottle.response.status = 205
    return ""


@bottle.post("/cookies/<cookie_name>/unblock")
def post_unblock(cookie_name):

    query_params = bottle.request.query.decode()

    c = db.cursor()

    cookie_id_query = """
        SELECT cookie_id
        FROM   cookies
        WHERE  cookie_name = ?
    """

    c.execute(cookie_id_query, (cookie_name,))

    cookie_id = c.fetchall()[0][0]

    unblock_pallets_query = """
        UPDATE  pallets
        SET     blocked = 0
        WHERE   cookie_id = ?
    """

    if "after" in query_params:
        unblock_pallets_query += (
            f"AND prod_time >= STRFTIME('%s', '{query_params['after']}') "
        )

    if "before" in query_params:
        unblock_pallets_query += (
            f"AND prod_time >= STRFTIME('%s', '{query_params['before']}')"
        )
    else:
        # Unblock indefinetly by setting unblock on the cookie
        cookie_unblock_query = """
            UPDATE  cookies
            SET     blocked = 0
            WHERE   cookie_id = ?
        """

        c.execute(cookie_unblock_query, (cookie_id,))

    c.execute(unblock_pallets_query, (cookie_id,))

    bottle.response.status = 205
    return ""


bottle.run(host="localhost", port=8888)
