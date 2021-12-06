import streamlit as st
from prodder import RandomVariable
from prodder.components import card_selector
from prodder.contains_duplicates import contains_duplicates


def main():
    st.title("Prodder")
    precision = st.slider(
        "Precision",
        min_value=256,
        max_value=4096,
        help="Number of possible hands to randomly consider",
    )
    with st.expander("Hand", expanded=True):
        hand = [card_selector("hand 1"), card_selector("hand 2")]
    with st.expander("Board", expanded=True):
        num_cards_on_board = st.selectbox(
            "Number of cards on board", options=[0, 3, 4, 5]
        )
        board = [card_selector(f"board {idx}") for idx in range(num_cards_on_board)]
    if contains_duplicates(hand + board):
        st.error("Duplicated cards")
        return
    RandomVariable.score(board=board, precision=precision)


main()
