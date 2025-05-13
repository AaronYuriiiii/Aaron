import streamlit as st
import threading
import time

# Persistent state
if 'items' not in st.session_state:
    st.session_state.items = []

def reminder(item, delay):
    time.sleep(delay)
    st.warning(f"⏰ Reminder! Don't forget your item: {item}")

# Title
st.title("🧾 Item Manager with Reminders")

# View items
st.subheader("Your Items")
if st.session_state.items:
    for i, item in enumerate(st.session_state.items, start=1):
        st.write(f"{i}. {item}")
else:
    with st.form("add_form"):
        new_item = st.text_input("Enter item to add:")
        submitted = st.form_submit_button("Add Item")
        if submitted and new_item.strip():
            st.session_state.items.append(new_item.strip())
            st.success("Item added!")

# Remove item
if st.session_state.items:
    with st.form("remove_form"):
        remove_index = st.number_input(
            "Enter item number to remove:", min_value=1,
            max_value=len(st.session_state.items), step=1
        )
        remove_submit = st.form_submit_button("Remove Item")
        if remove_submit:
            removed_item = st.session_state.items.pop(remove_index - 1)
            st.success(f"Removed item: {removed_item}")

# Add item with reminder
st.subheader("Add Item With Reminder")
with st.form("reminder_form"):
    reminder_item = st.text_input("Item name:")
    time_value = st.number_input("Remind me after (number):", min_value=1)
    unit = st.selectbox("Time unit:", ["Seconds", "Minutes", "Hours"])
    submit_reminder = st.form_submit_button("Add with Reminder")

    if submit_reminder and reminder_item.strip():
        # Convert to seconds
        multiplier = {"Seconds": 1, "Minutes": 60, "Hours": 3600}
        delay = time_value * multiplier[unit]

        st.session_state.items.append(reminder_item.strip())
        st.success(f"Item added with reminder. You’ll be reminded in {int(delay)} seconds.")

        # Run reminder in background
        t = threading.Thread(target=reminder, args=(reminder_item, delay))
        t.start()
