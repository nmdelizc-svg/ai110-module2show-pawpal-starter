from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_time=80)

# --- Pets ---
buddy    = Pet(name="Buddy",    species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

# --- Buddy's Tasks (added out of order by time) ---
buddy.add_task(Task(description="Bath time",      duration=30, frequency="weekly",  time="14:00"))
buddy.add_task(Task(description="Morning walk",   duration=20, frequency="daily",   time="07:30"))
buddy.add_task(Task(description="Feed breakfast", duration=5,  frequency="daily",   time="08:00"))

# --- Whiskers's Tasks (also out of order, one shares Buddy's 08:00 slot) ---
whiskers.add_task(Task(description="Vet checkup",      duration=45, frequency="monthly", time="11:00"))
whiskers.add_task(Task(description="Feed dinner",      duration=5,  frequency="daily",   time="18:00"))
whiskers.add_task(Task(description="Clean litter box", duration=10, frequency="daily",   time="08:00"))  # conflict!

# --- Register pets with owner ---
owner.add_pet(buddy)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)

# --- Today's Schedule ---
schedule = scheduler.build_daily_schedule()
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
total     = scheduler.get_total_scheduled_time()
scheduled = sum(t.get_duration() for t in schedule)
print(f"Scheduled today: {scheduled} min  |  All pending: {total} min")
print("=" * 40)

# --- Sort by Time ---
print("\n" + "=" * 40)
print("      TASKS SORTED BY TIME")
print("=" * 40)
for task in scheduler.sort_by_time():
    pet_name = next(p.name for p in owner.get_pets() if task in p.get_tasks())
    print(f"  {task.time}  [{pet_name}] {task.description}")

# --- Filter by Pet Name ---
print("\n" + "=" * 40)
print("      BUDDY'S TASKS")
print("=" * 40)
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {task.time}  {task.description} ({task.frequency})")

# --- Filter by Completion Status ---
print("\n" + "=" * 40)
print("      PENDING TASKS (not done)")
print("=" * 40)
for task in scheduler.filter_tasks(is_done=False):
    pet_name = next(p.name for p in owner.get_pets() if task in p.get_tasks())
    print(f"  [{pet_name}] {task.description}")

# --- Conflict Detection ---
print("\n" + "=" * 80)
print("      \t\t\t\t SCHEDULING CONFLICTS")
print("=" * 80)
conflicts = scheduler.get_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")
print("=" * 80)