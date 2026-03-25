import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_done_changes_status():
    """Verify that calling mark_done() actually changes the task's is_done status."""
    task = Task(description="Morning walk", duration=20, frequency="daily")
    assert task.is_done is False
    task.mark_done()
    assert task.is_done is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Feed breakfast", duration=5, frequency="daily"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task(description="Bath time", duration=30, frequency="weekly"))
    assert len(pet.get_tasks()) == 2


def test_build_daily_schedule_respects_available_time():
    """Verify that build_daily_schedule never exceeds the owner's available time."""
    owner = Owner(name="Alex", available_time=25)
    pet = Pet(name="Whiskers", species="Cat", age=5)
    pet.add_task(Task(description="Feed dinner",      duration=5,  frequency="daily"))
    pet.add_task(Task(description="Clean litter box", duration=10, frequency="daily"))
    pet.add_task(Task(description="Vet checkup",      duration=45, frequency="monthly"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule()
    total = sum(t.get_duration() for t in schedule)

    assert total <= owner.available_time
    # The 45-min vet checkup must be excluded
    assert all(t.description != "Vet checkup" for t in schedule)
