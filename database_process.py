import os
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def set_sql_connect(database_name):
    """
    Establish a connection to the SQLite database.

    Args:
        database_name (str): Name of the database file.

    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    return sqlite3.connect(database_name)

def set_sql_cursor(database_connect):
    """
    Create a cursor object from the database connection.

    Args:
        database_connect (sqlite3.Connection): SQLite database connection object.

    Returns:
        sqlite3.Cursor: SQLite cursor object.
    """
    return database_connect.cursor()

def close_connect(conn):
    """
    Commit changes and close the database connection.

    Args:
        conn (sqlite3.Connection): SQLite database connection object.
    """
    if conn:
        conn.commit()
        conn.close()

def set_connect_and_cursor(path='Data/database.sqlite'):
    """
    Establish a connection and create a cursor for the database.

    Args:
        path (str): Path to the SQLite database file.

    Returns:
        tuple: SQLite database connection and cursor objects.
    """
    conn = set_sql_connect(path)
    cursor = set_sql_cursor(conn)
    return conn, cursor

def create_table(table_name, columns):
    """
    Create a table in the SQLite database if it doesn't exist.

    Args:
        table_name (str): Name of the table to create.
        columns (str): Columns definition for the table.
    """
    conn, cursor = set_connect_and_cursor()
    with conn:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    logging.info(f"Table '{table_name}' created or already exists.")

def get_data(sql_command):
    """
    Execute a SQL command to retrieve data from the database.

    Args:
        sql_command (str): SQL command to execute.

    Returns:
        list: Retrieved data from the database.
    """
    conn, cursor = set_connect_and_cursor()
    cursor.execute(sql_command)
    data = cursor.fetchall()
    close_connect(conn)
    return data

def add_data(table, adding):
    """
    Insert data into a table in the SQLite database.

    Args:
        table (str): Name of the table to insert data into.
        adding (tuple): Data to insert into the table.
    """
    conn, cursor = set_connect_and_cursor()
    with conn:
        placeholders = ', '.join(['?'] * len(adding))
        sql = f"INSERT INTO {table} VALUES ({placeholders})"
        cursor.execute(sql, adding)
    logging.info(f"Data inserted into table '{table}': {adding}")

# Example usage:
if __name__ == '__main__':
    # Create a table with two columns: id (integer) and name (text)
    create_table('example_table', 'id INTEGER PRIMARY KEY, name TEXT')

    # Add data to the table
    add_data('example_table', (1, 'Sample Name'))

    # Retrieve data from the table
    data = get_data('SELECT * FROM example_table')
    print(data)