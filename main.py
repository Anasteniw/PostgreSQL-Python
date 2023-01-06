import psycopg2


conn = psycopg2.connect(database="netology_db", user = "postgres", password = "02091990")
cur = conn.cursor()

# def delete_db(cur):
#     cur.execute("""
#                 DROP TABLE clients, phonenumbers CASCADE;
#                 """)

def create_db(cur):
    cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(20),
                last_name VARCHAR(30),
                email VARCHAR(254)
                );
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS phonenumbers(
                phones VARCHAR(11) PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id)
                );
                """)
    


def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute("""
                INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s);
                """, (first_name, last_name, email))
    

def add_phone(cur, client_id, phones):
    cur.execute("""
                INSERT INTO phonenumbers(client_id, phones) VALUES(%s, %s);
                """, (client_id, phones))
    

def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
               UPDATE clients SET first_name=%s WHERE client_id=%s;
               """, (first_name, client_id))
    cur.execute("""
               UPDATE clients SET last_name=%s WHERE client_id=%s;
               """, (last_name, client_id))
    cur.execute(f"""
               UPDATE clients SET email=%s WHERE client_id=%s;
               """, (email, client_id))
    cur.execute("""
               SELECT * FROM clients;
               """)
    print(cur.fetchall())
    cur.execute("""
               UPDATE phonenumbers SET phones=%s WHERE client_id=%s;
               """, (phones, client_id))
    cur.execute("""
               SELECT * FROM phonenumbers;
               """)
    print(cur.fetchall())
    


def delete_phone(cur, phones):
    cur.execute("""
                DELETE FROM phonenumbers WHERE phones=%s;
                """, (phones,))
    cur.execute("""
                SELECT * FROM phonenumbers;
                 """)
    print(cur.fetchall())


def delete_client(cur, client_id):
    cur.execute("""
                DELETE FROM phonenumbers WHERE client_id=%s;
                """, (client_id,))
    cur.execute("""
                SELECT * FROM phonenumbers;
                """)
    print(cur.fetchall())
    cur.execute("""
                DELETE FROM clients WHERE client_id=%s;
                """, (client_id,))
    cur.execute("""
                SELECT * FROM clients;
                 """)
    print(cur.fetchall())



def find_client(cur, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
                SELECT client_id FROM clients WHERE first_name=%s and last_name=%s and email=%s;
                """, (first_name, last_name, email,))
    print(cur.fetchone())
    cur.execute("""
                SELECT client_id FROM phonenumbers WHERE phones=%s;
                """, (phones,))
    print(cur.fetchall())


with psycopg2.connect(database="netology_db", user="postgres", password="02091990") as conn:
    with conn.cursor() as cur:
        # delete_db(cur)
        create_db(cur)
        add_client(cur, 'Ivan', 'Petrov', 'ivan@mail.ru', '+7-111-222-33-44')
        add_phone(cur, 1, '+7888888888')
        change_client(cur, 1, 'Anna', 'Ivanova', 'anna@mail.ru', '+75555555')
        delete_phone(cur, '+7888888')
        delete_client(cur, 1)
        find_client(cur, 'Anna', 'Ivanova', 'anna@mail.ru', '+75555555')

conn.close()