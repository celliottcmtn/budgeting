import streamlit as st
import random

# Define expense categories globally
expense_categories = ["Rent", "Food", "Entertainment", "Transportation", "Personal Care", "Cellphone/Internet", "Utilities", "Other"]

# Initialize game state
if 'month' not in st.session_state:
    st.session_state['month'] = 1
    st.session_state['balance'] = 0.00
    st.session_state['savings'] = 0.00
    st.session_state['monthly_income'] = 0.00
    st.session_state['available_this_month'] = 0.00
    st.session_state['expenses'] = {1: {cat: 0 for cat in expense_categories},
                                     2: {cat: 0 for cat in expense_categories},
                                     3: {cat: 0 for cat in expense_categories},
                                     4: {cat: 0 for cat in expense_categories}}

st.title("Northern BC Budgeting Game")

# Initial savings for the semester (only in the first month)
if st.session_state['month'] == 1:
    initial_savings = st.number_input("Savings for the semester:", min_value=0, step=50, value=0)
    initial_income = st.number_input("Enter your fixed monthly income:", min_value=50, step=50, value=950)
    st.session_state['monthly_income'] = float(initial_income)
    st.session_state['balance'] = float(initial_savings)
    st.session_state['available_this_month'] = st.session_state['balance'] + st.session_state['monthly_income']

else:
    st.session_state['available_this_month'] = st.session_state['balance'] + st.session_state['monthly_income']

st.write(f"Savings from last month: ${st.session_state['balance']:.2f}")
st.write(f"New income: ${st.session_state['monthly_income']:.2f}")
st.write(f"Total Available: ${st.session_state['available_this_month']:.2f}")
st.write(f"Month: {st.session_state['month']}")
st.write(f"Total Savings: ${st.session_state['savings']:.2f}")

st.subheader("Monthly Expenses")
current_month = st.session_state['month']
total_spent_this_month = sum(st.session_state['expenses'][current_month].values())
remaining_after_expenses = st.session_state['available_this_month'] - total_spent_this_month

expense_inputs = {}
for category in expense_categories:
    initial_value = st.session_state['expenses'][current_month].get(category, 0)
    max_val = 0
    if remaining_after_expenses is not None:
        try:
            max_val = int(remaining_after_expenses)
        except (ValueError, TypeError):
            max_val = 0

    expense_inputs[category] = st.number_input(
        f"Amount spent on {category}",
        min_value=0,
        max_value=max_val,
        value=int(initial_value),
        step=1,
        key=f"{category}_{current_month}",
        label_visibility="visible",
        key_format=None
    )

# Autogenerate savings based on what's left
savings_this_month = remaining_after_expenses - sum(expense_inputs.values())
st.subheader(f"Savings this month: ${savings_this_month:.2f}")

if st.button("End Month"):
    st.session_state['expenses'][current_month] = expense_inputs
    st.session_state['balance'] = savings_this_month # Remaining after expenses becomes next month's starting balance
    st.session_state['savings'] += savings_this_month
    st.session_state['month'] += 1

    # Random Events (50% chance)
    if random.random() < 0.5:
        event_type = random.choice(['positive', 'negative'])
        if event_type == 'positive':
            positive_events = [
                {"text": "You found $30 while helping a neighbour!", "amount": 30},
                {"text": "Your aunt sent you $50 for your birthday!", "amount": 50},
                {"text": "You sold some old snowboarding gear for $75!", "amount": 75},
                {"text": "You won a $25 gift card to the local movie theatre!", "amount": 25},
                {"text": "You got a bonus of $40 for shoveling snow for a neighbour!", "amount": 40},
            ]
            event = random.choice(positive_events)
            st.session_state['balance'] += event['amount']
            st.success(f"Good news! {event['text']} You gained ${event['amount']:.2f}!")
        else:
            negative_events = [
                {"text": "Your phone screen cracked - $70 to fix.", "amount": 70},
                {"text": "You needed a new bus pass this month ($55).", "amount": 55},
                {"text": "You forgot your reusable water bottle and had to buy drinks ($20).", "amount": 20},
                {"text": "A friend's birthday party came up - you spent $30 on a gift.", "amount": 30},
                {"text": "Your toque got lost, and you had to buy a new one ($25).", "amount": 25},
            ]
            event = random.choice(negative_events)
            st.session_state['balance'] -= event['amount']
            st.warning(f"Oh no! {event['text']} You lost ${event['amount']:.2f}.")

    if st.session_state['month'] > 4:
        st.write("Game Over!")
        st.write(f"Final Balance: ${st.session_state['balance']:.2f}")
        st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
        st.session_state['month'] = 1
        st.session_state['balance'] = 0.00
        st.session_state['savings'] = 0.00
        st.session_state['monthly_income'] = 0.00
        st.session_state['available_this_month'] = 0.00
        st.session_state['expenses'] = {}
        st.rerun()
    else:
        st.rerun()
