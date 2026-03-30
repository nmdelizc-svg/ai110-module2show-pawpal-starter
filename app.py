import streamlit as st
from pawpal_system import Scheduler, Owner, Pet, Task


def fmt_time(hhmm: str) -> str:
    """Convert 24h 'HH:MM' stored on a task to a readable '12:30 PM' string."""
    try:
        h, m = int(hhmm.split(":")[0]), int(hhmm.split(":")[1])
        period = "AM" if h < 12 else "PM"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d} {period}"
    except Exception:
        return hhmm


def to_24h(hour: int, minute: int, period: str) -> str:
    """Convert 12h hour/minute/AM-PM to a zero-padded 24h 'HH:MM' string."""
    if period == "AM":
        h24 = 0 if hour == 12 else hour
    else:
        h24 = 12 if hour == 12 else hour + 12
    return f"{h24:02d}:{minute:02d}"

PRIORITY_EMOJI = {"High": "🔴 High", "Medium": "🟡 Medium", "Low": "🟢 Low"}

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Theme: space + pink/blue ──────────────────────────────────────────────────
st.markdown("""
<style>

/* ── BUTTONS — gradient border glow effect ──────────────────────────────────
   .stButton is the div Streamlit wraps every button in.
   We use it as the "container" to create the pink-to-blue glowing border. */

/* Gradient border wrapper around every button */
.stButton {
    padding: 3px;
    background: linear-gradient(90deg, #03a9f4, #f441a5);
    border-radius: 0.9em;
    display: inline-block;
}

/* The button itself — dark fill so the gradient border shows around it */
.stButton > button {
    padding: 0.6em 0.8em;
    border-radius: 0.5em;
    border: none !important;
    background-color: #0b0b2a !important;
    color: #fff !important;
    cursor: pointer;
    width: 100%;
    transition: box-shadow 0.4s ease, background-color 0.4s ease;
}

/* Hover: the glow spreads out using box-shadow — works reliably in Streamlit */
.stButton > button:hover {
    background-color: #130a2e !important;
    box-shadow: 0 0 14px #03a9f4, 0 0 14px #f441a5;
}
.stButton > button:active {
    box-shadow: 0 0 5px #03a9f4, 0 0 5px #f441a5;
}

/* Hide the "Press Enter to submit form" hint text inside forms */
[data-testid="InputInstructions"] { display: none !important; }

/* ── INPUTS & SELECTBOXES ───────────────────────────────────────────────────
   Default: dark blue border. Hover: light blue. Focused/typing: pink glow. */

[data-baseweb="input"],
[data-baseweb="select"],
[data-baseweb="textarea"] {
    background: rgba(255,255,255,0.05) !important;
    border-color: #2a4a9e !important;
    border-radius: 6px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-baseweb="input"]:hover,
[data-baseweb="select"]:hover {
    border-color: #7eb8ff !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="select"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: #ff6eb4 !important;
    box-shadow: 0 0 8px rgba(255,110,180,0.35) !important;
}
input, textarea { color: #e0ecff !important; background: transparent !important; }

</style>
""", unsafe_allow_html=True)

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — build a daily schedule that fits your life.")

# ── Session state init ────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── Owner ─────────────────────────────────────────────────────────────────────
st.subheader("Owner")
col_a, col_b = st.columns(2)
with col_a:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_b:
    available_time = st.number_input(
        "Available time (minutes/day)", min_value=1, max_value=480, value=60
    )

if st.session_state.owner is None:
    st.session_state.owner = Owner(name=owner_name, available_time=int(available_time))
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time = int(available_time)

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species_choice = st.selectbox("Species", ["dog", "cat", "other"])
with col_p3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if species_choice == "other":
    custom_species = st.text_input("What kind of pet?", placeholder="e.g. rabbit, hamster, parrot…")
    species = custom_species.strip() if custom_species.strip() else "other"
else:
    species = species_choice

