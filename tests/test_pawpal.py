from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def make_task(title="Walk", priority="medium", duration=30):
    """Helper to quickly create a Task for testing."""
    return Task(
        title=title,
        pet_name="Mochi",
        task_type="walk",
        duration_minutes=duration,
        priority=priority,
    )


def test_mark_completed():
    task = make_task()
    assert task.completed is False
    task.mark_completed()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu", weight=25.0)
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1
    pet.add_task(make_task(title="Feeding"))
    assert len(pet.tasks) == 2


def test_get_pending_tasks_excludes_completed():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu", weight=25.0)
    task1 = make_task(title="Walk")
    task2 = make_task(title="Feed")
    pet.add_task(task1)
    pet.add_task(task2)
    task1.mark_completed()
    pending = pet.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].title == "Feed"


def test_schedule_sorts_by_priority():
    owner = Owner(name="Jordan", email="j@test.com", available_hours=[[7, 12]])
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu", weight=25.0)
    pet.add_task(make_task(title="Low Task", priority="low", duration=30))
    pet.add_task(make_task(title="High Task", priority="high", duration=30))
    pet.add_task(make_task(title="Med Task", priority="medium", duration=30))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner, schedule_date=date(2026, 3, 30))
    schedule = scheduler.generate_schedule()

    assert schedule[0].title == "High Task"
    assert schedule[1].title == "Med Task"
    assert schedule[2].title == "Low Task"


def test_schedule_respects_time_window():
    owner = Owner(name="Jordan", email="j@test.com", available_hours=[[7, 8]])  # only 1 hour
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu", weight=25.0)
    pet.add_task(make_task(title="Task 1", priority="high", duration=30))
    pet.add_task(make_task(title="Task 2", priority="high", duration=30))
    pet.add_task(make_task(title="Task 3", priority="low", duration=30))  # won't fit
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner, schedule_date=date(2026, 3, 30))
    schedule = scheduler.generate_schedule()

    assert len(schedule) == 2  # only 2 fit in 1 hour
