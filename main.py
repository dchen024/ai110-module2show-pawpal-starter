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

# --- Add Tasks ---
mochi.add_task(Task(
    title="Morning Walk",
    pet_name="Mochi",
    task_type="walk",
    duration_minutes=30,
    priority="high"
))

mochi.add_task(Task(
    title="Flea Medication",
    pet_name="Mochi",
    task_type="medication",
    duration_minutes=10,
    priority="high"
))

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
    priority="medium"
))

whiskers.add_task(Task(
    title="Play Time",
    pet_name="Whiskers",
    task_type="enrichment",
    duration_minutes=20,
    priority="medium"
))

# --- Generate Schedule ---
scheduler = Scheduler(owner=owner, schedule_date=date.today())
schedule = scheduler.generate_schedule()

# --- Print Schedule ---
print(f"📋 {owner.name}'s PawPal+ Schedule for {scheduler.date}")
print(f"   Available windows: {['{}:00-{}:00'.format(w[0], w[1]) for w in owner.available_hours]}")
print("-" * 50)

for task in schedule:
    time_str = task.scheduled_time.strftime("%I:%M %p")
    print(f"  {time_str} | {task.title:<20} | {task.pet_name:<10} | {task.priority} | {task.duration_minutes} min")

print("-" * 50)
print(f"  Total tasks scheduled: {len(schedule)}")

# --- Check for conflicts ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n⚠️  Conflicts detected:")
    for a, b in conflicts:
        print(f"  {a.title} overlaps with {b.title}")
else:
    print("\n✅ No scheduling conflicts!")

# --- Show unscheduled tasks ---
all_tasks = owner.get_all_tasks()
unscheduled = [t for t in all_tasks if t not in schedule]
if unscheduled:
    print(f"\n⏳ Tasks that didn't fit:")
    for task in unscheduled:
        print(f"  - {task.title} ({task.pet_name}) | {task.priority} | {task.duration_minutes} min")
