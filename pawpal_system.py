from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

@dataclass
class Task:
    """A single care activity for a pet."""
    description: str
    duration: int       # time in minutes
    frequency: str      # e.g. "daily", "weekly"
    time: str = "00:00"          # scheduled time in HH:MM format
    due_date: date = None        # date this task is due
    is_done: bool = False
    priority: str = "Medium"     # "High", "Medium", or "Low"

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

    def remove_task(self, task: Task) -> str:
        """Remove a care task from this pet. Returns a warning if not found."""
        try:
            self.tasks.remove(task)
            return f"Task '{task.description}' removed."
        except ValueError:
            return f"Warning: task '{task.description}' not found in {self.name}'s task list."

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

    def remove_pet(self, pet: Pet) -> str:
        """Remove a pet from this owner's list. Returns a warning if not found."""
        try:
            self.pets.remove(pet)
            return f"Pet '{pet.name}' removed."
        except ValueError:
            return f"Warning: pet '{pet.name}' not found in owner's pet list."

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
        available time, sorted by priority (High first) then by scheduled time.
        """
        pending = self.get_pending_tasks()
        pending.sort(key=lambda task: (PRIORITY_ORDER.get(task.priority, 1), task.time))
        schedule = []
        total_time = 0
        for task in pending:
            if total_time + task.duration <= self.owner.available_time:
                schedule.append(task)
                total_time += task.duration
        return schedule

    def mark_task_done(self, task: Task, pet: Pet):
        """Mark a task complete; if recurring, add a fresh instance to the pet."""
        task.mark_done()
        if task.is_recurring():
            base = task.due_date if task.due_date is not None else date.today()
            if task.frequency == "daily":
                next_due = base + timedelta(days=1)
            elif task.frequency == "weekly":
                next_due = base + timedelta(weeks=1)
            else:
                next_due = None
            next_task = Task(
                description=task.description,
                duration=task.duration,
                frequency=task.frequency,
                time=task.time,
                due_date=next_due,
                priority=task.priority,
            )
            pet.add_task(next_task)

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by their scheduled time (HH:MM)."""
        tasks = self.owner.get_all_tasks()
        tasks.sort(key=lambda task: task.time)
        return tasks

    def filter_tasks(self, pet_name=None, is_done=None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        if pet_name is not None:
            pets = list(filter(lambda pet: pet.name == pet_name, self.owner.get_pets()))
            tasks = []
            for pet in pets:
                tasks.extend(pet.get_tasks())
        else:
            tasks = self.owner.get_all_tasks()
        if is_done is not None:
            tasks = list(filter(lambda task: task.is_done == is_done, tasks))
        return tasks

    def get_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same time."""
        try:
            all_tasks = self.owner.get_all_tasks()
            time_groups: dict = {}
            for task in all_tasks:
                time_groups.setdefault(task.time, []).append(task)
            warnings = []
            for time, group in time_groups.items():
                if len(group) > 1:
                    names = ", ".join(t.description for t in group)
                    warnings.append(f"Warning: conflict at {time} — {names}")
            return warnings
        except Exception as e:
            return [f"Warning: conflict check failed — {e}"]

    def get_total_scheduled_time(self) -> int:
        """Return the total duration (minutes) of all pending tasks."""
        return sum(task.get_duration() for task in self.get_pending_tasks())
