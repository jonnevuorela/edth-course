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
        cursor = conn.cursor()

        try:
            with open(filename, "r", encoding='utf-8') as file:
                sql_script = file.read()
            cursor.execute(sql_script)
            conn.commit()
            print("Tietokanta yhteys ja scriptin suoritus onnistui!")

        except psycopg2.Error as e:
            print(f"Scriptin suorituksessa virhe: {e}")
            conn.rollback()

        finally:
            print("Kirjaudutaan postgres käyttäjältä ulos...")
            cursor.close()

    except psycopg2.Error as e:
        print(f"Tietokanta yhteys ei onnistunut: {e}")

    print("---------------------------------------------------------\n")


def try_conn():
    try:
        with connect() as conn:
            print("Yhteys onnistui.")
            return True, conn
    except psycopg2.Error as e:
        print(e)
        # Jos tämä on oikea tapa käsitellä virheitä pythonissa, niin voi voi.
        # kummallakaan errorilla ei jostain syystä ole pgcode arvoa, joten en muuta keksi
        if "password authentication failed" in str(e):
            _choice = input(
                "Ohjelma tarvitsee käyttäjän. Luodaanko käyttäjä? (y/n)").lower()
            if _choice == "y":
                create_app_user()
                return False, None
            elif _choice == "n":
                return False, None
        elif "does not exist" in str(e):
            _choice = input(
                "Tietokantaa ei löydy. Luodaanko tietokanta? (y/n)").lower()
            if _choice == "y":
                execute_db_creation("db_init_part_1.sql")
                execute_sql_file("db_init_part_2.sql")
                return False, None
            elif _choice == "n":
                return False, None
        else:
            print("virhe: ", e)
            return False, None
    return False, None


def create_app_user():
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
def connect():
    conn = None
    try:
        conn = psycopg2.connect(
            "postgresql://app:pass@localhost/tehtava4_jonne_vuorela")
        yield conn
    except psycopg2.Error as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
