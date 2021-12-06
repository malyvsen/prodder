import streamlit as st
from treys import Card


def card_selector(key: str):
    columns = st.columns(2)
    rank = columns[0].selectbox(
        "Rank", options=list(Card.STR_RANKS), key=f"rank of {key}"
    )
    suit = columns[1].selectbox(
        "Suit", options=Card.CHAR_SUIT_TO_INT_SUIT.keys(), key=f"suit of {key}"
    )
    return Card.new(rank + suit)
