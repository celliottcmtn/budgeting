import streamlit as st
import random

# Define expense categories globally
expense_categories = ["Rent", "Food", "Entertainment", "Transportation", "Personal Care", "Other"]

# Initialize game state
if 'month' not in st.session_state:
    st.session_state['month'] = 1
    st.session_state['balance'] = 0.00
    st.session_state['savings'] = 0.00
    st.session_state['monthly_income'] = 0.00
    st.session_state['expenses'] = {1: {cat: 0 for cat in expense_categories},
                                     2: {cat: 0 for cat in expense_categories},
                                     3: {cat: 0 for cat in expense_categories},
                                     4: {cat: 0 for cat in expense_categories}}

st.title("Northern BC Budgeting Game")

# Set initial monthly income at the start of the game
if st.session_state['month'] == 1:
    initial_income = st.number_input("Enter your fixed monthly income:", min_value=50, step=50, value=950)
    st.session_state['monthly_income'] = float(initial_income)
    st.session_state['balance'] = float(initial_income)

st.write(f"Month: {st.session_state['month']}")
st.write(f"Current Balance: ${st.session_state['balance']:.2f}")
st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
st.write(f"Monthly Income: ${st.session_state['monthly_income']:.2f}")

st.subheader("Monthly Expenses")
current_month = st.session_state['month']
available_to_spend = st.session_state['balance'] - sum(st.session_state['expenses'][current_month].values())
if available_to_spend < 0:
    available_to_spend = 0

expense_inputs = {}
for category in expense_categories:
    initial_value = st.session_state['expenses'][current_month].get(category, 0)
    expense_inputs[category] = st.number_input(
        f"Amount spent on {category}",
        value=int(initial_value),
        key=f"{category}_{current_month}"
    )

st.subheader("Savings")
savings_this_month = st.number_input(
    "Amount to save this month",
    value=0,
    key=f"savings_{current_month}"
)

if st.button("End Month"):
    st.session_state['expenses'][current_month] = expense_inputs
    total_spent_this_month = sum(st.session_state['expenses'][current_month].values())
    remaining_balance = st.session_state['balance'] - total_spent_this_month - savings_this_month
    st.session_state['balance'] = float(remaining_balance + st.session_state['monthly_income'])
    st.session_state['savings'] += float(savings_this_month)
    st.session_state['month'] += 1

    if st.session_state['month'] > 4:
        st.write("Game Over!")
        pass
    else:
        st.rerun()
