import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State: keep data alive across re-runs ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")

owner = st.session_state.owner

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
            st.write(f"Window {i+1}: {w[0]}:00 - {w[1]}:00")

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
    # --- Add Task (only shows when pets exist) ---
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

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        new_task = Task(
            title=task_title,
            pet_name=selected_pet,
            task_type=task_type,
            duration_minutes=int(duration),
            priority=priority,
            is_recurring=is_recurring,
        )
        pet.add_task(new_task)
        st.success(f"Added '{task_title}' for {selected_pet}!")

    st.divider()

    # --- Show Current Pets & Tasks ---
    st.subheader("Your Pets & Tasks")
    for pet in owner.pets:
        with st.expander(f"{pet.name} ({pet.species} - {pet.breed})", expanded=True):
            if pet.tasks:
                for task in pet.tasks:
                    status = "✅" if task.completed else "⏳"
                    st.write(f"{status} **{task.title}** — {task.task_type} | {task.duration_minutes} min | {task.priority} priority")
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

    # --- Display Schedule ---
    if "schedule" in st.session_state and st.session_state.schedule:
        schedule_data = []
        for task in st.session_state.schedule:
            schedule_data.append({
                "Time": task.scheduled_time.strftime("%I:%M %p"),
                "Task": task.title,
                "Pet": task.pet_name,
                "Type": task.task_type,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
            })
        st.table(schedule_data)

        if st.session_state.conflicts:
            st.error("⚠️ Scheduling conflicts detected!")
            for a, b in st.session_state.conflicts:
                st.write(f"- {a.title} overlaps with {b.title}")
        else:
            st.success("No conflicts!")

        # Show unscheduled tasks
        all_tasks = owner.get_all_tasks()
        unscheduled = [t for t in all_tasks if t not in st.session_state.schedule and not t.completed]
        if unscheduled:
            st.warning("Some tasks didn't fit in your available hours:")
            for t in unscheduled:
                st.write(f"- {t.title} ({t.pet_name}) — {t.duration_minutes} min, {t.priority}")
