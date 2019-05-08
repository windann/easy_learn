import sqlite3


def conn_open():
    base = '/Users/anja/projects/easy_learn/easy_learn/db.sqlite3'
    conn = sqlite3.connect(base)
    cur = conn.cursor()
    return cur, conn


def curr_execute(cur, conn, querry):
    cur.execute(querry)
    conn.commit()
    return cur


def conn_close(conn):
    conn.close()