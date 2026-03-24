from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


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
    duration: int       # in minutes
    priority: str
    pet: Pet            # the pet this task belongs to
    is_done: bool = False

    def mark_done(self):
        pass

    def get_duration(self) -> int:
        pass

    def get_priority(self) -> str:
        pass


class Daily_Plan:
    def __init__(self, date: str, owner: Owner):
        self.date = date
        self.owner = owner                   
        self.task_list: List[Task] = []
        self.completed_tasks: List[Task] = []

    @property
    def available_time(self) -> int:
        """Derived from the owner so it never drifts out of sync."""
        return self.owner.available_time

    def add_task(self, task: Task):
        # TODO: check total scheduled duration does not exceed self.available_time
        pass

    def remove_task(self, task: Task):
        pass

    def get_completed(self) -> List[Task]:
        pass

    def get_remaining(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time    # minutes per day
        self.pets: List[Pet] = []
        self.plans: List[Daily_Plan] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet: Pet):
        pass

    def set_availability(self, available_time: int):
        pass

    def get_pets(self) -> List[Pet]:
        pass

    def create_plan(self, _date: str) -> Daily_Plan:
        """Create and register a new Daily_Plan for the given date."""
        pass

    def get_plan_for_date(self, _date: str) -> Optional[Daily_Plan]:
        """Look up an existing plan by date."""
        pass
