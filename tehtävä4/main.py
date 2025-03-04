import connect
import data
import traceback

employees = data.load_csv()


education_levels_list, gender_list, job_titles_list = data.normalize_and_segregate_values(
    employees)

# connectin yritys pitää nestata looppiin,
# että saa puhtaan call stackin uudelle yritykselle.
connected, conn = connect.try_conn()
while not connected:
    print("Yritetään uudelleen...")
    connected, conn = connect.try_conn()

print("\n")
for edu in education_levels_list:
    print(edu)

print("\n")
for gen in gender_list:
    print(gen)

print("\n")
for job in job_titles_list:
    print(job)


#    if conn is not None:

#    # Add employee row
#        with conn:
#            try:
#                cur = conn.cursor()
#                _qry = "INSERT INTO employee(salary, age, years_of_experience, gender_id, education_level_id, job_title_id) VALUES(%f, %d, %f, %d, %d, %d)
#                for employee in employees:
#                    args = [
#                        employee.salary
#                        employee.age,
#                        employee.years_of_experience
#                        employee.job_title
#                    ]
#                    cur.execute(_qry, args)
#                conn.commit()
#            except Exception as e:
#                traceback.print_exc()
#                conn.rollback()
