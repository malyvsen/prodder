from dataclasses import dataclass
from treys import Deck, Evaluator
from collections import defaultdict
from typing import Dict, List


@dataclass(frozen=True)
class RandomVariable:
    cdf: Dict[int, float]

    @classmethod
    def score(cls, board: List[int], precision: int) -> "RandomVariable":
        """The score for a player's hand given the cards on the board"""
        evaluator = Evaluator()
        scores = sorted(
            evaluator.evaluate(cards=possible_hand(board), board=board)
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


def possible_hand(board: List[int]):
    while True:
        deck = Deck()
        cards = deck.draw(2)
        if all(card not in board for card in cards):
            return cards
