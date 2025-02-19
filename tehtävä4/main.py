from classes import Employee
import re


def printlist(lst: list) -> None:
    for item in lst:
        print(item)


def load_csv():
    with open("teht4.csv", mode="r", encoding="utf-8-sig") as file:
        employee_list: list[Employee] = []
        discarded: list[str] = []

        # Regex pattern AI genereoitu. Claude 3.5 Sonnet
        # Create me a regex pattern that matches the context.
        pattern: re.Pattern = re.compile(
            r'(\d+),(\w+),([^,]+),([^,]+),(\d+),(\d+(?:\.\d+)?)')

        for line in file:
            match: bool = pattern.match(line.rstrip())
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
                print("no match")
        printlist(employee_list)
        print("------discarded-------")
        printlist(discarded)


load_csv()
