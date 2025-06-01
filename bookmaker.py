"""

Booklet Writer

Book creator using automatic engine analysis

Developed and tested using python 3.13 and python-chess 1.11.2 on windows 11 OS.

"""

import os, sys
import time
import chess
import chess.engine
import chess.pgn
import argparse
import datetime


APP_NAME = 'BookMaker'
APP_VER = 'v0.1.0'
APP_NAME_VER = APP_NAME + ' ' + APP_VER
APP_DESC = 'Generates pgn lines using an engine useful for\
            book creation. It uses depth-first search algorithm\
            to build the pgn lines.'
CHESS_STD_START_POS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class genbook():
    def __init__(self, g):
        self.eng = g['engine']
        self.hash = g['hash']  # in mb
        self.threads = g['threads']
        self.book_side = g['bookside']  # white or black
        self.wmultipv = g['wmultipv']
        self.bmultipv = g['bmultipv']
        self.movetime = g['movetime']  # in ms
        self.mrs = g['mrs']  # mrs = minimum relative score
        self.depth = g['depth']  # book depth
        self.outfn = g['output']  # output pgn filename
        self.move_penalty = g['movepenalty']  # Move penalty for book side
        self.pv = []
        self.book_line = 0
        self.analyzer = None
        self.pgnfile = g['pgnfile']

    def get_end_fen(self, pgnfn):
        pgn = open(pgnfn)
        game = chess.pgn.read_game(pgn)
        game_node = game
        end_node = game_node.end()
        end_board = end_node.board()

        return end_board.fen()


if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description=APP_DESC, epilog=APP_NAME_VER)
    parser.add_argument("-e", "--engine", help="input engine name",
                        required=True)
    parser.add_argument("--inpgn", help="input pgn file", required=True)
    parser.add_argument("-m", "--hash", help="engine hash usage in MB, "
                                             "default=64MB", default=64, type=int)
    parser.add_argument("-t", "--threads", help="engine threads to use, "
                                                "default=1", default=1, type=int)
    parser.add_argument("-d", "--depth", help="maximum depth of a book line, "
                        "default=4", default=4, type=int)
    parser.add_argument("-a", "--movetime", help="analysis time per position "
                        "in ms, in multipv=n where n > 1, the analysis time "
                        "will be extended to n times this movetime, default=1000",
                        default=1000, type=int)
    parser.add_argument("-f", "--wmultipv", help="number of pv for white, "
                        "default=1", default=1, type=int)
    parser.add_argument("-g", "--bmultipv",
                        help="number of pv for black, default=1",
                        default=1, type=int)
    parser.add_argument("-b", "--bookside",
                        help="white=book for white, black=book for black, "
                             "default=black", default='black')
    parser.add_argument("-r", "--relminscore", help="minimum relative score "
                        "that a given move will be extended if this is high "
                        "then less book lines will be generated, default=-0.3",
                        default=-0.3, type=float)
    parser.add_argument("-j", "--movepenalty", help="move penalty for the "
                                                    "book side, default=-0.1",
                        default=-0.1, type=float)

    args = parser.parse_args()
    
    ply = 0
    
    outfn = 'w_out.pgn' if args.bookside == 'white' else 'b_out.pgn'
        
    data = {'engine':args.engine,
            'hash':args.hash,
            'threads':args.threads,
            'movetime':args.movetime,
            'bookside':args.bookside,
            'wmultipv':args.wmultipv,
            'bmultipv':args.bmultipv,
            'depth':args.depth,
            'mrs':args.relminscore,
            'movepenalty':args.movepenalty,
            'pgnfile':args.inpgn,
            'output':outfn
            }
    
    print(':: Settings ::')
    print('Book for                   : %s' % args.bookside)
    print('Move penalty for book side : %0.2f' % args.movepenalty)
    print('Minimum relative score     : %0.2f' % args.relminscore)
    print('Max ply                    : %d' % args.depth)
    print('Movetime (ms)              : %d' % args.movetime)
    print('Hash (mb)                  : %d' % args.hash)
    print('Threads                    : %d\n' % args.threads)
    
    a = genbook(data)
    end_fen = a.get_end_fen(args.inpgn)
    test = end_fen
##    a.search(end_fen, args.depth, ply)

