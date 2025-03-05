import connect
import data
import traceback

# connectin yritys pitää nestata looppiin,
# että saa puhtaan call stackin uudelle yritykselle.
connected, conn = connect.try_conn()
while not connected:
    print("Yritetään uudelleen...")
    connected, conn = connect.try_conn()

employees = data.load_csv()


education_levels, genders, job_titles = data.normalize_and_segregate_values(
    employees)


employees = data.assign_ids_to_employees(
    employees, education_levels, genders, job_titles)


if conn is not None:
    try:
        print("\n---------------------------------------------------------")
        print("Lisätään rivit education_level pöytään...")
        cur = conn.cursor()
        _qry = "INSERT INTO education_level(level) VALUES(%s)"
        for edu in education_levels:
            args = (edu,)
            cur.execute(_qry, args)
        conn.commit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        conn.rollback()
    try:
        print("\n---------------------------------------------------------")
        print("Lisätään rivit gender pöytään...")
        cur = conn.cursor()
        _qry = "INSERT INTO gender(gender) VALUES(%s)"
        for gen in genders:
            args = (gen,)
            cur.execute(_qry, args)
        conn.commit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        conn.rollback()
    try:
        print("\n---------------------------------------------------------")
        print("Lisätään rivit job_title pöytään...")
        cur = conn.cursor()
        _qry = "INSERT INTO job_title(title) VALUES(%s)"
        for title in job_titles:
            args = (title,)
            cur.execute(_qry, args)
        conn.commit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        conn.rollback()

    try:
        print("\n---------------------------------------------------------")
        print("Lisätään rivit employee pöytään...")
        cur = conn.cursor()
        _qry = "INSERT INTO employee(salary, age, years_of_experience, gender_id, education_level_id, job_title_id) VALUES(%s, %s, %s, %s, %s, %s)"
        for employee in employees:
            args = (
                employee.salary,
                employee.age,
                employee.years_of_experience,
                employee.gender_id,
                employee.education_level_id,
                employee.job_title_id,
            )
            cur.execute(_qry, args)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
        conn.rollback()
    finally:
        if conn is not None:
            print("\nYhteys tietokantaan suljetaan ja ohjelma sulkeutuu.")
            conn.close()
