from functools import reduce
import streamlit as st


def chip_counter() -> int:
    variable_name = "num_chips"
    current_key = "num_chips_current"
    added_key = "num_chips_added"
    if variable_name not in st.session_state:
        st.session_state[variable_name] = 0

    current_column, new_column = st.columns(2)

    def set_chips():
        st.session_state[variable_name] = st.session_state[current_key]

    current_column.number_input(
        "Number of chips in the pot",
        value=st.session_state[variable_name],
        on_change=set_chips,
        key=current_key,
    )

    def add_chips():
        st.session_state[variable_name] += st.session_state[added_key]
        st.session_state[added_key] = 0

    with new_column:
        st.number_input("Number of chips being added", value=0, key=added_key)
        st.button("Add these", on_click=add_chips)

    return st.session_state[variable_name]
