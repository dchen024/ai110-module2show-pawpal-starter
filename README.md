# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit-based pet care planning assistant that helps busy pet owners stay on top of daily care routines. It tracks tasks like walks, feedings, medications, and grooming, then generates an optimized daily schedule based on priorities and time constraints.

## Features

- **Owner & Pet Management** — Add pets with details (species, breed, age, weight) and set your available hours as multiple time windows
- **Task Management** — Create tasks with type, duration, priority, optional fixed time, and recurrence settings
- **Priority-based Scheduling** — High-priority tasks (e.g., medication) are always scheduled before lower-priority ones
- **Fixed & Flexible Tasks** — Set a specific time for must-happen tasks; the scheduler fills flexible tasks into the gaps around them
- **Recurring Tasks** — Daily or weekly tasks automatically generate their next occurrence when marked complete
- **Conflict Detection** — Overlapping fixed-time tasks are flagged with warnings in the UI
- **Filtering** — Filter the schedule view by pet name
- **Mark Complete** — Complete tasks directly in the UI, triggering recurrence logic automatically

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

### Run the CLI Demo

```bash
python main.py
```

## Architecture

The system is built with four core classes in `pawpal_system.py`:

| Class | Role |
|-------|------|
| **Task** | Dataclass representing a single care activity (title, type, duration, priority, time, recurrence) |
| **Pet** | Dataclass holding pet details and managing its task list, including recurring task creation |
| **Owner** | Dataclass representing the user with availability windows and a list of pets |
| **Scheduler** | The scheduling engine that collects tasks, respects fixed times, fills gaps with flexible tasks by priority, and detects conflicts |

See `uml_final.md` for the full Mermaid.js class diagram.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

**14 tests** covering:
- Task completion and recurring task generation
- Adding/removing tasks from pets
- Priority-based scheduling order
- Time window constraints (tasks that don't fit are excluded)
- Fixed-time tasks retain their set time while flexible tasks fill gaps
- Conflict detection for overlapping fixed-time tasks
- Edge cases: no pets, no tasks, no available hours

**Confidence Level:** 4/5 — Core scheduling, sorting, filtering, recurrence, and conflict detection are well-tested. Additional edge cases like tasks spanning multiple windows could be explored with more time.
