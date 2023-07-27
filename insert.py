import sqlite3
import random

con = sqlite3.connect('cosmos23-testdata copy.db')
c = con.cursor()

for i in range(10):
    id = random.randrange(10000000)
    id_1= random.randrange(10)
    sql = f"""
    INSERT INTO water (id, timestamp, science_id, lat, lon, tds, temperature, ph, do, orp, depth)
    VALUES ({id}, '{id_1}:00', 5, {id_1}, 20, 21, {id_1}, {id_1}, {id_1}, {id_1}, {id_1})
    """
    c.execute(sql)

con.commit()


con.close()
