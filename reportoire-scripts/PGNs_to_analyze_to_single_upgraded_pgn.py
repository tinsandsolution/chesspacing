import io
import chess.pgn
import sys
import pickle
from stockfish import Stockfish
import time

with open('to_analyze.pickle', 'rb') as handle:
    to_analyze, doing_black_reportoire = pickle.load(handle)

stockfish = Stockfish("/root/stockfishengine/stockfish_14_x64_avx2")

stockfish = Stockfish(parameters={"Threads":14,"Hash": 104537,"Write Debug Log": "true"})

print(stockfish.get_parameters())

print("setting depth")
stockfish.set_depth(39)

localtime = time.localtime()
result = time.strftime("%I:%M:%S %p", localtime)
print(str(result))

with open('somefile.tsv', 'a') as the_file:
    the_file.write(str(stockfish.get_parameters()))
    the_file.write(result)

to_consolidate = {}

for fen in to_analyze:
    stockfish.set_fen_position(fen)
    
    best_move_uci = stockfish.get_best_move()
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    
    to_print = fen + "\t" + \
               to_analyze[fen] + "\t" + \
               best_move_uci + "\t" + \
               result + "\n"
               
    to_consolidate[to_analyze[fen]] = str(best_move_uci)        
    print(to_print)
    with open('somefile.tsv', 'a') as the_file:
        the_file.write(to_print)

'''
the below code should take no more than a few minutes
'''
gamesPGN = []
for pgn, bestresponse in to_consolidate.items():
    game = chess.pgn.read_game(io.StringIO(pgn))
    game.end().add_variation(chess.Move.from_uci(bestresponse))
    gamesPGN.append(str(game[-1]))

# A significant amount of the below code comes from Aven Bross
# https://github.com/permutationlock/merge-pgn
# their code is under the MIT license
# Description: A simple tool to merge several pgn games into a single game with
# variations.

games = []
for pgn in gamesPGN:
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is not None:
        games.append(game)
        game = chess.pgn.read_game(io.StringIO(pgn))

master_node = chess.pgn.Game()
mlist = []
for game in games:
    mlist.extend(game.variations)

variations = [(master_node, mlist)]
done = False

while not done:
    newvars = []
    done = True
    for vnode, nodes in variations:
        newmoves = {}
        for node in nodes:
            if node.move is None:
                continue
            elif node.move not in list(newmoves):
                nvnode = vnode.add_variation(node.move)
                if len(node.variations) > 0:
                    done = False
                newvars.append((nvnode, node.variations))
                newmoves[node.move] = len(newvars) - 1
            else:
                nvnode, nlist = newvars[newmoves[node.move]]
                if len(node.variations) > 0:
                    done = False
                nlist.extend(node.variations)
                newvars[newmoves[node.move]] = (nvnode, nlist)
    variations = newvars

print(master_node)

if doing_black_reportoire == True:
    filename = "black_reportoire.pgn"
else: 
    filename = "white_reportoire.pgn"

with open(filename, "w") as f:
    f.write(str(master_node))