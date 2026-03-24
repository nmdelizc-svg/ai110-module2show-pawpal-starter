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
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
