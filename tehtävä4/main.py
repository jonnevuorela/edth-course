import connect
import data

# connectin yritys pitää nestata looppiin,
# että saa puhtaan call stackin uudelle yritykselle.
connected, conn = connect.try_conn()
while not connected:
    print("Yritetään uudelleen...")
    connected, conn = connect.try_conn()

employees = data.load_csv()

for employee in employees:
    print(employee.education_level)
