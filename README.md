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

## Smarter Scheduling

PawPal+ includes several algorithmic features to manage pet care intelligently:

- **Priority-based scheduling** — High-priority tasks (e.g., medication) are always scheduled before lower-priority ones
- **Time window fitting** — Tasks are placed into the owner's available hours, skipping tasks that don't fit
- **Recurring tasks** — Daily or weekly tasks automatically generate their next occurrence when completed
- **Conflict detection** — The scheduler checks for overlapping tasks and warns the user
- **Filtering** — View tasks by pet name, type, or completion status
- **Sorting** — Sort tasks by time or priority
- **Fixed-time support** — Tasks can have a user-set time; the scheduler fills flexible tasks around them

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

The tests cover:
- Task completion and recurring task generation
- Adding/removing tasks from pets
- Priority-based scheduling order
- Time window constraints (tasks that don't fit are excluded)
- Fixed-time tasks retain their set time while flexible tasks fill gaps
- Conflict detection for overlapping fixed-time tasks
- Edge cases: no pets, no tasks, no available hours

**Confidence Level:** ⭐⭐⭐⭐ (4/5) — Core scheduling, sorting, filtering, recurrence, and conflict detection are well-tested. Additional edge cases like very long tasks spanning multiple windows could be explored with more time.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
