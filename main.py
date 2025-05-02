import streamlit as st
import random

# Initialize game state
if 'month' not in st.session_state:
    st.session_state['month'] = 1
    st.session_state['balance'] = 500.00  # Starting balance
    st.session_state['savings'] = 0.00
    st.session_state['income'] = 200.00  # Initial monthly income
    st.session_state['expenses'] = {}

st.title("Northern BC Budgeting Game")

st.write(f"Month: {st.session_state['month']}")
st.write(f"Current Balance: ${st.session_state['balance']:.2f}")
st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
st.write(f"Income this month: ${st.session_state['income']:.2f}")

# Expense categories (you can expand these)
expense_categories = ["Food", "Entertainment", "Transportation", "Personal Care", "Other"]
st.session_state['expenses'].setdefault(st.session_state['month'], {cat: 0.00 for cat in expense_categories})

st.subheader("Monthly Expenses")
for category in expense_categories:
    st.session_state['expenses'][st.session_state['month']][category] = st.number_input(
        f"Amount spent on {category}",
        min_value=0.00,
        max_value=st.session_state['balance'] + st.session_state['income'] - sum(st.session_state['expenses'][st.session_state['month']].values()) - st.session_state['savings'],
        value=st.session_state['expenses'][st.session_state['month']][category],
        step=1.00
    )

st.subheader("Savings")
savings_this_month = st.number_input(
    "Amount to save this month",
    min_value=0.00,
    max_value=st.session_state['balance'] + st.session_state['income'] - sum(st.session_state['expenses'][st.session_state['month']].values()),
    value=0.00,
    step=1.00
)

if st.button("End Month"):
    total_spent_this_month = sum(st.session_state['expenses'][st.session_state['month']].values())
    remaining_balance = st.session_state['balance'] + st.session_state['income'] - total_spent_this_month - savings_this_month
    st.session_state['balance'] = remaining_balance
    st.session_state['savings'] += savings_this_month

    # Random event
    if random.random() < 0.5:  # Increased chance for testing
        event_type = random.choice(['positive', 'negative'])
        if event_type == 'positive':
            amount = random.randint(10, 60)
            st.session_state['balance'] += amount
            st.success(f"Good news! You received a surprise windfall of ${amount:.2f}!")
        else:
            amount = random.randint(15, 75)
            st.session_state['balance'] -= amount
            st.warning(f"Oh no! An unexpected expense of ${amount:.2f} occurred.")

    st.session_state['month'] += 1
    if st.session_state['month'] > 4:
        st.write("Game Over!")
        st.write(f"Final Balance: ${st.session_state['balance']:.2f}")
        st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
        st.session_state['month'] = 1 # Reset for a new game
        st.session_state['balance'] = 500.00
        st.session_state['savings'] = 0.00
        st.session_state['income'] = 200.00
        st.session_state['expenses'] = {}
        st.rerun()
    else:
        st.rerun()
