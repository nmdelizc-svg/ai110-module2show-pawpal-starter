from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    task_name: str
    duration: int
    priority: str
    is_done: bool = False

    def mark_done(self):
        pass

    def get_duration(self) -> int:
        pass

    def get_priority(self) -> str:
        pass


class Daily_Plan:
    def __init__(self, date: str, available_time: int):
        self.date = date
        self.available_time = available_time
        self.task_list: List[Task] = []
        self.completed_tasks: List[Task] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_completed(self) -> List[Task]:
        pass

    def get_remaining(self) -> List[Task]:
        pass

    def get_task_for_date(self, date: str) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet: Pet):
        pass

    def set_availability(self, available_time: int):
        pass

    def get_pets(self) -> List[Pet]:
        pass
