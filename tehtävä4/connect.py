import psycopg2
from contextlib import contextmanager
from getpass import getpass
import subprocess


def execute_db_creation(filename):
    print("---------------------------------------------------------")
    print(f'\nSuoritetaan sql tiedosto {filename}\n')
    print("Kirjaudutaan tietokantaan postgres, käyttäjänä postgres.")

    password = getpass("Syötä salasana käyttäjälle postgres: ")

    try:
        # komennon tekemiseen käytetty tekälyä
        result = subprocess.run(
            ['psql', '-X', '-U', 'postgres', '-f', filename],
            capture_output=True,
            text=True,
            env={'PGPASSWORD': password}
        )

        if result.returncode == 0:
            print("Tietokanta yhteys ja scriptin suoritus onnistui!")
        else:
            print(f"Scriptin suorituksessa virhe: {result.stderr}")

    except Exception as e:
        print(f"Virhe: {e}")

    print("---------------------------------------------------------\n")


def execute_sql_file(filename):
    print("---------------------------------------------------------")
    print(f'\nSuoritetaan sql tiedosto {filename}\n')
    print("Kirjaudutaan tietokantaan postgres, käyttäjänä postgres.")
    default_params = {
        'dbname': 'tehtava4_jonne_vuorela',
        'user': 'postgres',
        'password': getpass("Syötä salasana käyttäjälle postgres: "),
        'host': 'localhost'
    }

    try:
        conn_string = f"postgresql://{default_params['user']}:{
            default_params['password']}@{default_params['host']}/{default_params['dbname']}"
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()

        try:
            with open(filename, "r", encoding='utf-8') as file:
                sql_script = file.read()
            cursor.execute(sql_script)
            print("Tietokanta yhteys ja scriptin suoritus onnistui!")

        except psycopg2.Error as e:
            print(f"Scriptin suorituksessa virhe: {e}")

        finally:
            cursor.close()

    except psycopg2.Error as e:
        print(f"Tietokanta yhteys ei onnistunut: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

    print("---------------------------------------------------------\n")


@contextmanager
def connect():
    conn = None
    try:
        conn = psycopg2.connect(
            "postgresql://app:pass@localhost/tehtava4_jonne_vuorela")
        yield conn
    finally:
        if conn is not None:
            conn.close()
