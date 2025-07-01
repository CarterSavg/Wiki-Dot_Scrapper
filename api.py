from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2.extras
import os

app = Flask(__name__)


@app.route('/')
def hello():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('''SELECT * FROM spells''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    print('Hello, World!')
    print(data)
    return data

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)