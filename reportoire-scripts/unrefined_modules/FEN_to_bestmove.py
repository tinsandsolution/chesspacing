from stockfish import Stockfish
import time

FENs = [
        'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/3B1N2/PPP2PPP/RNBQ1RK1 b kq - 3 5',
        'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/2PB1N2/PP3PPP/RNBQK2R b KQkq - 0 5',
        'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/3B1N2/PPPN1PPP/R1BQK2R b KQkq - 3 5',
        'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/3B1N1P/PPP2PP1/RNBQK2R b KQkq - 0 5',
        'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/2NB1N2/PPP2PPP/R1BQK2R b KQkq - 3 5',
        'rnbqk2r/ppp1ppbp/3p1np1/8/2PPP3/3B1N2/PP3PPP/RNBQK2R b KQkq - 0 5',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/6P1/PPP1PPBP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/2P5/6P1/PP1PPPBP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/8/5NP1/PPPPPPBP/RNBQK2R b KQkq - 3 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P3/6P1/PPPP1PBP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/8/3P2P1/PPP1PPBP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/5P2/6P1/PPPPP1BP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/8/P5P1/1PPPPPBP/RNBQK1NR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/5NP1/PPP1PP1P/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/2P2N2/PP2PPPP/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/4PN2/PPP2PPP/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/6B1/3P4/5N2/PPP1PPPP/RN1QKB1R b KQkq - 2 3',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/1P3N2/P1P1PPPP/RNBQKB1R b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3P4/5N2/PPPNPPPP/R1BQKB1R b KQkq - 2 3',
        'rnbqk1nr/ppp1ppbp/3p2p1/8/2BPP3/5N2/PPP2PPP/RNBQK2R b KQkq - 1 4',
        'rnbqk1nr/ppp1ppbp/3p2p1/1B6/3PP3/5N2/PPP2PPP/RNBQK2R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/2P1P3/5N2/PP1P1PPP/RNBQKB1R w KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P4/2P5/PP3PPP/RNBQKBNR b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P4/5N2/PPP2PPP/RNBQKB1R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P1P2/8/PPP3PP/RNBQKBNR b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P4/4B3/PPP2PPP/RN1QKBNR b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2P1P3/8/8/PPP2PPP/RNBQKBNR b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2pPP3/8/8/PPP2PPP/RNBQKBNR b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/2BP4/8/PPP2PPP/RNBQK1NR b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P4/2N5/PPP2PPP/R1BQKBNR b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/3P1B2/8/PPP2PPP/RN1QKBNR b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p1P3/2PP4/8/PP3PPP/RNBQKBNR b KQkq - 0 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/5Q2/PPPPNPPP/RNB1K2R b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/2P2Q2/PP1P1PPP/RNB1K1NR b KQkq - 0 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/5Q2/PPPPNPPP/RNB1K2R b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/5Q1N/PPPP1PPP/RNB1K2R b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2BPP3/5Q2/PPP2PPP/RNB1K1NR b KQkq - 0 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P2P/5Q2/PPPP1PP1/RNB1K1NR b KQkq - 0 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/4P3/5Q2/PPPPBPPP/RNB1K1NR b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/P4Q2/1PPP1PPP/RNB1K1NR b KQkq - 0 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/4P3/1B3Q2/PPPP1PPP/RNB1K1NR b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/1Q6/PPPP1PPP/RNB1K1NR b KQkq - 1 4',
        'rnbqk1nr/pppp1pbp/4p1p1/8/2B1P3/5Q1P/PPPP1PP1/RNB1K1NR b KQkq - 0 4',
        'rnbqk2r/1pp1ppbp/p2p1np1/8/P2PP3/2N2N1P/1PP2PP1/R1BQKB1R b KQkq - 0 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/8/2BPP3/2N2N1P/PPP2PP1/R1BQK2R b KQkq - 1 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/6B1/3PP3/2N2N1P/PPP2PP1/R2QKB1R b KQkq - 1 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/8/3PP3/2N2N1P/PPP1BPP1/R1BQK2R b KQkq - 1 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/8/3PP3/P1N2N1P/1PP2PP1/R1BQKB1R b KQkq - 0 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/8/3PPB2/2N2N1P/PPP2PP1/R2QKB1R b KQkq - 1 6',
        'rnbqk2r/1pp1ppbp/p2p1np1/4P3/3P4/2N2N1P/PPP2PP1/R1BQKB1R b KQkq - 0 6',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/3P1NP1/PPP2P1P/RNBQKB1R b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/2NP1N2/PPP2PPP/R1BQKB1R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/3P1N2/PPPN1PPP/R1BQKB1R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/2P1P3/3P1N2/PP3PPP/RNBQKB1R b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/3PBN2/PPP2PPP/RN1QKB1R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/3P1N1P/PPP2PP1/RNBQKB1R b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P2P/3P1N2/PPP2PP1/RNBQKB1R b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4P3/3P1N2/PPPB1PPP/RN1QKB1R b KQkq - 1 4',
        'rnbqk1nr/pp1pppbp/6p1/2p5/4PB2/3P1N2/PPP2PPP/RN1QKB1R b KQkq - 1 4',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/2BPP3/2N1BN2/PPP2PPP/R2QK2R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BN2/PPPQ1PPP/R3KB1R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BN1P/PPP2PP1/R2QKB1R b KQ - 0 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BN2/PPP1BPPP/R2QK2R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/4P3/3P4/2N1BN2/PPP2PPP/R2QKB1R b KQ - 0 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP2P/2N1BN2/PPP2PP1/R2QKB1R b KQ - 0 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2NQBN2/PPP2PPP/R3KB1R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BN2/PPP1QPPP/R3KB1R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BNP1/PPP2P1P/R2QKB1R b KQ - 0 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/2N1BN2/PPP2PPP/R1Q1KB1R b KQ - 5 6',
        'rnbq1rk1/ppp1ppbp/3p1np1/8/3PP3/P1N1BN2/1PP2PPP/R2QKB1R b KQ - 0 6',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/7P/PPPP1P2/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/2B1P1P1/8/PPPP1P1P/RNBQK1NR b KQkq - 2 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/3P4/PPP2P1P/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/2P5/PP1P1P1P/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/5P2/PPPP3P/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/5N2/PPPP1P1P/RNBQKB1R b KQkq - 2 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/2N5/PPPP1P1P/R1BQKBNR b KQkq - 2 3',
        'rnbqk1nr/ppppppbp/6p1/8/4PPP1/8/PPPP3P/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/6P1/4P3/8/PPPP1P1P/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1P1/8/PPPP1PBP/RNBQK1NR b KQkq - 2 3',
        'rnbqk1nr/ppppppbp/6p1/8/4P1PP/8/PPPP1P2/RNBQKBNR b KQkq - 0 3',
        'rnbqk1nr/ppppppbp/6p1/8/3PP1P1/8/PPP2P1P/RNBQKBNR b KQkq - 0 3'
]

stockfish = Stockfish("/root/stockfishengine/stockfish_14_x64_avx2")

stockfish = Stockfish(parameters={"Threads":14,"Hash": 65336,"Write Debug Log": "true"})

print(stockfish.get_parameters())

stockfish.set_depth(40)

localtime = time.localtime()
result = time.strftime("%I:%M:%S %p", localtime)
print(result)

for FEN in FENs:
    stockfish.set_fen_position(FEN)
    print(stockfish.get_best_move())
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)
