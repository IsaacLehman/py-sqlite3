"""
A clean class to work with SQLITE3 Databases in Python

Note: iud = insert, update, and delete

Examle usage (run.py file):
=================================================================================
    from DB import DB

    # Connect to DB
    myDB = DB("db-test/db.sqlite3")

    # Create a table
    dbCols = ["id integer PRIMARY KEY", "name text NOT NULL", "priority integer"]
    myDB.create_table("Users", dbCols)

    # Insert data
    myDB.iud("INSERT INTO Users (name) VALUES (?)", ("Joe",))

    # Query data
    for row in myDB.select("SELECT * FROM Users"):
        print(row)

    # Close connection
    myDB.db_close()

    ---
    Console:
    IN:  $> python run.py
    OUT: $> {'id': 1, 'name': 'Joe', 'priority': None}
=================================================================================

BY: Isaac Lehman
"""
import os
import sqlite3

class DB:
    con = None # Connection
    cur = None # Cursor


    def __init__(self, path, is_relative=True):
        """
        Setup 
        -> path to db (String)
        -> was path relative (True/False)
        """
        if is_relative:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the database file from there
            self.path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        else:
            self.path = path

        # Connect to the database
        self.db_connect()

    def __del__(self):
        """
        Close the connection on destruction
        """
        if self.con:
            self.db_close()
        

    def db_connect(self):
        """
        Connect to the DB
        -> Populates con and cur
        """
        self.con = sqlite3.connect(self.path)  
        self.con.row_factory = sqlite3.Row  
        if self.con:
            self.cur = self.con.cursor()   
        else:
            raise ConnectionError(f'Unable to connect to the database at -> {self.path}')

    
    def db_close(self):
        """ 
        Close the DB connection
        """
        if self.con:
            self.con.close()


    def create_table(self, table_name, table_cols):
        """
        Create a table in the DB
        -> Name of table (String)
        -> Array of column statements (Array[String])
            ex. ["id integer PRIMARY KEY", "name text NOT NULL", ...]
        """
        create_statement = f'CREATE TABLE IF NOT EXISTS {table_name} ('

        num_rows = len(table_cols)
        index = 0
        for col in table_cols:
            index += 1
            if index == num_rows:
                create_statement += f' {col}'
            else:
                create_statement += f' {col},'

        create_statement += ')'

        self.cur.execute(create_statement)

    
    def add_column(self, table, new_col):
        """
        Add a column to a table in the DB
        -> Name of table (String)
        -> Name of the new column (String)
            ex. last_name text NOT NULL
        """
        create_statement = f'ALTER TABLE {table} ADD COLUMN {new_col}'
        self.cur.execute(create_statement)
        


    def select(self, statement, args=None):
        """
        Select data from the DB
        -> The SQL statment (String)
        -> A tuple of arguments to fill a prepared statement (tuple)
            Place ? where they go
            ex. "SELECT * FROM Users WHERE id=? and name=?", (id, name)  
        """
        results = None
        if args:
            results = self.cur.execute(statement, args)
        else:
            results = self.cur.execute(statement)

        if results:
            return [dict(row) for row in results]
        else:
            return None


    def iud(self, statement, args=None):
        """
        Insert/Update/Delet data into the DB
        -> The SQL statment (String)
        -> A tuple of arguments to fill a prepared statement (tuple)
            Place ? where they go
            ex. "INSERT INTO Users (id, name) VALUES (?, ?)", (id, name)  
        """

        if args:
            self.cur.execute(statement, args)
        else:
            self.cur.execute(statement)
        
        self.con.commit()


    def sql(self, statement, args=None, commit=False):
        """
        Execute arbitrary SQL
        -> The SQL statment (String)
        -> A tuple of arguments to fill a prepared statement (tuple)
            Place ? where they go
        -> Whether or not to commit to the DB (True/False)
        """
        if args:
            results = self.cur.execute(statement, args)
        else:
            results = self.cur.execute(statement)

        if commit:
            self.con.commit()
        
        return results

