How to run:

1. Put all files in one folder.
2. Open config.py and replace YOUR_PASSWORD_HERE with your PostgreSQL password.
3. Make sure database phonebook_db exists in PostgreSQL.
4. Install package:
   pip install psycopg2-binary
5. Run:
   python phonebook.py
6. First choose menu option 1 to create/update schema and load SQL functions/procedures.

Files:
- phonebook.py: main console application
- config.py: database config
- connect.py: connection helper
- schema.sql: extended tables
- functions.sql: search and pagination functions
- procedures.sql: procedures
- contacts.csv: sample import file