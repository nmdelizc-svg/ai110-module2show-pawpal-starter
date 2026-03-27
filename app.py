import streamlit as st
from pawpal_system import Scheduler, Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
col_a, col_b = st.columns(2)
with col_a:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_b:
    available_time = st.number_input("Available time (minutes/day)", min_value=1, max_value=480, value=60)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time=int(available_time))
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time = int(available_time)

st.subheader("Add a Pet")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_p3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if "pets" not in st.session_state:
    st.session_state.pets = []

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, age=int(age))
    st.session_state.pets.append(new_pet)

if st.session_state.pets:
    st.write("Pets added:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in st.session_state.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Select a pet and add tasks to them.")

if st.session_state.pets:
    pet_labels = [f"{p.name} ({p.species})" for p in st.session_state.pets]
    selected_index = st.selectbox("Assign task to", range(len(pet_labels)), format_func=lambda i: pet_labels[i])
    selected_pet = st.session_state.pets[selected_index]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        new_task = Task(description=task_title, duration=int(duration), frequency=frequency)
        selected_pet.add_task(new_task)

    all_tasks = []
    for p in st.session_state.pets:
        for t in p.get_tasks():
            all_tasks.append({"pet": p.name, "description": t.description, "duration (min)": t.duration, "frequency": t.frequency})
    if all_tasks:
        st.write("Current tasks:")
        st.table(all_tasks)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.divider()

st.subheader("Build Schedule")
st.caption("Builds a daily schedule that fits within the owner's available time.")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        owner = st.session_state.owner
        owner.pets = st.session_state.pets
        st.session_state.scheduler = Scheduler(owner)

if st.session_state.get("scheduler"):
    schedule = st.session_state.scheduler.build_daily_schedule()
    owner = st.session_state.owner
    if schedule:
        st.success(f"Schedule for {owner.name}")
        for task in schedule:
            st.write(f"- **{task.description}** ({task.duration} min, {task.frequency})")
        st.info(f"Total scheduled time: {sum(t.duration for t in schedule)} / {owner.available_time} min available")
    else:
        st.warning("No tasks could be scheduled. Try adding tasks or increasing available time.")
