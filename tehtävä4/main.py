from classes import Employee
import connect
import re


def printlist(lst: list) -> None:
    for item in lst:
        print(item)


def load_csv():
    with open("teht4.csv", mode="r", encoding="utf-8-sig") as file:
        employee_list: list[Employee] = []
        discarded: list[str] = []

        # Regex pattern AI genereoitu, josta muokattu sopivaksi. Claude 3.5 Sonnet
        # Create me a regex pattern that matches the context.
        pattern: re.Pattern = re.compile(
            r'(\d+),([^,]+),([^,]+),([^,]+),[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+),[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)')

        for line in file:
            match = pattern.match(line.rstrip())
            if match:
                fields: list[str] = line.rstrip().split(',')
                employee = Employee(
                    age=int(fields[0]),
                    gender=str(fields[1]),
                    education_level=str(fields[2]),
                    job_title=str(fields[3]),
                    years_of_experience=float(fields[4]),
                    salary=float(fields[5]),
                )
                employee_list.append(employee)
            else:
                discarded.append(line)

        incomplete_employees = parseMissingData(discarded)
        for incomplete_employee in incomplete_employees:
            employee_list.append(incomplete_employee)


def parseMissingData(data: list[str]):

    employee_list: list[Employee] = []

    # csv:n ensimmäisen rivin (tietotyyppi rivi) hylkäämiseen voisi olla parempiakin ratkaisuja
    for line in data[1:]:
        fields: list[str] = line.rstrip().split(',')
        employee = Employee(
            age=int(fields[0]) if fields[0].isdigit() else 0,
            gender=str(fields[1]) or 'Other',
            education_level=str(fields[2]) or 'no education',
            job_title=str(fields[3]) or 'no title',
            years_of_experience=float(
                fields[4]) if fields[4].isdigit() else 0,
            salary=float(fields[5]) if fields[5].isdigit() else 0,
        )

        if employee.age != 0:  # hylkää haamurivit.
            employee_list.append(employee)

    return employee_list


connect.tryConn()
