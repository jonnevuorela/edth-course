from enum import Enum
from dataclasses import dataclass


@dataclass
class Employee:

    def __init__(
        self,
        age: int,
        gender: str,
        education_level: str,
        job_title: str,
        years_of_experience: float,
        salary: float,
    ):
        self.age = age
        self.gender = gender
        self.education_level = education_level
        self.job_title = job_title
        self.years_of_experience = years_of_experience
        self.salary = salary

    # AI generoitu. Claude 3.5 Sonnet.
    # i want to print out employyees so i can see whats in the objects
    def __str__(self) -> str:
        return f"{self.age}, {self.gender}, {self.education_level}, {self.job_title}, {self.years_of_experience}, {self.salary}"


class Gender(Enum):
    female = 0
    male = 1
    other = 2


class Education(Enum):
    high_school = 0
    bachelors_degree = 1
    masters_degree = 2
    phd = 3
