import streamlit as st
from prodder.components import card_selector, pot_counter, own_chip_counter
from prodder import BetStatistics, contains_duplicates


def main():
    st.title("Prodder")

    with st.sidebar:
        num_opponents = st.slider("Number of opponents", min_value=1, max_value=5)
        precision = st.slider(
            "Precision",
            min_value=256,
            max_value=4096,
            help="Number of possible hands to randomly consider",
        )

    verdict = st.empty()

    with st.expander("Chips", expanded=True):
        num_pot_chips = pot_counter()
        num_own_chips = own_chip_counter()
    with st.expander("Hand", expanded=True):
        hand = [card_selector("hand 1"), card_selector("hand 2")]
    with st.expander("Board", expanded=True):
        num_cards_on_board = st.selectbox(
            "Number of cards on board", options=[0, 3, 4, 5]
        )
        board = [card_selector(f"board {idx}") for idx in range(num_cards_on_board)]
    if contains_duplicates(hand + board):
        verdict.error("Duplicated cards")
        return

    bet_statistics = BetStatistics.from_game_state(
        own_chips=num_own_chips,
        pot_chips=num_pot_chips,
        hand=hand,
        board=board,
        num_opponents=num_opponents,
        precision=precision,
    )
    with verdict.container():
        st.write(
            f"The probability of winning is {bet_statistics.win_probability * 100:.0f}%."
        )
        if bet_statistics.should_bet:
            st.write(
                f"The optimal bet is {bet_statistics.optimal_bet}, but anything up to {bet_statistics.max_bet} will improve your situation on average."
            )
        else:
            st.write("You shouldn't bet anything.")


main()
