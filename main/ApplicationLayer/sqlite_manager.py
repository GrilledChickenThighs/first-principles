import sqlite3

sqlite_file = '/Users/pAulse/Documents/productarbitrage/ebay_products_db.sqlite'
field_types = ['INTEGER', # Signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
               'NULL', # NULL value.
               'REAL', # floating point value, stored as an 8-byte IEEE floating point number.
               'TEXT', # text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE)
               'BLOB'] # blob of data, stored exactly as it was input.

def createTable(c, table_name, columns, field_types, primarykey=None):
    fields = ''
    count = 0
    for column, field_type in zip(columns, field_types):
        if column == primarykey:
            field = '{c} {ft} PRIMARYKEY'.format(c=column, ft=field_type)
        else:
            field = '{c} {ft}'.format(c=column, ft=field_type)

        count += 1
        if count < len(columns):
            fields += (field+', ')
        else:
            fields += (field)

    c.execute('CREATE TABLE table_name (fields)')

def connect():
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return c, conn

def commitandclose(conn):
    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()

# c,conn = connect()
# createTable(c,'Test_table',['dog','cat'],['TEXT','TEXT'], primarykey='dog')
# commitandclose(conn)
