from flask import current_app, g
import pymysql
import os

# MySQL configuration
db_host = os.environ.get('DB_HOST')
db_port = int(os.environ.get('DB_PORT'))
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

# Function to get MySQL connection
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

# Function to close MySQL connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def db_connect(query):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    
    cursor.close()
    close_db()
    return {'rows': rows, 'columns': column_names}

def db_fetch(query , param=None):
    # Establish a connection to the database
    db = get_db()
    cursor = db.cursor()

    if param is not None:
        # Execute a query to retrieve data with parameters
        cursor.execute(query, param)
    else:
        # Execute a query to retrieve data without parameters
        cursor.execute(query)

    # Fetch all rows from the result
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    # Close the cursor and connection
    cursor.close()
    close_db()
    return {'rows':rows,'columns':column_names}

def db_exec(query):
    # Establish a connection to the database
    db = get_db()
    cur = db.cursor()

    # Execute a query to retrieve data
    result = cur.execute(query)
    db.connection.commit()
    # Close the cursor and connection
    cur.close()
    close_db()
    if result is None:
        return True
    else:
        return False