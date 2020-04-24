from tournament import MatchMaking

men = [
    'ben',
    'ethan',
]

men_pref = [
    ('jack', 'sean'), # jack
    ('sean', 'jack') # sean
]

women_pref = [
    ('ethan', 'ben'),
    ('ben', 'ethan')
]

print(MatchMaking.stableMatching(2, men_pref, women_pref))