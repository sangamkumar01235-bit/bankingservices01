import streamlit as st


# ==========================
# OOP Classes
# ==========================
class BankAccount:
    def __init__(self, account_holder, initial_balance):
        self.account_holder = account_holder
        self._balance = 0.0
        self.balance = initial_balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self._balance = float(amount)
        else:
            raise ValueError("Error! Balance cannot be negative.")

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"Deposited ₹{amount:,.2f}. New Balance: ₹{self._balance:,.2f}"
        else:
            raise ValueError("Error: Deposit amount must be positive!")

    def cash_withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Error: Withdrawal amount must be positive!")
        elif amount > self._balance:
            raise ValueError("Error: Not enough money!")
        else:
            self._balance -= amount
            return f"Withdrew ₹{amount:,.2f}. New Balance: ₹{self._balance:,.2f}"


class SavingAccount(BankAccount):
    def __init__(self, account_holder, initial_balance, interest_rate):
        super().__init__(account_holder, initial_balance)
        self.interest_rate = interest_rate  # in %

    def add_interest(self):
        interest = self._balance * (self.interest_rate / 100.0)
        self._balance += interest
        return f"Added ₹{interest:,.2f} interest ({self.interest_rate}%). New Balance: ₹{self._balance:,.2f}"


# ==========================
# Streamlit UI
# ==========================
st.set_page_config(page_title="Savings Account App", page_icon="🏦", layout="centered")

st.title("🏦 Bank & Savings Account System")

# Initialize default account in session state
if "account" not in st.session_state:
    st.session_state.account = SavingAccount(
        account_holder="Aman", initial_balance=100.0, interest_rate=7.0
    )
    st.session_state.history = ["Account opened for Aman with initial balance: ₹100.00"]

acc = st.session_state.account

# Account Overview Card
st.subheader("Account Details")
col1, col2, col3 = st.columns(3)
col1.metric("Account Holder", acc.account_holder)
col2.metric("Current Balance", f"₹{acc.balance:,.2f}")
col3.metric("Interest Rate", f"{acc.interest_rate}%")

st.divider()

# Banking Actions
st.subheader("Perform Actions")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📥 Deposit", "💸 Withdraw", "📈 Add Interest", "⚙️ Balance Setter (Validation)"]
)

# 1. Deposit
with tab1:
    deposit_amount = st.number_input(
        "Enter amount to deposit", min_value=0.0, step=10.0, key="dep_input"
    )
    if st.button("Confirm Deposit"):
        try:
            msg = acc.deposit(deposit_amount)
            st.session_state.history.append(msg)
            st.success(msg)
            st.rerun()
        except ValueError as err:
            st.error(str(err))

# 2. Withdraw
with tab2:
    withdraw_amount = st.number_input(
        "Enter amount to withdraw", min_value=0.0, step=10.0, key="with_input"
    )
    if st.button("Confirm Withdrawal"):
        try:
            msg = acc.cash_withdraw(withdraw_amount)
            st.session_state.history.append(msg)
            st.success(msg)
            st.rerun()
        except ValueError as err:
            st.error(str(err))

# 3. Add Interest
with tab3:
    st.write(f"Click below to apply **{acc.interest_rate}%** interest to current balance.")
    if st.button("Apply Interest"):
        try:
            msg = acc.add_interest()
            st.session_state.history.append(msg)
            st.success(msg)
            st.rerun()
        except ValueError as err:
            st.error(str(err))

# 4. Property Setter Validation Test
with tab4:
    st.caption("Directly test the `@balance.setter` logic (e.g. testing negative values).")
    direct_bal = st.number_input(
        "Set Balance Value directly", value=acc.balance, step=10.0, key="set_input"
    )
    if st.button("Set Balance Directly"):
        try:
            acc.balance = direct_bal
            msg = f"Balance directly set to ₹{acc.balance:,.2f}"
            st.session_state.history.append(msg)
            st.success(msg)
            st.rerun()
        except ValueError as err:
            st.error(str(err))

st.divider()

# Reset / New Account Section
with st.expander("Create / Reset Account"):
    with st.form("reset_form"):
        new_holder = st.text_input("Name", value="Aman")
        new_balance = st.number_input("Initial Balance", min_value=0.0, value=100.0, step=10.0)
        new_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=7.0, step=0.5)
        if st.form_submit_button("Reset / Create Account"):
            st.session_state.account = SavingAccount(new_holder, new_balance, new_rate)
            st.session_state.history = [
                f"Account created for {new_holder} with ₹{new_balance:,.2f}"
            ]
            st.rerun()

# Transaction History Log
st.subheader("Activity Log")
for record in reversed(st.session_state.history):
    st.write(f"- {record}")