if st.button("Add pet"):
    if species_choice == "other" and not custom_species.strip():
        st.warning("⚠️ Please describe the pet type before adding.")
        new_pet = None
    else:
        new_pet = Pet(name=pet_name, species=species, age=int(age))
    if new_pet:
        st.session_state.pets.append(new_pet)
        st.session_state.scheduler = None
        st.success(f"Added **{pet_name}** the {species}!")

if st.session_state.pets:
    st.table(
        [{"Name": p.name, "Species": p.species, "Age (yrs)": p.age}
         for p in st.session_state.pets]
    )
else:
    st.info("No pets yet. Add one above.")

# ── Add a Task ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Task")
st.caption("Select a pet and assign a care task with a scheduled time.")

if st.session_state.pets:
    pet_labels = [f"{p.name} ({p.species})" for p in st.session_state.pets]
    selected_index = st.selectbox(
        "Assign task to",
        range(len(pet_labels)),
        format_func=lambda i: pet_labels[i],
    )
    selected_pet = st.session_state.pets[selected_index]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
    with col4:
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        task_hour = st.selectbox("Hour", list(range(1, 13)), index=7, key="task_hour")
    with tc2:
        task_minute = st.selectbox("Minute", [0, 15, 30, 45], format_func=lambda m: f"{m:02d}", key="task_minute")
    with tc3:
        task_period = st.selectbox("AM / PM", ["AM", "PM"], key="task_period")

    if st.button("Add task"):
        task_time = to_24h(task_hour, task_minute, task_period)
        new_task = Task(
            description=task_title,
            duration=int(duration),
            frequency=frequency,
            time=task_time,
            priority=priority,
        )
        selected_pet.add_task(new_task)
        st.session_state.scheduler = None
        st.success(f"Task **{task_title}** added to {selected_pet.name} at {fmt_time(task_time)}.")
else:
    st.info("Add a pet first before adding tasks.")

# ── Task View with Scheduler methods ─────────────────────────────────────────
st.divider()
st.subheader("Task Overview")

