from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Create Owner ---
owner = Owner(
    name="Jordan",
    email="jordan@example.com",
    available_hours=[[7, 9], [17, 20]]  # free 7-9am and 5-8pm
)

# --- Create Pets ---
mochi = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu", weight=25.0)
whiskers = Pet(name="Whiskers", species="cat", age=5, breed="Tabby", weight=10.0)

owner.add_pet(mochi)
owner.add_pet(whiskers)

# --- Add Tasks (intentionally out of order to test sorting) ---
mochi.add_task(Task(
    title="Grooming Session",
    pet_name="Mochi",
    task_type="grooming",
    duration_minutes=45,
    priority="low"
))

whiskers.add_task(Task(
    title="Evening Feeding",
    pet_name="Whiskers",
    task_type="feeding",
    duration_minutes=15,
    priority="medium",
    is_recurring=True,
    recurrence_interval="daily"
))

mochi.add_task(Task(
    title="Morning Walk",
    pet_name="Mochi",
    task_type="walk",
    duration_minutes=30,
    priority="high",
    is_recurring=True,
    recurrence_interval="daily"
))

mochi.add_task(Task(
    title="Flea Medication",
    pet_name="Mochi",
    task_type="medication",
    duration_minutes=10,
    priority="high"
))

whiskers.add_task(Task(
    title="Play Time",
    pet_name="Whiskers",
    task_type="enrichment",
    duration_minutes=20,
    priority="medium"
))

# === 1. Generate Schedule ===
print("=" * 55)
print(f"  {owner.name}'s PawPal+ Schedule for {date.today()}")
print(f"  Available: {['{}:00-{}:00'.format(w[0], w[1]) for w in owner.available_hours]}")
print("=" * 55)

scheduler = Scheduler(owner=owner, schedule_date=date.today())
schedule = scheduler.generate_schedule()

for task in schedule:
    time_str = task.scheduled_time.strftime("%I:%M %p")
    print(f"  {time_str} | {task.title:<20} | {task.pet_name:<10} | {task.priority} | {task.duration_minutes} min")

print(f"\n  Total scheduled: {len(schedule)}")

# === 2. Sort by Time ===
print("\n--- Sorted by Time ---")
by_time = scheduler.sort_by_time(schedule)
for task in by_time:
    print(f"  {task.scheduled_time.strftime('%I:%M %p')} | {task.title}")

# === 3. Filter by Pet ===
print("\n--- Mochi's Tasks Only ---")
mochi_tasks = scheduler.filter_by_pet("Mochi")
for task in mochi_tasks:
    print(f"  {task.title} | {task.duration_minutes} min | {task.priority}")

print("\n--- Whiskers' Tasks Only ---")
whiskers_tasks = scheduler.filter_by_pet("Whiskers")
for task in whiskers_tasks:
    print(f"  {task.title} | {task.duration_minutes} min | {task.priority}")

# === 4. Conflict Detection ===
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n⚠️  Conflicts detected:")
    for a, b in conflicts:
        print(f"  {a.title} overlaps with {b.title}")
else:
    print("\n✅ No scheduling conflicts!")

# === 5. Recurring Tasks ===
print("\n--- Recurring Task Demo ---")
walk_task = mochi.tasks[1]  # Morning Walk (added second, index 1)
print(f"  Completing '{walk_task.title}' (recurring: {walk_task.recurrence_interval})")
next_task = mochi.complete_task(walk_task)
print(f"  Original completed: {walk_task.completed}")
if next_task:
    print(f"  Next occurrence created: '{next_task.title}' scheduled for {next_task.scheduled_time}")
    print(f"  Mochi's total tasks now: {len(mochi.tasks)}")

# === 6. Unscheduled Tasks ===
all_tasks = owner.get_all_tasks()
unscheduled = [t for t in all_tasks if t not in schedule and not t.completed]
if unscheduled:
    print(f"\n⏳ Unscheduled tasks:")
    for task in unscheduled:
        print(f"  - {task.title} ({task.pet_name}) | {task.priority} | {task.duration_minutes} min")
