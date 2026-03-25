from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single care activity for a pet."""
    description: str
    duration: int       # time in minutes
    frequency: str      # e.g. "daily", "weekly"
    is_done: bool = False

    def mark_done(self):
        """Mark this task as completed."""
        self.is_done = True

    def get_duration(self) -> int:
        """Return the time required for this task in minutes."""
        return self.duration

    def is_recurring(self) -> bool:
        """Return True if the task repeats on a schedule."""
        return self.frequency != "once"


@dataclass
class Pet:
    """Stores a pet's details and its associated care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a summary of the pet's details."""
        return f"{self.name} ({self.species}, age {self.age})"

    def add_task(self, task: Task):
        """Assign a new care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a care task from this pet."""
        self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that have not been completed."""
        return [task for task in self.tasks if not task.is_done]


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time    # minutes available per day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's list."""
        self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned."""
        return self.pets

    def set_availability(self, available_time: int):
        """Update how many minutes per day the owner has available."""
        self.available_time = available_time

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return every incomplete task across all pets."""
        pending_tasks = []
        for pet in self.pets:
            pending_tasks.extend(pet.get_pending_tasks())
        return pending_tasks


class Scheduler:
    """The brain — retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_tasks_by_pet(self, _pet: Pet) -> List[Task]:
        """Return all tasks for a specific pet."""
        return _pet.get_tasks()

    def get_tasks_by_frequency(self, _frequency: str) -> List[Task]:
        """Return all tasks that match a given frequency (e.g. 'daily')."""
        return [task for task in self.owner.get_all_tasks() if task.frequency == _frequency]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        return self.owner.get_all_pending_tasks()

    def build_daily_schedule(self) -> List[Task]:
        """
        Return an ordered list of tasks that fit within the owner's
        available time, prioritizing pending tasks by duration.
        """
        pending = self.get_pending_tasks()
        pending.sort(key=lambda task: task.duration)
        schedule = []
        total_time = 0
        for task in pending:
            if total_time + task.duration <= self.owner.available_time:
                schedule.append(task)
                total_time += task.duration
        return schedule

    def mark_task_done(self, task: Task):
        """Mark a specific task as completed."""
        task.mark_done()

    def get_total_scheduled_time(self) -> int:
        """Return the total duration (minutes) of all pending tasks."""
        return sum(task.get_duration() for task in self.get_pending_tasks())
