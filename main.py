from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_time=80)

# --- Pets ---
buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

# --- Buddy's Tasks ---
buddy.add_task(Task(description="Morning walk",   duration=20, frequency="daily"))
buddy.add_task(Task(description="Feed breakfast", duration=5,  frequency="daily"))
buddy.add_task(Task(description="Bath time",      duration=30, frequency="weekly"))

# --- Whiskers's Tasks ---
whiskers.add_task(Task(description="Clean litter box", duration=10, frequency="daily"))
whiskers.add_task(Task(description="Feed dinner",      duration=5,  frequency="daily"))
whiskers.add_task(Task(description="Vet checkup",      duration=45, frequency="monthly"))

# --- Register pets with owner ---
owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Build Schedule ---
scheduler = Scheduler(owner)
schedule = scheduler.build_daily_schedule()

# --- Print Today's Schedule ---
print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
print(f"Owner : {owner.name}")
print(f"Available time: {owner.available_time} min")
print("-" * 40)

for i, task in enumerate(schedule, start=1):
    pet_name = next(p.name for p in owner.get_pets() if task in p.get_tasks())
    print(f"{i}. [{pet_name}] {task.description} — {task.get_duration()} min ({task.frequency})")

print("-" * 40)
total = scheduler.get_total_scheduled_time()
scheduled = sum(t.get_duration() for t in schedule)
print(f"Scheduled today: {scheduled} min  |  All pending tasks: {total} min (if you had unlimited time)")
print("=" * 40)
