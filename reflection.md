# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My design has four main classes. The Pet class stores the animal's basic information. The Task class represents a single care activity (like a walk or medication) along with its priority and duration. The Daily Plan class ties everything together by organizing tasks for a specific date and tracking which ones have been completed. The Owner class represents the person caring for the pet, managing their list of pets and setting their daily availability.
- What classes did you include, and what responsibilities did you assign to each?
 - Owner
    - responsability - Manages their pets and sets their daily availability.
    - attributes - name, pets, available_time
    - methods - add_pet(), remove_pet(), set_availability(), get_pets()
 - Pet 
    - responsability - Holds the pets info
    - attributes - Name, species, age
    - methods - get_info()
 - Task 
    - responsability - Has a single care task and its details
    - attributes - task_name, duration, priority, is_done
    - methods - mark_done(), get_duration(), get_priority()
 - Daily_Plan
    - responsability - Holds the scheduled tasks for a specific day and tracks what has already been completed.
    - attributes - date, task_list, completed_tasks, available_time
    - methods - add_task(), remove_task(), get_completed(), get remaining(), get_task_for_date()

**b. Design changes**

- Did your design change during implementation?
   Yes, I made changes twice.
- If yes, describe at least one change and why you made it.
FIRST CHANGES
   Missing Relationships

      Task → Pet — tasks need to be attached to a pet.
      Owner → Daily_Plan — owners need a plans list plus get_plan/create_plan methods
      Daily_Plan → Owner — plans need a back-reference so they aren't orphaned objects

   Logic Bottlenecks

      available_time on both Owner and Daily_Plan → single source of truth on Owner, derived by Daily_Plan
      get_task_for_date on Daily_Plan → move to Owner as get_plan_for_date, where cross-plan lookup belongs
      add_task → enforce available_time so adding a task can't silently exceed the owner's availability

SECOND CHANGES
   After re-reading the implementation plan i made the redesign shift responsibilities away from Daily_Plan, which was doing too much, and distributes it more naturally across the model. Task is simplified, swapping a vague priority field for a meaningful frequency that actually drives scheduling. Pet now owns its tasks directly, which makes more intuitive sense than tasks floating independently or pointing back at pets. Owner is trimmed down to what it actually represents: a person with pets and availability. All scheduling logic is pulled into a new Scheduler class that acts as the central coordinator. It knows the owner, can see across all pets and tasks, and is the only place where planning decisions get made. Daily_Plan is removed entirely because its responsibilities were split between classes that handle them better. This all makes backend much easier aswell.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time (owner availability) - build_daily_schedule checks the owner's available time and only includes tasks whose cumulative duration fits within that range.
Duration - Each task has a duration, and the scheduler uses it to decide what fits.
Completion status - Only pending tasks are considered for the daily schedule via get_pending_tasks().
- How did you decide which constraints mattered most?
Owner available time was treated as the most important thing. If a task does not fit within the owner's day, it simply cannot happen regardless of importance (this will be modified to handle priorities). Completion status was a natural second constraint since scheduling a done task is meaningless. Duration was used as the sorting key so the most tasks possible fit within the available time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
build_daily_schedule sorts tasks by shortest duration first. This means a long but critical task could be skipped if shorter tasks fill up the owner's available time
- Why is that tradeoff reasonable for this scenario?
Why is that tradeoff reasonable for this scenario?
For everyday pet care, most tasks are short and recurring, so fitting the most tasks in a day is generally the right goal. The app does not yet have a priority/urgency field on tasks, so duration is the best available proxy.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
