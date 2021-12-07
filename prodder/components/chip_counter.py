import streamlit as st


def chip_counter(
    count_label: str,
    change_label: str,
    change_button_label: str,
    change_callback,
    keys: str,
) -> int:
    """A generic chip counter with a change button"""

    def sync_count():
        st.session_state[keys["count"]] = st.session_state[keys["count_widget"]]

    def sync_change():
        st.session_state[keys["change"]] = st.session_state[keys["change_widget"]]

    def change_chips():
        change_callback()
        st.session_state[keys["change"]] = 0

    count_column, change_column = st.columns(2)
    with count_column:
        st.number_input(
            count_label,
            value=st.session_state[keys["count"]],
            on_change=sync_count,
            key=keys["count_widget"],
        )
    with change_column:
        st.number_input(
            change_label,
            value=st.session_state[keys["change"]],
            on_change=sync_change,
            key=keys["change_widget"],
        )
        st.button(change_button_label, on_click=change_chips)

    return st.session_state[keys["count"]]


def streamlit_keys(master_key: str):
    keys = dict(
        count=f"chips_{master_key}",
        count_widget=f"{master_key}_widget",
        change=f"chips_{master_key}_change",
        change_widget=f"{master_key}_change_widget",
    )
    for handle, key in keys.items():
        if "widget" not in handle:
            if key not in st.session_state:
                st.session_state[key] = 0
            st.session_state[key] = int(st.session_state[key])
    return keys
