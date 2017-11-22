'''
Created on 14.11.2017

@author: tpfeiffer
'''

import trueskill
from trueskill import Rating

# Parameter über Admin-Interface verstellbar? Ranglisten-Reset bei Parameter-Änderung notwendig?
# Spielpaarungen und Ergebnisse mitloggen, damit hinterher Parameter appliziert werden können.
# Wird für Anzeige der letzten Spiele eh gebraucht
env = trueskill.TrueSkill(mu=30.0, sigma=10.0, beta=5.0, tau=0.1, draw_probability=0.0) # Es gibt kein Unentschieden

if 'mpmath' in trueskill.backends.available_backends():
    # mpmath can be used in the current environment
    env.backend = 'mpmath'
    
print(env)
    
# Ratings der einzelnen Spieler laden (mu und sigma können auch explizit übergeben werden)
p1 = env.create_rating(mu=27.0, sigma=7.2) # 1P's skill, create_rating verwendet die als default die Werte die im environment festgelegt werden
p2 = Rating(mu=37.9, sigma=2.1)  # 2P's skill
p3 = env.Rating()  # 3P's skill
p4 = Rating()  # Rating verwendet die globalen default Werte (siehe make_as_global)

# Beispiel:
# p1 = load_player_from_database('Arpad Emrick Elo')
# p2 = load_player_from_database('Mark Glickman')
# p3 = load_player_from_database('Heungsub Lee')

print(p1)
print(p2)
print(p3)
print(p4)

# Teams zuweisen
Team1 = [p1, p2]  # Team A contains just 1P
Team2 = [p3, p4]  # Team B contains 2P and 3P

print('{:.1%} chance to draw'.format(env.quality([Team1, Team2])))
if env.quality([Team1, Team2]) < 0.30:
    print('This match seems to be not so fair')

# spielen

# sieger eingeben

# neue Bewertungen anhand des Ergebnisses berechnen
(p1, p2), (p3, p4) = env.rate([Team1, Team2], ranks=[1, 0]) # Team1 wins (rank lower)

# Neue Wertung ausgeben und speichern
print(p1)
print(p2)
print(p3)
print(p4)