from flask import Flask, request
from dotenv import load_dotenv
from collections import defaultdict
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
    '''Returns all the spells within the given level range'''
    conn, cursor = connect_to_db()
    lower = request.args.get('lower', None)
    higher = request.args.get('higher', None)
    cursor.execute("select * from spells where level <= %s and level >= %s", (higher,lower))
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/time/<casting_time>')
def get_spells_casting_time(casting_time):
    '''Returns all the spells with the given casting time'''
    values = (f"{casting_time}%",)
    if 'action' not in casting_time.lower():
        values = (f"%{casting_time}%",)
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where casting_time like %s", values)
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/user/<caster>')
def get_spells_user_casts(caster):
    '''Returns all the spells that the specified caster is able to cast'''
    values = (f"%{caster}%",)
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where array_to_string(users, ',') ilike %s", values)
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

@app.route('/spell/school/<school>')
def get_spells_school(school):
    '''Returns all the spells that are in the specific school.\nCan have multiple schools by comma delimiting them'''
    values = (tuple(school.lower().split(',')),)
    conn, cursor = connect_to_db()
    cursor.execute("select * from spells where lower(school) in %s", values)
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

def setup_casting_time_range(casting_time):
    '''Returns the query with all of the casting times appended to it within the specified range\n
    Input: A set of comma delimited values the first value being the start and the second being the end.'''
    first = True
    query = "select * from spells where 1 = 1 and ("
    casting_speeds = ["reaction", "ba", "action", "minute", "minutes", "hour", "hours"]
    casting_speeds_parts = defaultdict(lambda:None)
    casting_speeds_parts["reaction"] = " lower(casting_time) = 'reaction'"
    casting_speeds_parts["ba"] = " lower(casting_time) = 'bonus action'"
    casting_speeds_parts["action"] = " lower(casting_time) like 'action%'" # having a % on the end for spells that have casting time of 'action or ...'
    casting_speeds_parts["minute"] = " lower(casting_time) = 'minute'"
    casting_speeds_parts["minutes"] = " lower(casting_time) like '% minutes'"
    casting_speeds_parts["hour"] = " lower(casting_time) = 'hour'"
    casting_speeds_parts["hours"] = r" lower(casting_time) like '% hours'"
    start = casting_time.lower().split(',')[0]
    end = casting_time.lower().split(',')[-1]
    if not (start in casting_speeds and end in casting_speeds):
        return None
    
    for time in casting_speeds[casting_speeds.index(start):casting_speeds.index(end) + 1]:
        if first:
            query = query + casting_speeds_parts[time]
            first = False
        else: 
            query = query + ' or ' + casting_speeds_parts[time]
    query = query + ")"
    return query

@app.route('/spell/time/range/<casting_time>')
def get_spells_casting_time_range(casting_time):
    '''Returns all the spells with the given casting time range.\n
    Input: A set of comma delimited values the first value being the start and the second being the end.\n
    ORDER: reaction, BA, action, minute, minutes, hour, hours'''
    
    query = setup_casting_time_range(casting_time)
    if not query:
        return 'Invalid casting time range', 400
    conn, cursor = connect_to_db()
    cursor.execute(query)
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data


@app.route('/spell/filter/all')
def get_spells_all_filters():
    '''Returns all the spells within the given parameters.\n
    Input: 
    * Level (Upper and lower)
    * Casting time
    * Name
    * Range
    * Level
    * School
    * Users'''
    conn, cursor = connect_to_db()
    input = request.args.to_dict()
    cursor.execute(*make_query(input)) # base_query, variables
    data = cursor.fetchall()
    dis_db(conn, cursor)
    return data

def setup_master_query():
    '''Returns the base query, variable tuple and, a defualt dict with all of the where sections for each enpoint option'''
    base_query = "select * from spells where 1 = 1"
    variables = tuple()
    
    param_query_parts = defaultdict(lambda:None)
    param_query_parts["lower"] = " and level >= %s"
    param_query_parts["higher"] = " and level <= %s"
    param_query_parts["name"] = " and lower(name) like lower(%s)"
    param_query_parts["verbal"] = " and verbal = %s"
    param_query_parts["somatic"] = " and somatic = %s"
    param_query_parts["component"] = " and component = %s"
    param_query_parts["school"] = " and lower(school) in %s"
    
    return base_query, variables, param_query_parts

def make_query(input):
    '''Returns a query with all of the inputs provided also returns a tuple of the variables. Ignores NULL'''
    # TODO:
    # Casting time
    # Range
    # Duration ?
    # Users (Maybe let that also be a list)
    
    base_query, variables, param_query_parts = setup_master_query()
    
    for param, value in input.items():
        if param_query_parts[param]:
            if param == "name":
                value = f"%{value}%"
            elif param == "school":
                value = tuple(value.lower().split(','))
            base_query += param_query_parts[param]
            temp = list(variables)
            temp.append(value)
            variables = tuple(temp)
    return base_query, variables

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)