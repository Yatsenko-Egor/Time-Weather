import sqlite3


def get_timezone(city):
    con = sqlite3.connect("time_db.sql")
    cur = con.cursor()
    try:
        timezone = cur.execute(f"SELECT time FROM cities WHERE city like '{city}%'").fetchone()[0]
    except Exception:
        return None
    return timezone
