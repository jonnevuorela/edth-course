from classes import Employee
import re


def printlist(lst: list) -> None:
    for item in lst:
        print(item)


def load_csv():
    with open("teht4.csv", mode="r", encoding="utf-8-sig") as file:
        print("\n---------------------------------------------------------")
        print("Luetaan data tiedostolta...")
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
                    gender=str(fields[1]).lower(),
                    education_level=str(fields[2]).lower(),
                    job_title=str(fields[3]).lower(),
                    years_of_experience=float(fields[4]),
                    salary=float(fields[5]),
                )
                employee_list.append(employee)
            else:
                discarded.append(line)

        incomplete_employees = parseMissingData(discarded)
        for incomplete_employee in incomplete_employees:
            employee_list.append(incomplete_employee)
    return employee_list


def assign_ids_to_employees(employee_list, education_levels_list, gender_list, job_titles_list):
    for employee in employee_list:
        employee.gender_id = gender_list.index(employee.gender) + 1
        employee.education_level_id = education_levels_list.index(
            employee.education_level) + 1
        employee.job_title_id = job_titles_list.index(employee.job_title) + 1

    return employee_list


def normalize_and_segregate_values(employee_list):
    education_levels = set()
    genders = set()
    job_titles = set()

    for employee in employee_list:
        employee.education_level = normalize_education_level(
            employee.education_level)
        education_levels.add(employee.education_level)

        employee.gender = employee.gender.strip()
        genders.add(employee.gender)

        job_titles.add(employee.job_title)

    education_levels_list = sorted(list(education_levels))
    gender_list = sorted(list(genders))
    job_titles_list = sorted(list(job_titles))

    return education_levels_list, gender_list, job_titles_list


def normalize_education_level(education_level):
    education = education_level.lower().strip()

    if "master" in education:
        return "master's degree"
    elif "bachelor" in education:
        return "bachelor's degree"
    elif "phd" in education or "phd" in education:
        return "phd"
    elif "high school" in education or "highschool" in education:
        return "high school"
    elif "no " in education or education == "":
        return "no education"
    else:
        return education


def parseMissingData(data: list[str]):

    employee_list: list[Employee] = []

    # csv:n ensimmäisen rivin (tietotyyppi rivi) hylkäämiseen voisi olla
    # parempiakin ratkaisuja, mutta tämä toimii käyttötarkoitukseen.
    for line in data[1:]:
        fields: list[str] = line.rstrip().split(',')
        employee = Employee(
            age=int(fields[0]) if fields[0].isdigit() else 0,
            gender=str(fields[1]).lower() or 'other',
            education_level=str(fields[2]).lower() or 'no education',
            job_title=str(fields[3]).lower() or 'no title',
            years_of_experience=float(
                fields[4]) if fields[4].isdigit() else 0,
            salary=float(fields[5]) if fields[5].isdigit() else 0,
        )

        if employee.age != 0:  # hylkää haamurivit.
            employee_list.append(employee)

    return employee_list
