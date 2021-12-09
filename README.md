# Prodder

A poker bot powered by statistics.
Click [here](https://share.streamlit.io/malyvsen/prodder/main/app.py) to try it!

## How it works

Prodder tries a lot of possible draws to see what cards your opponents could have. It then checks in how many of these simulated cases you would be the winner, i.e. your hand would be the best of all hands. That gives your probability of winning.

Prodder then assumes that whatever bet you make will be matched by one opponent (not realistic, I know). For each possible amount you could bet, it calculates the expected utility of that bet - the average "goodness" of the situations that it could lead to. This "goodness" is calculated in a pretty arbitrary way, as `log(1 + num-chips)`. It makes _some_ sense because the number of chips you can win in the future is probably roughly proportional to the number of chips you have - read up on the [Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion) to learn more.

Prodder entirely ignores your opponent's bets - it only cares about how many chips there are on the table. If you like Bayesian statistics, you could see this as never updating the prior probability of winning. If you like poker, you could see this as assuming that your opponents didn't look at their cards. At least it's not fooled by bluffing ;)

## Disclaimer

This is probably not a good bot, it was just fun to make. DOn't actually use it to play with money or anything silly like that.
