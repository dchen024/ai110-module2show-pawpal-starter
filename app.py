import streamlit as st
from datetime import date, datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State: keep data alive across re-runs ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")
if "schedule" not in st.session_state:
    st.session_state.schedule = []
if "conflicts" not in st.session_state:
    st.session_state.conflicts = []

owner = st.session_state.owner

PRIORITY_COLORS = {"high": "🔴", "medium": "🟡", "low": "🟢"}

# ====== SIDEBAR ======
with st.sidebar:
    st.header("Owner Info")
    owner.name = st.text_input("Owner Name", value=owner.name or "Jordan")
    owner.email = st.text_input("Email", value=owner.email or "jordan@example.com")

    st.subheader("Available Hours")
    st.caption("Add time windows when you're free (24hr format)")
    col1, col2 = st.columns(2)
    with col1:
        window_start = st.number_input("Start hour", min_value=0, max_value=23, value=7)
    with col2:
        window_end = st.number_input("End hour", min_value=1, max_value=24, value=9)
    if st.button("Add time window"):
        owner.available_hours.append([window_start, window_end])

    if owner.available_hours:
        for i, w in enumerate(owner.available_hours):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"Window {i+1}: {w[0]}:00 - {w[1]}:00")
            with col_b:
                if st.button("X", key=f"rm_window_{i}"):
                    owner.available_hours.pop(i)
                    st.rerun()

    st.divider()

    # --- Add Pet ---
    st.subheader("Add a Pet")
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Shiba Inu")
    age = st.number_input("Age", min_value=0, max_value=30, value=3)
    weight = st.number_input("Weight (lbs)", min_value=0.1, max_value=300.0, value=25.0)

    if st.button("Add Pet"):
        new_pet = Pet(name=pet_name, species=species, age=age, breed=breed, weight=weight)
        owner.add_pet(new_pet)
        st.success(f"Added {pet_name}!")

# ====== MAIN AREA ======
st.title("🐾 PawPal+")

if not owner.pets:
    st.info("No pets yet — add one in the sidebar!")
else:
    # --- Add Task ---
    st.subheader("Add a Task")
    pet_names = [p.name for p in owner.pets]
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("For which pet?", pet_names)
        task_title = st.text_input("Task title", value="Morning Walk")
        task_type = st.selectbox("Type", ["walk", "feeding", "medication", "grooming", "enrichment"])
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        is_recurring = st.checkbox("Recurring?")
        recurrence_interval = None
        if is_recurring:
            recurrence_interval = st.selectbox("How often?", ["daily", "weekly"])

    has_fixed_time = st.checkbox("Set a specific time?")
    fixed_time = None
    if has_fixed_time:
        fixed_time = st.time_input("Task time", value=time(8, 0))

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        scheduled_time = None
        if fixed_time:
            scheduled_time = datetime.combine(date.today(), fixed_time)
        new_task = Task(
            title=task_title,
            pet_name=selected_pet,
            task_type=task_type,
            duration_minutes=int(duration),
            priority=priority,
            is_recurring=is_recurring,
            recurrence_interval=recurrence_interval,
            scheduled_time=scheduled_time,
        )
        pet.add_task(new_task)
        st.success(f"Added '{task_title}' for {selected_pet}!")

    st.divider()

    # --- Pets & Tasks ---
    st.subheader("Your Pets & Tasks")
    for pet in owner.pets:
        with st.expander(f"{pet.name} ({pet.species} - {pet.breed})", expanded=True):
            if pet.tasks:
                for i, task in enumerate(pet.tasks):
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        icon = PRIORITY_COLORS.get(task.priority, "⚪")
                        status = "~~" if task.completed else ""
                        check = "✅" if task.completed else icon
                        time_str = ""
                        if task.scheduled_time:
                            time_str = f" @ {task.scheduled_time.strftime('%I:%M %p')}"
                        recurring_str = f" (repeats {task.recurrence_interval})" if task.is_recurring else ""
                        st.markdown(
                            f"{check} {status}**{task.title}**{status} — "
                            f"{task.task_type} | {task.duration_minutes} min | "
                            f"{task.priority}{time_str}{recurring_str}"
                        )
                    with col_b:
                        if not task.completed:
                            if st.button("Done", key=f"complete_{pet.name}_{i}"):
                                next_task = pet.complete_task(task)
                                if next_task:
                                    st.toast(f"'{task.title}' completed! Next one created for {next_task.recurrence_interval}.")
                                else:
                                    st.toast(f"'{task.title}' completed!")
                                st.rerun()
            else:
                st.write("No tasks yet.")

    st.divider()

    # --- Generate Schedule ---
    st.subheader("Daily Schedule")

    if not owner.available_hours:
        st.warning("Add at least one time window in the sidebar first!")
    elif st.button("Generate Schedule"):
        scheduler = Scheduler(owner=owner, schedule_date=date.today())
        schedule = scheduler.generate_schedule()

        if schedule:
            st.session_state.schedule = schedule
            st.session_state.conflicts = scheduler.detect_conflicts()
        else:
            st.warning("No pending tasks to schedule!")
            st.session_state.schedule = []
            st.session_state.conflicts = []

    # --- Display Schedule ---
    if st.session_state.schedule:
        # Filter by pet
        filter_options = ["All Pets"] + [p.name for p in owner.pets]
        pet_filter = st.selectbox("Filter by pet", filter_options, key="pet_filter")

        display_tasks = st.session_state.schedule
        if pet_filter != "All Pets":
            scheduler = Scheduler(owner=owner, schedule_date=date.today())
            scheduler.daily_schedule = st.session_state.schedule
            display_tasks = scheduler.filter_by_pet(pet_filter)

        if display_tasks:
            schedule_data = []
            for task in display_tasks:
                schedule_data.append({
                    "Time": task.scheduled_time.strftime("%I:%M %p"),
                    "Task": task.title,
                    "Pet": task.pet_name,
                    "Type": task.task_type,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": f"{PRIORITY_COLORS.get(task.priority, '')} {task.priority}",
                })
            st.table(schedule_data)
        else:
            st.info(f"No scheduled tasks for {pet_filter}.")

        # Conflicts
        if st.session_state.conflicts:
            st.error("Scheduling conflicts detected!")
            for a, b in st.session_state.conflicts:
                st.warning(
                    f"**{a.title}** ({a.scheduled_time.strftime('%I:%M %p')} - "
                    f"{(a.scheduled_time.replace(minute=a.scheduled_time.minute + a.duration_minutes) if a.scheduled_time.minute + a.duration_minutes < 60 else a.scheduled_time).strftime('%I:%M %p')}) "
                    f"overlaps with **{b.title}** ({b.scheduled_time.strftime('%I:%M %p')})"
                )
        else:
            st.success("No scheduling conflicts!")

        # Unscheduled tasks
        all_tasks = owner.get_all_tasks()
        unscheduled = [t for t in all_tasks if t not in st.session_state.schedule and not t.completed]
        if unscheduled:
            with st.expander("Tasks that didn't fit", expanded=False):
                for t in unscheduled:
                    st.write(f"- {PRIORITY_COLORS.get(t.priority, '')} {t.title} ({t.pet_name}) — {t.duration_minutes} min, {t.priority}")
