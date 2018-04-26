import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='judgement_doc',
    charset="utf8"
)
cur = conn.cursor()

def get_random_doc():
    statement = "SELECT content FROM `document` WHERE id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM `document`))) ORDER BY id LIMIT 1;"

    cur.execute(statement)
    result = cur.fetchone()
    return result