if st.session_state.pets:
    # Build a temporary scheduler just for viewing — schedule button builds the real one
    view_scheduler = Scheduler(st.session_state.owner)
    st.session_state.owner.pets = st.session_state.pets

    # ── Filter & sort controls ────────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        filter_pet_opts = ["All pets"] + [p.name for p in st.session_state.pets]
        filter_pet = st.selectbox("Filter by pet", filter_pet_opts, key="filter_pet")
    with fc2:
        filter_freq = st.selectbox(
            "Filter by frequency", ["All", "daily", "weekly", "once"], key="filter_freq"
        )
    with fc3:
        filter_priority = st.selectbox(
            "Filter by priority", ["All", "High", "Medium", "Low"], key="filter_priority"
        )
    with fc4:
        sort_mode = st.selectbox(
            "Sort by", ["Added order", "Scheduled time", "Duration", "Priority"], key="sort_mode"
        )

    # Resolve pet name filter
    pet_name_filter = None if filter_pet == "All pets" else filter_pet

    # Use Scheduler.filter_tasks() for pet/status filtering
    filtered = view_scheduler.filter_tasks(pet_name=pet_name_filter)

    # Apply frequency filter manually (filter_tasks doesn't expose frequency)
    if filter_freq != "All":
        filtered = [t for t in filtered if t.frequency == filter_freq]

    # Apply priority filter
    if filter_priority != "All":
        filtered = [t for t in filtered if t.priority == filter_priority]

    # Apply sort via Scheduler.sort_by_time() or plain duration/priority sort
    if sort_mode == "Scheduled time":
        sorted_all = view_scheduler.sort_by_time()
        # Keep only tasks that survived the filter
        filtered_set = set(id(t) for t in filtered)
        filtered = [t for t in sorted_all if id(t) in filtered_set]
    elif sort_mode == "Duration":
        filtered = sorted(filtered, key=lambda t: t.duration)
    elif sort_mode == "Priority":
        from pawpal_system import PRIORITY_ORDER
        filtered = sorted(filtered, key=lambda t: (PRIORITY_ORDER.get(t.priority, 1), t.time))

    # Build stable key lookup: id(task) → (pet_idx, task_idx) for checkbox keys
    # Also build pet-name lookup for display
    pet_of: dict = {}
    task_key: dict = {}
    for pi, p in enumerate(st.session_state.pets):
        for ti, t in enumerate(p.get_tasks()):
            pet_of[id(t)] = p.name
            task_key[id(t)] = (pi, ti)

    if "editing_task" not in st.session_state:
        st.session_state.editing_task = None  # stores (pi, ti) of task being edited

    if filtered:
        # Header row
        hc = st.columns([1.8, 2.5, 1.5, 1.5, 1.2, 1.5, 1, 1])
        for col, label in zip(hc, ["Pet", "Task", "Priority", "Time", "Duration", "Frequency", "Done", "Edit"]):
            col.markdown(f"**{label}**")
        st.divider()

        for t in filtered:
            pi, ti = task_key.get(id(t), (-1, -1))
            rc = st.columns([1.8, 2.5, 1.5, 1.5, 1.2, 1.5, 1, 1])
            rc[0].write(pet_of.get(id(t), "—"))
            rc[1].write(t.description)
            rc[2].write(PRIORITY_EMOJI.get(t.priority, t.priority))
            rc[3].write(fmt_time(t.time))
            rc[4].write(f"{t.duration} min")
            rc[5].write(t.frequency)
            checked = rc[6].checkbox(
                "done",
                value=t.is_done,
                key=f"done_{pi}_{ti}",
                label_visibility="collapsed",
            )
            if checked and not t.is_done:
                t.mark_done()
                st.rerun()
            if rc[7].button("✏️", key=f"edit_{pi}_{ti}", help="Edit this task"):
                st.session_state.editing_task = (pi, ti)
                st.rerun()

            # Inline edit form — shown directly below the row being edited
            if st.session_state.editing_task == (pi, ti):
                with st.form(key=f"edit_form_{pi}_{ti}"):
                    st.markdown(f"**Editing:** {t.description}")
                    ec1, ec2, ec3, ec4 = st.columns(4)
                    new_desc = ec1.text_input("Task title", value=t.description)
                    new_dur  = ec2.number_input("Duration (min)", min_value=1, max_value=240, value=t.duration)
                    new_freq = ec3.selectbox("Frequency", ["daily", "weekly", "once"],
                                             index=["daily", "weekly", "once"].index(t.frequency))
                    cur_priority = t.priority if t.priority in ["High", "Medium", "Low"] else "Medium"
                    new_priority = ec4.selectbox("Priority", ["High", "Medium", "Low"],
                                                 index=["High", "Medium", "Low"].index(cur_priority))
                    tc1, tc2, tc3 = st.columns(3)
                    # Parse current stored 24h time back to 12h for the pickers
                    try:
                        cur_h24 = int(t.time.split(":")[0])
                        cur_min = int(t.time.split(":")[1])
                    except Exception:
                        cur_h24, cur_min = 8, 0
                    cur_period = "AM" if cur_h24 < 12 else "PM"
                    cur_h12 = cur_h24 % 12 or 12
                    new_hour   = tc1.selectbox("Hour", list(range(1, 13)),
                                               index=cur_h12 - 1, key=f"eh_{pi}_{ti}")
                    new_minute = tc2.selectbox("Minute", [0, 15, 30, 45],
                                               index=[0, 15, 30, 45].index(cur_min) if cur_min in [0, 15, 30, 45] else 0,
                                               format_func=lambda m: f"{m:02d}", key=f"em_{pi}_{ti}")
                    new_period = tc3.selectbox("AM / PM", ["AM", "PM"],
                                               index=0 if cur_period == "AM" else 1, key=f"ep_{pi}_{ti}")
                    sc1, sc2 = st.columns(2)
                    save    = sc1.form_submit_button("Save changes")
                    cancel  = sc2.form_submit_button("Cancel")

                if save:
                    t.description = new_desc
                    t.duration    = int(new_dur)
                    t.frequency   = new_freq
                    t.time        = to_24h(new_hour, new_minute, new_period)
                    t.priority    = new_priority
                    st.session_state.editing_task = None
                    st.session_state.scheduler = None
                    st.success(f"Task updated to **{new_desc}** at {fmt_time(t.time)}.")
                    st.rerun()
                if cancel:
                    st.session_state.editing_task = None
                    st.rerun()
    else:
        st.info("No tasks match the current filters.")

    # ── Conflict detection ────────────────────────────────────────────────────
    conflicts = view_scheduler.get_conflicts()
    if conflicts:
        st.markdown("**Scheduling Conflicts Detected**")
        for msg in conflicts:
            # Multiple tasks at the exact same time is a hard conflict → red
            st.error(f"🚨 {msg}")

    # ── Time budget advisory ──────────────────────────────────────────────────
    total_pending = view_scheduler.get_total_scheduled_time()
    budget = st.session_state.owner.available_time
    if total_pending > budget * 1.5:
        # Well over budget — real risk of nothing getting done
        st.error(
            f"🚨 Total pending task time ({total_pending} min) is more than 1.5× your "
            f"available time ({budget} min). Many tasks will be skipped — reduce task load "
            f"or increase available time."
        )
    elif total_pending > budget:
        # Slightly over — soft reminder
        st.warning(
            f"⚠️ Total pending task time ({total_pending} min) exceeds your available "
            f"time ({budget} min). Some tasks won't make it into today's schedule."
        )

