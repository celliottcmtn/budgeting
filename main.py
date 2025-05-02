import streamlit as st
import random

# Initialize game state
if 'month' not in st.session_state:
    st.session_state['month'] = 1
    st.session_state['balance'] = 0  # Starting balance will be determined by initial income
    st.session_state['savings'] = 0
    st.session_state['income'] = 0
    st.session_state['expenses'] = {}

st.title("Northern BC Budgeting Game")

# Set initial monthly income at the start of the game
if st.session_state['month'] == 1:
    initial_income = st.number_input("Enter your initial monthly income:", min_value=50, step=50, value=300)
    st.session_state['income'] = float(initial_income)  # Ensure it's a float

st.write(f"Month: {st.session_state['month']}")
st.write(f"Current Balance: ${st.session_state['balance']:.2f}")
st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
st.write(f"Income this month: ${st.session_state['income']:.2f}")

# Expense categories with 'Rent' added
expense_categories = ["Rent", "Food", "Entertainment", "Transportation", "Personal Care", "Other"]
st.session_state['expenses'].setdefault(st.session_state['month'], {cat: 0 for cat in expense_categories})

st.subheader("Monthly Expenses")
available_to_spend = st.session_state['balance'] + st.session_state['income'] - sum(st.session_state['expenses'][st.session_state['month']].values()) - st.session_state['savings']
if available_to_spend < 0:
    available_to_spend = 0 # Prevent negative max values

for category in expense_categories:
    initial_expense_value = st.session_state['expenses'][st.session_state['month']][category]
    st.session_state['expenses'][st.session_state['month']][category] = st.number_input(
        f"Amount spent on {category}",
        min_value=0,
        max_value=int(available_to_spend),
        value=min(initial_expense_value, int(available_to_spend)), # Ensure value is not greater than max
        step=1
    )

st.subheader("Savings")
max_savings = int(st.session_state['balance'] + st.session_state['income'] - sum(st.session_state['expenses'][st.session_state['month']].values()))
savings_this_month = st.number_input(
    "Amount to save this month",
    min_value=0,
    max_value=max_savings,
    value=0,
    step=1 # No decimal places
)

if st.button("End Month"):
    total_spent_this_month = sum(st.session_state['expenses'][st.session_state['month']].values())
    remaining_balance = st.session_state['balance'] + st.session_state['income'] - total_spent_this_month - savings_this_month
    st.session_state['balance'] = float(remaining_balance) # Keep balance as float for potential future calculations
    st.session_state['savings'] += float(savings_this_month)

    # Refined Random Events (more context for Northern BC)
    if random.random() < 0.5:
        event_type = random.choice(['positive', 'negative'])
        if event_type == 'positive':
            positive_events = [
                {"text": "You found $30 while helping a neighbour!", "amount": 30},
                {"text": "Your aunt sent you $50 for your birthday!", "amount": 50},
                {"text": "You sold some old snowboarding gear for $75!", "amount": 75},
                {"text": "You won a $25 gift card to the local coffee shop!", "amount": 25},
                {"text": "You got a bonus of $40 for extra hours at work!", "amount": 40},
            ]
            event = random.choice(positive_events)
            st.session_state['balance'] += event['amount']
            st.success(f"Good news! {event['text']} You gained ${event['amount']:.2f}!")
        else:
            negative_events = [
                {"text": "Your ski boots broke and cost $60 to repair.", "amount": 60},
                {"text": "You got a flat tire on your bike - $45 for a new tube.", "amount": 45},
                {"text": "You forgot your lunch and had to buy a pricey sandwich ($15).", "amount": 15},
                {"text": "You chipped your phone screen - $80 to fix.", "amount": 80},
                {"text": "Unexpected cost for a school trip: $35.", "amount": 35},
            ]
            event = random.choice(negative_events)
            st.session_state['balance'] -= event['amount']
            st.warning(f"Oh no! {event['text']} You lost ${event['amount']:.2f}.")

    st.session_state['month'] += 1
    if st.session_state['month'] > 4:
        st.write("Game Over!")
        st.write(f"Final Balance: ${st.session_state['balance']:.2f}")
        st.write(f"Total Savings: ${st.session_state['savings']:.2f}")
        st.session_state['month'] = 1 # Reset for a new game
        st.session_state['balance'] = 0
        st.session_state['savings'] = 0
        st.session_state['income'] = 0
        st.session_state['expenses'] = {}
        st.rerun()
    else:
        st.rerun()
