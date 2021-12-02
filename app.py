import streamlit as st
from prodder.components import card_selector


def main():
    st.title("Prodder")
    hand = [card_selector("First card on hand"), card_selector("Second card on hand")]


main()
