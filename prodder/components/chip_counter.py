from functools import reduce
import streamlit as st


def chip_counter() -> int:
    pot_state_key = "num_chips_pot"
    pot_widget_key = "pot_widget"
    if pot_state_key not in st.session_state:
        st.session_state[pot_state_key] = 0
    added_state_key = "num_chips_added"
    added_widget_key = "added_widget"
    if added_state_key not in st.session_state:
        st.session_state[added_state_key] = 0

    pot_column, added_column = st.columns(2)

    def set_pot():
        st.session_state[pot_state_key] = st.session_state[pot_widget_key]

    def set_added():
        st.session_state[added_state_key] = st.session_state[added_widget_key]

    def add_to_pot():
        st.session_state[pot_state_key] += st.session_state[added_state_key]
        st.session_state[added_state_key] = 0

    with pot_column:
        st.number_input(
            "Chips in the pot",
            value=st.session_state[pot_state_key],
            on_change=set_pot,
            key=pot_widget_key,
        )
    with added_column:
        st.number_input(
            "Chips an opponent is betting",
            value=st.session_state[added_state_key],
            on_change=set_added,
            key=added_widget_key,
        )
        st.button("Add these to the pot", on_click=add_to_pot)

    return st.session_state[pot_state_key]