else:
    st.info("Add a pet and some tasks to see the task overview.")

# ── Build Schedule ────────────────────────────────────────────────────────────
st.divider()
st.subheader("Build Schedule")
st.caption("Builds a daily schedule that fits within the owner's available time.")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.warning("⚠️ Add at least one pet before generating a schedule.")
    else:
        owner = st.session_state.owner
        owner.pets = st.session_state.pets
        st.session_state.scheduler = Scheduler(owner)

if st.session_state.scheduler:
    scheduler: Scheduler = st.session_state.scheduler
    owner = st.session_state.owner
    schedule = scheduler.build_daily_schedule()

    if schedule:
        total_sched = sum(t.duration for t in schedule)
        st.success(
            f"Schedule ready for **{owner.name}** — "
            f"{total_sched} of {owner.available_time} min used."
        )

        # Display scheduled tasks sorted by time via Scheduler.sort_by_time()
        sorted_sched = scheduler.sort_by_time()
        # Keep only tasks that are in the built schedule
        sched_ids = set(id(t) for t in schedule)
        sorted_sched = [t for t in sorted_sched if id(t) in sched_ids]

        pet_of_sched: dict = {}
        for p in owner.pets:
            for t in p.get_tasks():
                pet_of_sched[id(t)] = p.name

        sched_rows = [
            {
                "Time": fmt_time(t.time),
                "Pet": pet_of_sched.get(id(t), "—"),
                "Task": t.description,
                "Priority": PRIORITY_EMOJI.get(t.priority, t.priority),
                "Duration (min)": t.duration,
                "Frequency": t.frequency,
            }
            for t in sorted_sched
        ]
        st.table(sched_rows)

        # Unscheduled tasks (pending but didn't fit)
        all_pending = scheduler.get_pending_tasks()
        unscheduled = [t for t in all_pending if id(t) not in sched_ids]
        if unscheduled:
            st.warning(
                f"⚠️ {len(unscheduled)} task(s) couldn't fit in today's schedule "
                f"due to time constraints:"
            )
            for t in unscheduled:
                st.markdown(f"- **{t.description}** ({t.duration} min, {t.frequency})")

        # Hard conflicts in the built schedule
        conflicts = scheduler.get_conflicts()
        if conflicts:
            st.markdown("**Conflicts in Schedule**")
            for msg in conflicts:
                st.error(f"🚨 {msg}")

    else:
        # No tasks fit at all — that's a meaningful problem, use error
        total_pending = scheduler.get_total_scheduled_time()
        if total_pending == 0:
            st.warning("⚠️ No pending tasks found. Add tasks to your pets first.")
        else:
            st.error(
                f"🚨 No tasks could be scheduled — the shortest pending task exceeds "
                f"your available time ({owner.available_time} min). "
                f"Increase available time or shorten task durations."
            )
