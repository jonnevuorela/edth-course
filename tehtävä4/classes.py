from enum import Enum
from dataclasses import dataclass


class Education(Enum):
    bachelors_degree = 0
    high_school = 1
    masters_degree = 2
    no_education = 3
    phd = 4


class Gender(Enum):
    female = 0
    male = 1
    other = 2


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
        self.gender_id = 0
        self.education_level_id = 0
        self.job_title_id = 0

    # AI generoitu. Claude 3.5 Sonnet.
    # i want to print out employyees so i can see whats in the objects
    def __str__(self) -> str:
        return f"{self.age}, {self.gender}, {self.education_level}, {self.job_title}, {self.years_of_experience}, {self.salary}\n gender id: {self.gender_id}, education level id: {self.education_level_id}, job title id: {self.job_title_id}"
