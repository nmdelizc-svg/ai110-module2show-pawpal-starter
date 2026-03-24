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
        pass

    def get_duration(self) -> int:
        """Return the time required for this task in minutes."""
        pass

    def is_recurring(self) -> bool:
        """Return True if the task repeats on a schedule."""
        pass


@dataclass
class Pet:
    """Stores a pet's details and its associated care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a summary of the pet's details."""
        pass

    def add_task(self, task: Task):
        """Assign a new care task to this pet."""
        pass

    def remove_task(self, task: Task):
        """Remove a care task from this pet."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that have not been completed."""
        pass


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time    # minutes available per day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        pass

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's list."""
        pass

    def get_pets(self) -> List[Pet]:
        """Return all pets owned."""
        pass

    def set_availability(self, available_time: int):
        """Update how many minutes per day the owner has available."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        pass

    def get_all_pending_tasks(self) -> List[Task]:
        """Return every incomplete task across all pets."""
        pass


class Scheduler:
    """The brain — retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_tasks_by_pet(self, _pet: Pet) -> List[Task]:
        """Return all tasks for a specific pet."""
        pass

    def get_tasks_by_frequency(self, _frequency: str) -> List[Task]:
        """Return all tasks that match a given frequency (e.g. 'daily')."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        pass

    def build_daily_schedule(self) -> List[Task]:
        """
        Return an ordered list of tasks that fit within the owner's
        available time, prioritizing pending tasks by duration.
        """
        pass

    def mark_task_done(self, task: Task):
        """Mark a specific task as completed."""
        pass

    def get_total_scheduled_time(self) -> int:
        """Return the total duration (minutes) of all pending tasks."""
        pass
