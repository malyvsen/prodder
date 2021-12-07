import streamlit as st

from .chip_counter import chip_counter, streamlit_keys


def own_chip_counter() -> int:
    pot_keys = streamlit_keys("pot")
    own_keys = streamlit_keys("own")

    def bet():
        st.session_state[pot_keys["count"]] += st.session_state[own_keys["change"]]
        st.session_state[own_keys["count"]] -= st.session_state[own_keys["change"]]

    return chip_counter(
        count_label="Your chips",
        change_label="Your bet",
        change_button_label="Make the bet",
        change_callback=bet,
        keys=own_keys,
    )
