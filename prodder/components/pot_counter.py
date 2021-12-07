import streamlit as st

from .chip_counter import chip_counter, streamlit_keys


def pot_counter() -> int:
    keys = streamlit_keys("pot")

    def add_chips():
        st.session_state[keys["count"]] += st.session_state[keys["change"]]

    return chip_counter(
        count_label="Chips in the pot",
        change_label="Chips being bet by an opponent",
        change_button_label="Add these to the pot",
        change_callback=add_chips,
        keys=keys,
    )
