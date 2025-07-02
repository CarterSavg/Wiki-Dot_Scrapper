from flask import Flask, render_template
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
@app.route('/')
def show_all_spells():
    '''Returns all spells in the spells table'''
    
    conn, cursor = connect_to_db()
    cursor.execute('''SELECT * FROM spells''')
    data = cursor.fetchall()
    dis_db(conn, cursor)
    # print(data)
    return data

# @app.route('/spell/<spell_name>')
# def get_spell():
#     '''Returns all the spells like the spell in the parameters'''
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)