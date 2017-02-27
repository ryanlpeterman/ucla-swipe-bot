# UCLA Swipe Swap Bot
Messenger bot to replace Swipe Swap and help easily match buyers to sellers in the market

## Problem:
Currently in order to buy or sell a swipe at UCLA, one must inefficiently scroll through the
UCLA SwipeSwap Facebook page and scan through to find someone that fits your criteria. Once
a match is found one must personally message the person to facilitate the trade or see if its still
offered.

## Solution:
A messenger bot that prompts users for information about the swipes they are buying/selling. Once a
match is found the two parties will be connected.

This bot solution will be as good as SwipeSwap at least since the bot will scrape the SwipeSwap page for
listings. These will be parsed and the data for each post will be stored in the database using a probabilistic model.
If the confidence in figuring out what post's data is too low, we can manually ask them to confirm the data.


## File Descriptions:
```
├── app.py (main event code)
├── messenger_interface.py (messenger api functions bundled)
├── Procfile (for Heroku app setup)
├── readme.md
├── requirements.txt (for Heroku app setup)
├── test.py (all unit tests)
├── test.sh (helper script to add messenger API token to env variables)
└── util.py (various utility functions)
```

## Important Commands:
To run locally:

```python app.py```

To test:

``` ./test.sh ```

To deploy:

``` git push heroku master ```

## TODO (high level):
1. Database - after preliminary research python's TinyDB should do the trick and not add any dependencies
2. Matching Algorithm - I envisioned a tree/bucket type of matching which can match each new buyer/seller in O(1)
3. Recommendations - If market has no buyers, message people who have previously bought at these prices
4. Metrics/Data Analytics - tracking avg buy/sell price, best times to buy/sell