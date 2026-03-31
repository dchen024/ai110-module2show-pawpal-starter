from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Optional


@dataclass
class Task:
    title: str
    pet_name: str
    task_type: str  # walk, feeding, medication, grooming, enrichment
    duration_minutes: int
    priority: str  # low, medium, high
    is_recurring: bool = False
    recurrence_interval: Optional[str] = None  # daily, weekly, etc.
    scheduled_time: Optional[datetime] = None
    completed: bool = False

    def mark_completed(self):
        """Set this task's status to completed."""
        self.completed = True

    def is_overdue(self):
        """Return True if the task is past its scheduled time and not completed."""
        if self.completed or self.scheduled_time is None:
            return False
        return datetime.now() > self.scheduled_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    weight: float
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks_by_type(self, task_type: str):
        """Return all tasks matching the given type (e.g. 'walk', 'feeding')."""
        return [task for task in self.tasks if task.task_type == task_type]

    def get_pending_tasks(self):
        """Return all tasks that have not been completed."""
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task: Task):
        """Mark a task as completed and auto-create the next occurrence if recurring."""
        task.mark_completed()
        if task.is_recurring and task.recurrence_interval:
            # Calculate next scheduled time
            days = {"daily": 1, "weekly": 7}
            delta = timedelta(days=days.get(task.recurrence_interval, 1))
            next_time = None
            if task.scheduled_time:
                next_time = task.scheduled_time + delta

            next_task = Task(
                title=task.title,
                pet_name=task.pet_name,
                task_type=task.task_type,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                is_recurring=True,
                recurrence_interval=task.recurrence_interval,
                scheduled_time=next_time,
            )
            self.add_task(next_task)
            return next_task
        return None


@dataclass
class Owner:
    name: str
    email: str
    available_hours: List[List[int]] = field(default_factory=list)  # e.g. [[7, 9], [17, 20]]
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's pet list."""
        self.pets.remove(pet)

    def get_all_tasks(self):
        """Collect and return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner, schedule_date: date = None):
        self.owner = owner
        self.daily_schedule: List[Task] = []
        self.date = schedule_date or date.today()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by scheduled time, with unscheduled tasks at the end."""
        return sorted(tasks, key=lambda t: t.scheduled_time or datetime.max)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return only scheduled tasks belonging to the given pet."""
        return [t for t in self.daily_schedule if t.pet_name == pet_name]

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority: high first, then medium, then low."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 3))

    def detect_conflicts(self) -> List[tuple]:
        """Check the daily schedule for overlapping tasks and return conflict pairs."""
        conflicts = []
        scheduled = [t for t in self.daily_schedule if t.scheduled_time]
        scheduled.sort(key=lambda t: t.scheduled_time)
        for i in range(len(scheduled) - 1):
            current = scheduled[i]
            next_task = scheduled[i + 1]
            current_end = current.scheduled_time.timestamp() + current.duration_minutes * 60
            if current_end > next_task.scheduled_time.timestamp():
                conflicts.append((current, next_task))
        return conflicts

    def generate_schedule(self) -> List[Task]:
        """Build a daily schedule by fitting pending tasks into available time windows by priority."""
        # 1. Get all pending tasks
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_pending_tasks())

        # 2. Sort by priority (high first)
        sorted_tasks = self.sort_by_priority(all_tasks)

        # 3. Fill tasks into available time windows
        self.daily_schedule = []
        for window in self.owner.available_hours:
            window_start = window[0]
            window_end = window[1]
            current_hour = window_start

            for task in sorted_tasks:
                if task in self.daily_schedule:
                    continue  # already scheduled
                task_hours = task.duration_minutes / 60
                if current_hour + task_hours <= window_end:
                    hour = int(current_hour)
                    minute = int((current_hour - hour) * 60)
                    task.scheduled_time = datetime(
                        self.date.year, self.date.month, self.date.day,
                        hour, minute
                    )
                    self.daily_schedule.append(task)
                    current_hour += task_hours

        return self.daily_schedule
