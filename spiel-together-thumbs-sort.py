#!/usr/bin/env python

import argparse
import sys
import re
from collections import namedtuple
from operator import attrgetter

parser = argparse.ArgumentParser(description='tool che ordina per numero di like la lista di giochi http://www.tabletoptogether.com/essen-spiel')
parser.add_argument('sourceFile', metavar='spiel-together-file')
parser.add_argument('-o', metavar='nome del file di output')
args = parser.parse_args()

Game = namedtuple('Game', 'name like')
thumbs_list = []
out_list = []
game_rule = re.compile('^.*<strong>(.*?)<.*BGG Thumbs:\s*(\d+)<br')
with open(args.sourceFile, 'r', encoding = 'UTF8', errors = 'ignore') as source:
    all_games = source.readlines()
   
for line in all_games:
    game_string = game_rule.match(line)
    if game_string:
        game_name = game_string.group(1)
        game_thumbs = game_string.group(2)
        thumbs_list.append(Game(game_name.strip(' '), int(game_thumbs)))
        
for game in sorted(thumbs_list, reverse=True, key=attrgetter('like')):
    out_list.append('{} - {}'.format(game.name, game.like))

out_string = '\n'.join(out_list)


if args.o:
    with open(args.o, 'w') as out:
        out.write(out_string)
else:
    print(out_string)
