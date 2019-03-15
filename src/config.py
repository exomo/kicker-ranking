"""
Configuration file kicker ranking system. Import the config wherever the global database (db) or rfid reader (rfidReader)
need to be accessed.
"""

import trueskill
from trueskill import Rating

from database import database
from hardware import rfid

# Parameters for the trueskill ranking

#: Default initial mean of ratings.
MU = 30.
#: Default initial standard deviation of ratings.
SIGMA = MU / 3
#: Default distance that guarantees about 76% chance of winning.
BETA = SIGMA / 2
#: Default dynamic factor.
TAU = SIGMA / 100
#: Default draw probability of the game.
DRAW_PROBABILITY = .0
#: A basis to check reliability of the result.
DELTA = 0.0001

if 'mpmath' in trueskill.backends.available_backends():
    # mpmath can be used in the current environment
    backend = 'mpmath'
else:
    backend = None
trueskill.setup(mu=MU, sigma=SIGMA, beta=BETA, tau=TAU, draw_probability=DRAW_PROBABILITY, backend=backend) # Es gibt kein Unentschieden

# global setup of database and rfid reader
kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)
db.show_players()

rfidReader = rfid.rfid()