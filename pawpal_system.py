from dataclasses import dataclass, field
from datetime import datetime, date
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
        pass

    def is_overdue(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    weight: float
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_tasks_by_type(self, task_type: str):
        pass

    def get_pending_tasks(self):
        pass


@dataclass
class Owner:
    name: str
    email: str
    available_hours: List[int] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet: Pet):
        pass

    def get_all_tasks(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner, schedule_date: date = None):
        self.owner = owner
        self.daily_schedule: List[Task] = []
        self.date = schedule_date or date.today()

    def generate_schedule(self):
        pass

    def detect_conflicts(self):
        pass

    def sort_by_priority(self):
        pass
