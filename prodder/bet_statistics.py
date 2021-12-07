from dataclasses import dataclass
import math
from typing import Dict, List

from .random_variable import RandomVariable


@dataclass(frozen=True)
class BetStatistics:
    win_probability: float
    bet_utilities: Dict[int, float]

    @classmethod
    def from_game_state(
        cls,
        own_chips: int,
        pot_chips: int,
        hand: List[int],
        board: List[int],
        num_opponents: int,
        precision: int,
    ):
        """Various statistics on the optimal bet"""
        own_score = RandomVariable.score(
            known_hand=hand, known_board=board, precision=precision
        )
        best_enemy_score = RandomVariable.score(
            known_hand=[], known_board=board, precision=precision
        ).minimum(num_opponents)
        advantage = best_enemy_score - own_score
        win_probability = 1 - advantage.evaluate_cdf(0)
        return cls(
            win_probability=win_probability,
            bet_utilities={
                bet: win_probability * cls.utility(own_chips + pot_chips + bet)
                + (1 - win_probability) * cls.utility(own_chips - bet)
                - cls.utility(own_chips)
                for bet in range(own_chips + 1)
            },
        )

    @property
    def should_bet(self) -> bool:
        return any(utility > 0 for utility in self.bet_utilities.values())

    @property
    def optimal_bet(self):
        return max(self.bet_utilities.keys(), key=lambda bet: self.bet_utilities[bet])

    @property
    def max_bet(self):
        return max(bet for bet, utility in self.bet_utilities.items() if utility > 0)

    @classmethod
    def utility(cls, num_chips):
        return math.log(1 + num_chips)
