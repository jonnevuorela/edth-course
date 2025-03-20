import pymongo
import psycopg2
from getpass import getpass
from contextlib import contextmanager


def deleteDatabase():
    startOver()


def importDatabase():
    listDb()
    startOver()


def queryDatabase():
    startOver()


def promptAction():
    print("--------------------------------------")
    print("Mitä haluat tehdä?")
    print("0. Sulje ohjelma.")
    print("1. Tyhjennä MongoDB titetokanta.")
    print("2. Vie tietokanta Postgrestä MongoDB.")
    print("3. Suorita kysely MongoDB")
    _choice = input(": ")
    match _choice:
        case "0":
            return 0
        case "1":
            deleteDatabase()
        case "2":
            importDatabase()
        case "3":
            queryDatabase()


def startOver():
    _choice = input("Haluatko jatkaa? (k/e): ")
    match _choice.lower():
        case "e":
            return 0
        case "k":
            promptAction()


def listDb():
    probeConn = None

    password = getpass("Syötä salasana käyttäjälle postgres: ")
    probeConn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=password,
        host="localhost",
        port="5432"
    )

    cursor = probeConn.cursor()

    cursor.execute(
        "SELECT datname FROM pg_database WHERE datistemplate = false;")

    databases = cursor.fetchall()

    print("--------------------------------------")
    print("Löydetyt postgres tietokannat")
    for db in databases:
        print(db[0])

    cursor.close()
    probeConn.close()


def selectDb():

    choice = input("\nSyötä tietokannan nimi, jonka haluat tuoda.")
    connected, conn = try_conn(choice)
    while not connected:
        print("Yritetään uudelleen...")
        connected, conn = try_conn(choice)


def try_conn(db):
    try:
        conn = psycopg2.connect(
            "postgresql://app:pass@localhost/tehtava4_jonne_vuorela",
            dbname=db,
            user="app",
            password="pass",
            host="localhost",
            port="5432"
        )
        print("Yhteys onnistui.")
        return True, conn
    except psycopg2.Error as e:
        print(e)
        if "password authentication failed" in str(e):
            _choice = input(
                "Ohjelma tarvitsee käyttäjän. Luodaanko käyttäjä? (y/n)").lower()
            if _choice == "y":
                create_app_user(db)
                return False, None
            elif _choice == "n":
                return False, None


def create_app_user(db):
    try:
        with psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=getpass("Syötä salasana käyttäjälle postgres: "),
            host="localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE USER app WITH PASSWORD 'pass';")
                conn.commit()
                print("Käyttäjä luotu.")

    except psycopg2.Error as e:
        print(f"Virhe käyttäjän luonnissa: {e}")


@contextmanager
def connect(db):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=db,
            user="app",
            password="pass",
            host="localhost",
            port="5432"
        )
        yield conn
    except psycopg2.Error as e:
        raise e
    finally:
        if conn is not None:
            conn.close()


promptAction()
