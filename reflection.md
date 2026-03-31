# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Core actions a user should be able to perform:**
1. **Pet Management** — Add and manage pets with their details (name, species, age, breed)
2. **Task Management** — Create, edit, and assign care tasks to pets (with duration, priority, and type)
3. **Schedule Viewing** — View the generated daily care plan on a calendar or timeline display

We chose four classes: **Task** (a dataclass representing a single care activity with title, type, duration, priority, and recurrence info), **Pet** (a dataclass holding pet details and a list of its tasks, with methods to add/remove/filter tasks), **Owner** (a dataclass representing the user with their available hours and a list of pets), and **Scheduler** (a regular class that takes an Owner, collects all tasks across their pets, and generates a prioritized daily schedule with conflict detection).

**b. Design changes**

Changed `available_hours` on Owner from `List[int]` to `List[List[int]]` (a list of start/end pairs). This allows an owner to have multiple availability windows with gaps in between (e.g., free 7-9am and 5-8pm), which is more realistic than assuming one continuous block of time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: **priority** (high tasks are scheduled first), **available time windows** (tasks are only placed within the owner's free hours), and **task duration** (a task is skipped if it doesn't fit in the remaining window). Priority was chosen as the primary sort key because a pet owner would always want critical tasks like medication handled before optional ones like grooming.

**b. Tradeoffs**

The scheduler uses a greedy algorithm — it places the highest-priority task first and moves on, never reconsidering. This means it might skip a short low-priority task that could have fit in a gap, in favor of a longer high-priority task that doesn't fit. This tradeoff is reasonable because for pet care, getting the important things done first matters more than maximizing the total number of tasks scheduled.

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

We tested 14 behaviors across the system: task completion, task addition, pending task filtering, priority-based scheduling, time window constraints, recurring task generation (both daily and verifying non-recurring tasks don't create new ones), pet filtering, fixed-time task preservation, flexible tasks filling gaps around fixed tasks, conflict detection for overlapping tasks, and three edge cases (no pets, no tasks, no available hours). These tests are important because they verify both the "happy path" and the boundary conditions that could silently produce incorrect schedules.

**b. Confidence**

4/5 stars. The core scheduling logic, sorting, filtering, recurrence, and conflict detection are all covered by automated tests. Edge cases we would test next: tasks whose duration spans multiple time windows, weekly recurring tasks, and removing a pet that has scheduled tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
