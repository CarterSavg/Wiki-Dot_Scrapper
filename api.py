from flask import Flask, request
from dotenv import load_dotenv
import psycopg2.extras
import os

app = Flask(__name__)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_to_db():
    '''Connects to database using psycopg2 module and returns the connection object and the cursor object'''
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn, cursor

def dis_db(conn, cursor):
    '''Disconnects from the connection and cursor objects'''
    try:
        cursor.close()
        conn.close()
    except:
        pass

#Routes

'''
TODO:
END POINTS:
- Action range, lower bound, upper bound, range
- Range endpoint, lower bound, upper bound, range
- All parameter
- Count parameter
- Class specific 
- level range 
'''
@app.route('/')
def show_all_spells():
    '''Returns all spells in the spells table'''
    conn, cursor = connect_to_db()
    cursor.execute('''SELECT * FROM spells''')
    data = cursor.fetchall()
    dis_db(conn, cursor)
    # print(data)
    return data

@app.route('/spell/like/<spell_name>')
def get_spell_like(spell_name):
    '''Returns all the spells like the spell in the parameters'''
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where lower(name) like lower(%s)", (f"%{spell_name}%",))
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/strict/<spell_name>')
def get_spell_strict(spell_name):
    '''Returns spell in the parameter'''
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where lower(name) = lower(%s)", (f"{spell_name}",))
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/level/upper/<spell_level>')
def get_spells_upper_level(spell_level):
    '''Returns all the spells of the level provided or lower'''
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where level <= %s", (spell_level,))
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/level/range')
def get_spells_level_range():
    '''Returns all the spells within the given range'''
    conn, cursor = connect_to_db()
    lower = request.args.get('lower', None)
    higher = request.args.get('higher', None)
    cursor.execute("select * from spells where level <= %s and level >= %s", (higher,lower))
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)