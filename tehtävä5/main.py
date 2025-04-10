from typing_extensions import Doc
import pymongo
import psycopg2
from psycopg2.extensions import AsIs
from dataclasses import dataclass
from getpass import getpass
from contextlib import contextmanager
from typing import Any


@dataclass
class Table:
    name: str
    # dictionary lista, jossa dictionaryn
    # avain merkkaa columnia ja arvo geneeristä tyyppiä.
    rows: list[dict[str, Any]]

    # Claude 3.7 Sonnet Thinking
    # create a __str__ function for this dataclass,
    # that prints header line with column names and
    # then lists row values under.
    def __str__(self) -> str:
        if not self.rows:
            return f"Table: {self.name} (empty)"

        columns = set()
        for row in self.rows:
            columns.update(row.keys())
        columns = sorted(list(columns))

        result = [f"Table: {self.name}"]

        header = " | ".join(columns)
        result.append(header)
        result.append("-" * len(header))

        for row in self.rows:
            row_values = []
            for col in columns:
                value = str(row.get(col, "")) if row.get(
                    col) is not None else ""
                row_values.append(value)
            result.append(" | ".join(row_values))

        result.append(f"({len(self.rows)} rows)")

        return "\n".join(result)


@dataclass
class Database:
    tables: list[Table]


def deleteDatabase():
    startOver()


def importDatabase():
    passw = getpass("Syötä postgres käyttäjän salasana: ")
    listDb(passw)
    conn = selectDb(passw)
    if conn:
        database = loadPostgresDatabase(conn)

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


def loadPostgresDatabase(conn):
    """
    Jäsentää haettavan tietokannan dataclassien mukaisesti.

    Args:
        conn: psycopg2.connect

    Returns:
            Database

    Example:
            database = loadPostgresDatabase(conn)
    """
    cur = conn.cursor()
    database = None
    try:
        cur.execute("SELECT * FROM pg_tables WHERE schemaname = 'public';")
        result = cur.fetchall()
        _tables: list[Table] = []
        for _table in result:
            _qry = ("SELECT * FROM %s")
            # resultissa järjestyksessä toisena on tablen nimi.
            _args = _table[1]
            print(_qry, (AsIs(_table[1])))
            cur.execute(_qry, (AsIs(_table[1]),))

            rows = cur.fetchall()

            # Claude 3.7 Sonnet Thinking
            # how to get column names from psycopg2 query result.
            column_names = [desc[0] for desc in cur.description]

            # tyhjä rows lista joka on tyyppiä käyvä Table dataclassiin.
            _rows: list[dict[str, Any]] = []
            for row in rows:
                row_dict = {}
                for i, col_name in enumerate(column_names):
                    row_dict[col_name] = row[i]
                _rows.append(row_dict)

            table = Table(
                # resultissa järjestyksessä toisena on tablen nimi.
                name=_table[1],
                rows=_rows
            )
            _tables.append(table)
        database = Database(tables=_tables)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
    return database


def listDb(passw):
    probeConn = None

    probeConn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=passw,
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


def selectDb(passw):

    choice = input("\nSyötä tietokannan nimi, jonka haluat tuoda.\n")
    connected, conn = try_conn(choice, passw)
    while not connected:
        print("Yritetään uudelleen...")
        connected, conn = try_conn(choice, passw)

    if connected:
        return conn
    else:
        print("Tietokantaan yhdistäminen epäonnistui.")


def try_conn(db, passw):
    try:
        conn = psycopg2.connect(
            "postgresql://app:pass@localhost/tehtava4_jonne_vuorela",
            dbname=db,
            user="postgres",
            password=passw,
            host="localhost",
            port="5432"
        )
        print("Yhteys onnistui.")
        return True, conn
    except psycopg2.Error as e:
        print(e)
        # uusi käyttäjä postgresiin mahdollisesti tarpeeton
#        if "password authentication failed" in str(e):
#            _choice = input(
#                "Ohjelma tarvitsee käyttäjän. Luodaanko käyttäjä? (y/n)").lower()
#            if _choice == "y":
#                create_app_user(db)
#                return False, None
#            elif _choice == "n":
#                return False, None


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


if __name__ == "__main__":
    promptAction()
