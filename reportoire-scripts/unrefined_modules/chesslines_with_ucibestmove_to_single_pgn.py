# A significant amount of this code comes from Aven Bross
# https://github.com/permutationlock/merge-pgn
# their code is under the MIT license, and as such this code is too.
# Description: A simple tool to merge several pgn games into a single game with
# variations.

# this has been edited to not need a bunch of files
# in theory this should be split up into two specific scripts:
# 1. a script that takes a pgn and a uci move and converts it into a single PGN
# 2. a script that takes a bunch of PGNs and turns them into a single PGN (with like, variants)

import chess.pgn
import io

thisdictionary = {
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Bb4' : 'a2a3',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Nf6' : 'd1c2',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 f5' : 'g2g3',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Bd6' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Nd7' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 dxc4' : 'd2c4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 a6' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Be7' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 g6' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 h6' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 Ne7' : 'e2e4',
    '1. Nf3 c6 2. d4 d5 3. c4 e6 4. Nbd2 b6' : 'e2e4',
    '1. Nf3 b6 2. d4 Bb7 3. e3 e6' : 'c2c4',
    '1. Nf3 b6 2. d4 Bb7 3. e3 g6' : 'f1d3',
    '1. Nf3 b6 2. d4 Bb7 3. e3 Nf6' : 'c2c4',
    '1. Nf3 b6 2. d4 Bb7 3. e3 d6' : 'f1d3',
    '1. Nf3 b6 2. d4 Bb7 3. e3 d5' : 'c2c4',
    '1. Nf3 b6 2. d4 Bb7 3. e3 f5' : 'f1e2',
    '1. Nf3 b6 2. d4 Bb7 3. e3 Bxf3' : 'd1f3',
    '1. Nf3 b6 2. d4 Bb7 3. e3 Nc6' : 'd4d5',
    '1. Nf3 b6 2. d4 Bb7 3. e3 h6' : 'f1d3',
    '1. Nf3 b6 2. d4 Bb7 3. e3 a6' : 'b1d2',
    '1. Nf3 b6 2. d4 Bb7 3. e3 c5' : 'd4d5',
    '1. Nf3 b6 2. d4 Bb7 3. e3 c6' : 'e3e4',
    '1. Nf3 f6 2. d4 d5 3. c4 c6' : 'b1c3',
    '1. Nf3 f6 2. d4 d5 3. c4 Bg4' : 'd1b3',
    '1. Nf3 f6 2. d4 d5 3. c4 Be6' : 'c4d5',
    '1. Nf3 f6 2. d4 d5 3. c4 e5' : 'd4e5',
    '1. Nf3 f6 2. d4 d5 3. c4 Nc6' : 'c4d5',
    '1. Nf3 f6 2. d4 d5 3. c4 Bf5' : 'c4d5',
    '1. Nf3 f6 2. d4 d5 3. c4 c5' : 'c4d5',
    '1. Nf3 f6 2. d4 d5 3. c4 g6' : 'c4d5',
    '1. Nf3 f6 2. d4 d5 3. c4 b6' : 'c4d5',
    '1. Nf3 c5 2. e4 g6' : 'd2d4',
    '1. Nf3 c5 2. e4 d5' : 'e4d5',
    '1. Nf3 c5 2. e4 b6' : 'd2d4',
    '1. Nf3 c5 2. e4 Qc7' : 'c2c3',
    '1. Nf3 c5 2. e4 e5' : 'f3e5',
    '1. Nf3 c5 2. e4 h6' : 'c2c4',
    '1. Nf3 c5 2. e4 Qb6' : 'd2d4',
    '1. Nf3 b6 2. d4 Bb7' : 'c2c4',
    '1. Nf3 b6 2. d4 a5' : 'e2e4',
    '1. Nf3 b6 2. d4 e6' : 'e2e4',
    '1. Nf3 b6 2. d4 Ba6' : 'e2e4',
    '1. Nf3 b6 2. d4 g6' : 'e2e4',
    '1. Nf3 b6 2. d4 Nf6' : 'g2g3',
    '1. Nf3 b6 2. d4 d5' : 'c2c4',
    '1. Nf3 b6 2. d4 c5' : 'd4d5',
    '1. Nf3 b6 2. d4 d6' : 'e2e4',
    '1. Nf3 b6 2. d4 c6' : 'e2e4',
    '1. Nf3 b6 2. d4 f5' : 'c1g5',
    '1. Nf3 b6 2. d4 Nc6' : 'd4d5',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Bb4' : 'c4d5',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 c6' : 'd1b3',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Nf6' : 'c4d5',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Nc6' : 'c1f4',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 a6' : 'd1b3',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 f6' : 'f3h4',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Nd7' : 'c4d5',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Be7' : 'c4d5',
    '1. Nf3 d5 2. d4 Bf5 3. c4 e6 4. Nc3 Bd6' : 'd1b3',
    '1. Nf3 d5 2. d4 c5 3. c4 cxd4' : 'c4d5',
    '1. Nf3 d5 2. d4 c5 3. c4 Nf6' : 'c4d5',
    '1. Nf3 d5 2. d4 c5 3. c4 Bf5' : 'c4d5',
    '1. Nf3 d5 2. d4 c5 3. c4 e5' : 'd4e5',
    '1. Nf3 d5 2. d4 c5 3. c4 Qa5' : 'c1d2',
    '1. Nf3 d5 2. d4 c5 3. c4 g6' : 'd4c5',
    '1. Nf3 d5 2. d4 c5 3. c4 b6 ' : 'c4d5',
    '1. Nf3 d5 2. d4 c5 3. c4 f6' : 'c4d5'
    }

gamesPGN = []
for pgn, bestresponse in thisdictionary.items():
    game = chess.pgn.read_game(io.StringIO(pgn))
    game.end().add_variation(chess.Move.from_uci(bestresponse))
    gamesPGN.append(str(game[-1]))

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