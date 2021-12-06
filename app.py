import streamlit as st
from prodder import RandomVariable
from prodder.components import card_selector, chip_counter
from prodder.contains_duplicates import contains_duplicates


def main():
    st.title("Prodder")

    with st.sidebar:
        num_enemies = st.slider("Number of other players", min_value=1, max_value=5)
        precision = st.slider(
            "Precision",
            min_value=256,
            max_value=4096,
            help="Number of possible hands to randomly consider",
        )

    with st.expander("Pot", expanded=True):
        pot_amount = chip_counter()
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

    own_score = RandomVariable.score(
        known_hand=hand, known_board=board, precision=precision
    )
    best_enemy_score = RandomVariable.score(
        known_hand=[], known_board=board, precision=precision
    ).minimum(num_enemies)
    advantage = best_enemy_score - own_score
    win_probability = 1 - advantage.evaluate_cdf(0)
    st.write(f"The probability of winning is {win_probability * 100:.0f}%")


main()
