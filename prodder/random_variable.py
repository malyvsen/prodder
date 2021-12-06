from dataclasses import dataclass
from functools import reduce
from treys import Deck, Evaluator
from collections import Counter, defaultdict
from typing import Dict, List

from .contains_duplicates import contains_duplicates


@dataclass(frozen=True)
class RandomVariable:
    pmf: Dict[int, float]

    @classmethod
    def from_cdf(cls, cdf: Dict[int, float]) -> "RandomVariable":
        sorted_values = sorted(cdf.keys())
        return cls(
            pmf={
                value: cdf[value] - (cdf[prev_value] if prev_value is not None else 0)
                for prev_value, value in zip([None] + sorted_values, sorted_values)
            }
        )

    @classmethod
    def score(
        cls, known_hand: List[int], known_board: List[int], precision: int
    ) -> "RandomVariable":
        """The score for a player's hand given the cards on the board"""
        evaluator = Evaluator()
        scores = [
            evaluator.evaluate(
                **random_situation(known_hand=known_hand, known_board=known_board)
            )
            for _ in range(precision)
        ]
        return cls(
            pmf={
                value: num_occurences / precision
                for value, num_occurences in Counter(scores).items()
            }
        )

    @property
    def mean(self):
        return sum(value * probability for value, probability in self.pmf.items())

    def to_cdf(self) -> Dict[int, float]:
        sorted_values = sorted(self.pmf.keys())
        sorted_probabilities = [self.pmf[value] for value in sorted_values]
        cumulative_probabilities = reduce(
            lambda cumulative, current: cumulative + [cumulative[-1] + current],
            sorted_probabilities,
            [0],
        )[1:]
        return {
            value: probability
            for value, probability in zip(sorted_values, cumulative_probabilities)
        }

    def maximum(self, num_trials: int) -> "RandomVariable":
        """The maximum of num_trials independent evaluations of this variable"""
        return self.from_cdf(
            cdf={
                value: probability ** num_trials
                for value, probability in self.to_cdf().items()
            }
        )

    def minimum(self, num_trials: int) -> "RandomVariable":
        """The minimum of num_trials independent evaluations of this variable"""
        return -(-self).maximum(num_trials)

    def evaluate_cdf(self, value):
        """The probability of this random variable taking a value <= the given one"""
        return sum(probability for x, probability in self.pmf.items() if x <= value)

    def __neg__(self) -> "RandomVariable":
        return type(self)(
            pmf={-value: probability for value, probability in self.pmf.items()}
        )

    def __add__(self, other) -> "RandomVariable":
        pmf = defaultdict(float)
        for value, probability in self.pmf.items():
            for other_value, other_probability in other.pmf.items():
                pmf[value + other_value] += probability * other_probability
        return type(self)(pmf=dict(pmf))

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
