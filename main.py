import streamlit as st
import random

# Initialize game state
if 'month' not in st.session_state:
    st.session_state['month'] = 1
    st.session_state['balance'] = 0.00
    st.session_state['savings'] = 0.00
    st.session_state['monthly_income'] = 0.00
    st.session_state['expenses'] = {}

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

# Expense categories with 'Rent' added
expense_categories = ["Rent", "Food", "Entertainment", "Transportation", "Personal Care", "Other"]
st.session_state['expenses'].setdefault(st.session_state['month'], {cat: 0 for cat in expense_categories})

st.subheader("Monthly Expenses")
available_to_spend = st.session_state['balance'] - sum(st.session_state['expenses'][st.session_state['month']].values())
if available_to_spend is None or available_to_spend < 0:
    max_val = 0
else:
    max_val = int(float(available_to_spend)) # Explicitly convert to float then int

for category in expense_categories:
    current_expense = st.session_state['expenses'][st.session_state['month']].get(category, 0)
    initial_value = min(current_expense, max_val)

    st.session_state['expenses'][st.session_state['month']][category] = st.number_input(
        f"Amount spent on {category}",
        min_value=0,
        max_value=max_val,
        value=initial_value,
        step=1,
        key=f"{category}_{st.session_state['month']}",
        label_visibility="visible",
        key_format=None
    )

st.subheader("Savings")
available_for_savings = st.session_state['balance'] - sum(st.session_state['expenses'][st.session_state['month']].values())
max_savings = int(float(available_for_savings)) if available_for_savings is not None and available_for_savings >= 0 else 0
savings_this_month = st.number_input(
    "Amount to save this month",
    min_value=0,
    max_value=max_savings,
    value=0,
    step=1,
    key=f"savings_{st.session_state['month']}",
    key_format=None
)

if st.button("End Month"):
    total_spent_this_month = sum(st.session_state['expenses'][st.session_state['month']].values())
    remaining_balance = st.session_state['balance'] - total_spent_this_month - savings_this_month
    st.session_state['balance'] = float(remaining_balance + st.session_state['monthly_income'])
    st.session_state['savings'] += float(savings_this_month)
    st.session_state['month'] += 1
    st.session_state['expenses'].setdefault(st.session_state['month'], {cat: 0 for cat in expense_categories})

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
        st.session_state['expenses'] = {}
        st.rerun()
    else:
        st.rerun()
