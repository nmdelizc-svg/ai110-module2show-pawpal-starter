# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


### Smarter Scheduling
PawPal+ received a full data model and scheduling engine built around three core classes. The Pet class now stores a list of care tasks and exposes methods to add, remove, and filter them by completion status. The Owner class tracks daily available time in minutes and aggregates tasks across all owned pets. The Task class captures each care activity with a description, duration, scheduled time, frequency, and due date, and supports recurring task logic so completing a daily or weekly task automatically queues the next occurrence.

The Scheduler class serves as the central brain of the app. It implements a greedy daily schedule builder that sorts pending tasks by shortest duration first and fills the owner's time budget without going over. Additional methods let you sort all tasks by their scheduled time slot, filter tasks by pet or completion status, and detect conflicts when two tasks share the same time slot. A demo script in main.py exercises all of these features and prints formatted output showing today's schedule, time-sorted tasks, per-pet filters, pending tasks, and any scheduling conflicts detected.

### Testing PawPal+
 # Command to run tests:
 python -m pytest
 # Description of tests created
 test_mark_done_changes_status - This confirms a task starts as not done and flips it to done after calling mark_done().
 test_add_task_increases_pet_task_count - Makes sure each call to add_task() actually appends to the pet's task list and they aren't dropped or duplicated.
 test_build_daily_schedule_respects_available_time - Checks that the scheduler never schedules more minutes than the owner has available.
 test_sort_by_time_returns_chronological_order - Adds tasks out of order and verifies sort_by_time() returns them in order. 
 test_mark_task_done_daily_creates_next_day_task - Marks a daily task complete and asserts a new identical task is created with a due date exactly one day later.
 test_get_conflicts_flags_duplicate_times - Schedules two tasks at the same time and one at a different time, then confirms exactly one conflict warning is returned naming both overlapping tasks. 
 test_hardest_combined_edge_cases - A full stress test: one pet with no tasks, one pet with a time conflict, an overflow task, and a past-due recurring task 
 # Confidence Level
  ☆ ☆ ☆ ☆ ☆