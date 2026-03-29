import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta
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


def test_sort_by_time_returns_chronological_order():
    """Verify tasks are returned in chronological HH:MM order regardless of insertion order."""
    owner = Owner(name="Alex", available_time=120)
    pet = Pet(name="Buddy", species="Dog", age=3)
    # Added out of order on purpose
    pet.add_task(Task(description="Evening walk",   duration=30, frequency="daily", time="18:00"))
    pet.add_task(Task(description="Morning meds",   duration=5,  frequency="daily", time="07:30"))
    pet.add_task(Task(description="Afternoon play", duration=20, frequency="daily", time="13:00"))
    pet.add_task(Task(description="Midnight check", duration=5,  frequency="once",  time="00:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got: {times}"


def test_mark_task_done_daily_creates_next_day_task():
    """Confirm marking a daily task complete adds a new task due the following day."""
    owner = Owner(name="Alex", available_time=60)
    pet = Pet(name="Luna", species="Cat", age=2)
    today = date.today()
    task = Task(description="Feed breakfast", duration=10, frequency="daily", due_date=today)
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_done(task, pet)

    # Original task is done
    assert task.is_done is True

    # A new pending task must exist
    pending = pet.get_pending_tasks()
    assert len(pending) == 1, "Expected exactly one new recurring task"

    next_task = pending[0]
    assert next_task.description == "Feed breakfast"
    assert next_task.due_date == today + timedelta(days=1), (
        f"Expected due date {today + timedelta(days=1)}, got {next_task.due_date}"
    )
    assert next_task.is_done is False


def test_get_conflicts_flags_duplicate_times():
    """Verify the Scheduler returns a warning when two tasks share the same scheduled time."""
    owner = Owner(name="Alex", available_time=120)
    pet = Pet(name="Rex", species="Dog", age=4)
    pet.add_task(Task(description="Morning walk", duration=30, frequency="daily",  time="08:00"))
    pet.add_task(Task(description="Morning meds", duration=5,  frequency="daily",  time="08:00"))
    pet.add_task(Task(description="Evening walk", duration=30, frequency="daily",  time="18:00"))  # no conflict
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.get_conflicts()

    assert len(conflicts) == 1, f"Expected 1 conflict warning, got {len(conflicts)}: {conflicts}"
    assert "08:00" in conflicts[0]
    assert "Morning walk" in conflicts[0]
    assert "Morning meds" in conflicts[0]


def test_hardest_combined_edge_case():
    """
    Hardest combined scenario:
    - One pet has no tasks (Rex)
    - One pet has a conflict (two tasks at 08:00), an overflow task, and a past-due recurring task
    - build_daily_schedule fits exactly at the limit (60 min), excluding the overflow
    - Completing the recurring task creates a next-day copy
    - filter_tasks on the empty pet returns []
    - get_conflicts detects the 08:00 collision
    - get_total_scheduled_time counts only pending tasks
    """
    owner = Owner(name="Alex", available_time=60)

    # Pet with no tasks
    rex = Pet(name="Rex", species="Dog", age=5)
    owner.add_pet(rex)

    # Pet with a conflict, overflow, and a past-due recurring task
    luna = Pet(name="Luna", species="Cat", age=3)
    yesterday = date.today() - timedelta(days=1)

    walk = Task(description="Walk",  duration=30, frequency="daily",  time="08:00", due_date=yesterday)
    meds = Task(description="Meds",  duration=30, frequency="weekly", time="08:00")   # conflict with walk
    bath = Task(description="Bath",  duration=40, frequency="once",   time="09:00")   # overflows (30+30+40=100)

    luna.add_task(walk)
    luna.add_task(meds)
    luna.add_task(bath)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    # 1. Schedule fits exactly at 60 min; bath (40 min) must be excluded
    schedule = scheduler.build_daily_schedule()
    total = sum(t.get_duration() for t in schedule)
    assert total == 60, f"Expected schedule total of 60, got {total}"
    assert all(t.description != "Bath" for t in schedule)

    # 2. Conflict at 08:00 is detected
    conflicts = scheduler.get_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]

    # 3. Completing the daily walk (past due_date) creates a task due today
    scheduler.mark_task_done(walk, luna)
    assert walk.is_done is True
    pending = luna.get_pending_tasks()
    new_walk = next((t for t in pending if t.description == "Walk"), None)
    assert new_walk is not None, "Expected a new Walk task after completing the recurring one"
    assert new_walk.due_date == date.today(), (
        f"Expected new walk due today ({date.today()}), got {new_walk.due_date}"
    )

    # 4. filter_tasks on Rex (no tasks) returns empty list
    rex_tasks = scheduler.filter_tasks(pet_name="Rex")
    assert rex_tasks == [], f"Expected [] for Rex, got {rex_tasks}"

    # 5. get_total_scheduled_time counts only pending tasks (walk is now done)
    # pending = meds(30) + bath(40) + new_walk(30) = 100
    # if broken and counting all tasks including done walk: 30+30+40+30 = 130 → caught
    total_pending_time = scheduler.get_total_scheduled_time()
    assert total_pending_time == 100, (
        f"Expected 100 min (meds+bath+new_walk), got {total_pending_time} — "
        "done walk may be incorrectly counted"
    )
