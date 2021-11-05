# A clean class to work with SQLITE3 Databases in Python

**Methods:**
- db_connect
- db_close
- create_table
- add_column
- select
- iud
- sql

Each method has a doc-string on how to use it, please refer there for more details.
- Note: iud = insert, update, and delete

---

### Examle usage (run.py file):
```py
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
```

### Console:
```shell
IN:  $> python run.py
OUT: $> {'id': 1, 'name': 'Joe', 'priority': None}
```
BY: Isaac Lehman
