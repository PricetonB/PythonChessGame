import requests
import chess
import chess.pgn

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()

    def send_move(self, move):
        move = chess.Move.from_uci(move.lower())
        if self.board.is_legal(move):
            self.board.push(move)
            return True
        print(f"Invalid move: {move}")
        return False

    def get_engine_move(self):
        # Send board FEN to Lichess API for a Stockfish move suggestion
        url = "https://lichess.org/api/cloud-eval"
        params = {
            'fen': self.board.fen(),  # Get the FEN of the current board position
            'multiPv': 1  # Request the top move from Stockfish
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            move_san = response.json()['pvs'][0]['moves'].split()[0]
            move = self.board.parse_san(move_san)
            self.board.push(move)
            moveString = move.uci()
            print(f"Engine move: {moveString}")
            return moveString.upper()
        else:
            raise Exception(f"Error getting move from engine: {response.status_code}")

