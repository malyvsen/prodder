from dataclasses import dataclass
from treys import Deck, Evaluator
from collections import defaultdict
from typing import Dict, List

from .contains_duplicates import contains_duplicates


@dataclass(frozen=True)
class RandomVariable:
    cdf: Dict[int, float]

    @classmethod
    def score(
        cls, known_hand: List[int], known_board: List[int], precision: int
    ) -> "RandomVariable":
        """The score for a player's hand given the cards on the board"""
        evaluator = Evaluator()
        scores = sorted(
            evaluator.evaluate(
                **random_situation(known_hand=known_hand, known_board=known_board)
            )
            for _ in range(precision)
        )
        cdf = {}
        for num_scores_seen, score in enumerate(scores):
            cdf[score] = (num_scores_seen + 1) / precision
        return cls(cdf=cdf)

    def maximum(self, num_trials: int) -> "RandomVariable":
        """The maximum of num_trials independent evaluations of this variable"""
        return type(self)(
            cdf={
                value: probability ** num_trials
                for value, probability in self.cdf.items()
            }
        )

    def __neg__(self) -> "RandomVariable":
        return type(self)(
            cdf={-value: 1 - probability for value, probability in self.cdf.items()}
        )

    def __add__(self, other) -> "RandomVariable":
        cdf = defaultdict(int)
        for value, probability in self.cdf.items():
            for other_value, other_probability in other.cdf.items():
                cdf[value + other_value] += probability * other_probability
        return type(self)(cdf=dict(cdf))

    def __sub__(self, other) -> "RandomVariable":
        return self + (-other)


def random_situation(known_hand: List[int], known_board: List[int]):
    deck = Deck()
    draw = (
        lambda num_cards: [deck.draw(num_cards)]
        if num_cards == 1
        else deck.draw(num_cards)
    )
    while True:
        hand = known_hand + draw(2 - len(known_hand))
        full_board = known_board + draw(5 - len(known_board))
        if not contains_duplicates(hand + full_board):
            return dict(cards=hand, board=full_board)
