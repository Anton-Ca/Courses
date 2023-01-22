import bottle
import hashlib
import sqlite3
from ast import literal_eval

db = sqlite3.connect("movies.sqlite")


def hash(msg):
    return hashlib.sha256(msg.encode("utf-8")).hexdigest()


@bottle.get("/ping")
def get_ping():
    bottle.response.status = 200
    return "pong"


@bottle.post("/reset")
def post_reset():
    c = db.cursor()
    with open("./lab3.sql") as f:
        sql = f.read()
        c.executescript(sql)
    bottle.response.status = 200
    return ""


@bottle.post("/users")
def post_users():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("username", "fullName", "pwd")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    # Nedan kollar vi om usern redan finns
    check_query = """
        SELECT count() as count
        FROM customers
        WHERE usr_name = ?
    """

    check_params = (postdata["username"],)

    c.execute(check_query, check_params)
    count = c.fetchall()[0][0]
    if count > 0:
        bottle.response.status = 400
        return ""

    # Annars stoppar vi in uppgifterna i vår query
    insert_query = """
        INSERT
        INTO customers(usr_name, full_name, password)
        VALUES( ? , ? , ? )
    """

    postdata["pwd"] = hash(postdata["pwd"])
    insert_params = tuple(postdata[param] for param in expected_params)

    c.execute(insert_query, insert_params)

    bottle.response.status = 201
    return f"/users/{postdata['username']}"


@bottle.post("/movies")
def post_movies():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("imdbKey", "title", "year")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    check_query = """
        SELECT count()
        FROM movies
        WHERE imdb_key = ?
    """
    check_params = (postdata["imdbKey"],)

    c.execute(check_query, check_params)
    count = c.fetchall()[0][0]
    if count > 0:
        bottle.response.status = 400
        return ""

    insert_query = """
        INSERT
        INTO movies(imdb_key, title, year)
        VALUES( ? , ? , ? )
    """
    insert_params = tuple(postdata[param] for param in expected_params)

    c.execute(insert_query, insert_params)

    bottle.response.status = 201
    return f"/movies/{postdata['imdbKey']}"


@bottle.post("/performances")
def post_performances():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("imdbKey", "theater", "date", "time")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    insert_query = """
        INSERT
        INTO performances(imdb_key, th_name, screen_date, start_time)
        VALUES( ? , ? , ? , ? )
    """

    insert_params = tuple(postdata[param] for param in expected_params)

    c.execute(insert_query, insert_params)

    id_query = """
        SELECT p_id
        FROM   performances
        WHERE  rowid = last_insert_rowid()
    """

    c.execute(id_query)
    performance_id = c.fetchall()[0][0]

    bottle.response.status = 201
    return f"/performances/{performance_id}"


@bottle.get("/movies/<imdb_key>")
def get_movies(imdb_key):
    c = db.cursor()
    c.execute(
        """
        SELECT  imdb_key, title, year
        FROM    movies
        WHERE imdb_key = ?
    """,
        [imdb_key],
    )

    found = [
        {
            "imdbKey": imdb_key,
            "title": title,
            "year": year,
        }
        for imdb_key, title, year in c
    ]
    bottle.response.status = 200
    return {"data": found}


@bottle.get("/movies")
def get_movies():
    query = """
        SELECT  imdb_key, title, year
        FROM    movies
    """

    params = []
    query_params = bottle.request.query.decode()
    if "year" in query_params:
        params.append(query_params.year)
        query += "WHERE year = ?"

    if "title" in query_params:
        if len(params):
            query += " AND title = ?"
        else:
            query += "WHERE title = ?"
        params.append(query_params.title)

    c = db.cursor()
    c.execute(query, params)

    found = [
        {
            "imdbKey": imdb_key,
            "title": title,
            "year": year,
        }
        for imdb_key, title, year in c
    ]
    bottle.response.status = 200
    return {"data": found}


@bottle.get("/performances")
def get_performances():
    query = """
        SELECT  
            p.p_id, 
            p.screen_date, 
            p.start_time, 
            p.imdb_key, 
            p.th_name,
            th.capacity - count(t.t_id) as remaining_seats
        FROM    performances as p
        JOIN    theatres as th
        ON      th.th_name = p.th_name
        LEFT OUTER JOIN tickets as t
        ON      t.p_id = p.p_id
        GROUP BY p.p_id
    """
    c = db.cursor()
    c.execute(query)

    found = [
        {
            "performanceId": p_id,
            "date": screen_date,
            "startTime": start_time,
            "imdbKey": imdb_key,
            "theater": th_name,
            "remainingSeats": remaining_seats,
        }
        for p_id, screen_date, start_time, imdb_key, th_name, remaining_seats in c
    ]
    bottle.response.status = 200
    return {"data": found}


@bottle.post("/tickets")
def post_tickets():
    try:
        postdata = literal_eval(bottle.request.body.read().decode("UTF-8"))
    except:
        bottle.response.status = 400
        return "Bad resuest, need JSON object with parameters: username, fullName, password"

    expected_params = ("username", "pwd", "performanceId")
    for param in expected_params:
        if param not in postdata:
            bottle.response.status = 400
            return "Bad parameters, need: " + ", ".join(expected_params)

    c = db.cursor()

    is_user_query = """
        SELECT count()
        FROM customers
        WHERE usr_name = ? and password = ? 
    """

    postdata["pwd"] = hash(postdata["pwd"])
    is_user_params = (postdata["username"], postdata["pwd"])

    c.execute(is_user_query, is_user_params)
    is_user = c.fetchall()[0][0]
    if not is_user:
        bottle.response.status = 401
        return "Wrong user credentials"

    seats_remain_query = """
        SELECT  th.capacity - count(t.t_id)
        FROM    performances as p
        JOIN    theatres as th
        ON      th.th_name = p.th_name
        LEFT OUTER JOIN tickets as t
        ON      t.p_id = p.p_id
        GROUP BY p.p_id
        HAVING p.p_id = ?
    """
    seats_remain_params = (postdata["performanceId"],)

    c.execute(seats_remain_query, seats_remain_params)
    remaining_seats = c.fetchall()[0][0]
    if remaining_seats < 1:
        bottle.response.status = 400
        return "No tickets left"

    insert_query = """
        INSERT
        INTO tickets(usr_name, p_id)
        VALUES( ? , ? )
    """

    insert_params = (postdata["username"], postdata["performanceId"])

    c.execute(insert_query, insert_params)

    id_query = """
        SELECT t_id
        FROM   tickets
        WHERE  rowid = last_insert_rowid()
    """

    c.execute(id_query)
    ticket_id = c.fetchall()[0][0]

    bottle.response.status = 201
    return f"/tickets/{ticket_id}"


@bottle.get("/users/<user>/tickets")
def get_movies(user):
    query = """
        SELECT 
            p.screen_date, 
            p.start_time, 
            p.th_name, 
            m.title, 
            m.year,
            count(t.t_id) as n_tickets
        FROM performances as p
        JOIN movies as m
        ON m.imdb_key = p.imdb_key
        JOIN
        tickets as t
        ON t.p_id = p.p_id
        WHERE usr_name = ?
        GROUP BY t.p_id
    """
    params = (user,)

    c = db.cursor()
    c.execute(query, params)
    found = [
        {
            "date": screen_date,
            "startTime": start_time,
            "theater": th_name,
            "title": title,
            "year": year,
            "nbrOfTickets": n_tickets,
        }
        for screen_date, start_time, th_name, title, year, n_tickets in c
    ]
    bottle.response.status = 200
    return {"data": found}


bottle.run(host="localhost", port=7007)
