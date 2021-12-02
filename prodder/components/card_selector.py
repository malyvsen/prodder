import streamlit as st
from treys import Card


def card_selector(card_name):
    st.header(card_name)
    columns = st.columns(2)
    rank = columns[0].selectbox(
        "Rank", options=list(Card.STR_RANKS), key=f"rank of {card_name}"
    )
    suit = columns[1].selectbox(
        "Suit", options=Card.CHAR_SUIT_TO_INT_SUIT.keys(), key=f"suit of {card_name}"
    )
    return Card.new(rank + suit)
