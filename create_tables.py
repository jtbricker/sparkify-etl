import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def create_database():
    """ Drops Datbase if it already exists and creates it again

    Returns:
        cur {[cursor]} -- [psycopg2 object representing connection to PostgreSQL DB]
        conn {[connection]} -- [psycopg2 object that allows for interactions with the DB]
    """
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """ Executes the list of DROP TABLE queries that is imported from sql_queries

    Arguments:
        cur {[cursor]} -- [psycopg2 object representing connection to PostgreSQL DB]
        conn {[connection]} -- [psycopg2 object that allows for interactions with the DB]
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """ Executes the list of CREATE TABLE queries that is imported from sql_queries

    Arguments:
        cur {[cursor]} -- [psycopg2 object representing connection to PostgreSQL DB]
        conn {[connection]} -- [psycopg2 object that allows for interactions with the DB]
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ Creates database, drops existing tables if they exist and creates the tables """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
