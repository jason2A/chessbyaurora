import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import time
import random
import os
import json

# Page configuration
st.set_page_config(
    page_title="💎 Glass Chess",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');

    /* Global animations */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
        min-height: 100vh;
        padding: 0;
    }

    @keyframes glassGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
    }

    .glass-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        animation: containerFloat 6s ease-in-out infinite;
    }

    @keyframes containerFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .glass-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(64, 156, 255, 0.05) 50%, transparent 70%);
        animation: glassShimmer 4s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes glassShimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }

    .glass-title {
        text-align: center;
        color: #ffffff;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow:
            0 0 20px rgba(64, 156, 255, 0.5),
            0 0 40px rgba(255, 215, 0, 0.3);
        animation: glassTitle 4s ease-in-out infinite alternate;
        letter-spacing: -0.02em;
        position: relative;
    }

    .glass-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #409cff, #ffd700, #ff453a);
        animation: titleUnderline 3s ease-in-out infinite;
    }

    @keyframes titleUnderline {
        0%, 100% { width: 0; opacity: 0; }
        50% { width: 200px; opacity: 1; }
    }

    @keyframes glassTitle {
        0% {
            text-shadow: 0 0 20px rgba(64, 156, 255, 0.5), 0 0 40px rgba(255, 215, 0, 0.3);
            transform: scale(1) rotateY(0deg);
        }
        100% {
            text-shadow: 0 0 30px rgba(255, 69, 58, 0.6), 0 0 50px rgba(255, 215, 0, 0.4);
            transform: scale(1.02) rotateY(2deg);
        }
    }

    .glass-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.01em;
        animation: subtitleGlow 5s ease-in-out infinite;
    }

    @keyframes subtitleGlow {
        0%, 100% { opacity: 0.8; transform: translateY(0); }
        50% { opacity: 1; transform: translateY(-2px); }
    }

    .chess-board-container {
        display: flex;
        justify-content: center;
        margin: 2.5rem 0;
        position: relative;
        animation: boardContainerPulse 8s ease-in-out infinite;
    }

    @keyframes boardContainerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.01); }
    }

    .chess-board-container img {
        border-radius: 24px;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: boardGlow 6s ease-in-out infinite;
    }

    @keyframes boardGlow {
        0%, 100% {
            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        50% {
            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1),
                0 0 30px rgba(64, 156, 255, 0.2);
        }
    }

    .chess-board-container img:hover {
        transform: scale(1.02) translateY(-4px) rotateY(2deg);
        box-shadow:
            0 30px 80px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 40px rgba(255, 215, 0, 0.3);
    }
    /* Add other styles you want to keep here... */
    /* Chess square button style, tutor hints, etc. per original */

    .chess-square-button {
        border-radius: 12px !important;
        border: 3px solid rgba(64, 156, 255, 0.3) !important;
        font-family: 'SF Mono', 'Monaco', 'Menlo', monospace !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow:
            0 4px 16px rgba(64, 156, 255, 0.2),
            0 0 0 1px rgba(64, 156, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        min-height: 70px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
        background: linear-gradient(135deg,
            rgba(64, 156, 255, 0.1),
            rgba(100, 200, 255, 0.15),
            rgba(64, 156, 255, 0.1)) !important;
    }

    /* Tutor mode and hint styles */
    .tutor-mode-active {
        background: linear-gradient(135deg,
            rgba(255, 215, 0, 0.15),
            rgba(255, 193, 7, 0.2),
            rgba(255, 215, 0, 0.15)) !important;
        border-color: rgba(255, 215, 0, 0.5) !important;
        box-shadow:
            0 4px 16px rgba(255, 215, 0, 0.3),
            0 0 0 2px rgba(255, 215, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    .tutor-hint {
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255, 215, 0, 0.9);
        color: #000;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
        z-index: 1000;
        animation: hintFloat 2s ease-in-out infinite;
    }

    @keyframes hintFloat {
        0%, 100% { transform: translateX(-50%) translateY(0px); }
        50% { transform: translateX(-50%) translateY(-3px); }
    }

</style>
""", unsafe_allow_html=True)


def init_chess_game():
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'selected_piece' not in st.session_state:
        st.session_state.selected_piece = None
    if 'promotion_piece' not in st.session_state:
        st.session_state.promotion_piece = chess.QUEEN
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = "single"
    if 'room_code' not in st.session_state:
        st.session_state.room_code = None
    if 'player_name' not in st.session_state:
        st.session_state.player_name = None
    if 'waiting_for_opponent' not in st.session_state:
        st.session_state.waiting_for_opponent = False
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'last_click_time' not in st.session_state:
        st.session_state.last_click_time = 0
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True
    if 'tutor_hints' not in st.session_state:
        st.session_state.tutor_hints = {}
    if 'last_move_quality' not in st.session_state:
        st.session_state.last_move_quality = None
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "intermediate"
    if 'ai_thinking_time' not in st.session_state:
        st.session_state.ai_thinking_time = 2
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'move_quality_threshold' not in st.session_state:
        st.session_state.move_quality_threshold = 0.7


def get_player_color():
    if st.session_state.room_code:
        return "white" if st.session_state.waiting_for_opponent else "black"
    return "white"


def is_player_turn():
    if st.session_state.game_mode == "single":
        return True
    player_color = get_player_color()
    board_turn = "white" if st.session_state.board.turn else "black"
    return player_color == board_turn


def generate_room_code():
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def create_multiplayer_game():
    room_code = generate_room_code()
    st.session_state.room_code = room_code
    st.session_state.game_mode = "multiplayer"
    st.session_state.waiting_for_opponent = True
    st.session_state.board = chess.Board()
    st.session_state.move_history = []
    save_game_state()
    return room_code


def join_multiplayer_game(room_code):
    if room_code and len(room_code) == 6:
        st.session_state.room_code = room_code.upper()
        st.session_state.game_mode = "multiplayer"
        st.session_state.waiting_for_opponent = False
        load_game_state()
        return True
    return False


def save_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            game_state = {
                'fen': st.session_state.board.fen(),
                'move_history': st.session_state.move_history,
                'last_updated': time.time()
            }
            filename = f"game_{st.session_state.room_code}.json"
            with open(filename, 'w') as f:
                json.dump(game_state, f)
            return True
        except:
            return False
    return False


def load_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            filename = f"game_{st.session_state.room_code}.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    game_state = json.load(f)
                st.session_state.board = chess.Board(game_state['fen'])
                st.session_state.move_history = game_state['move_history']
                return True
        except:
            pass
    return False


def make_move(move_uci):
    try:
        move = chess.Move.from_uci(move_uci)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_uci)
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            if st.session_state.game_mode == "multiplayer":
                save_game_state()
            return True
        else:
            st.error("💎 Invalid move! Try again!")
            return False
    except ValueError:
        st.error("💎 Invalid move format! Use UCI notation (e.g., 'e2e4')")
        return False


def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        st.session_state.selected_square = square
        st.session_state.valid_moves = [move for move in st.session_state.board.legal_moves if move.from_square == square]
    else:
        st.session_state.selected_square = None
        st.session_state.valid_moves = []


def handle_square_click(square):
    if not (st.session_state.game_mode == "single" or is_player_turn()):
        return
    
    if st.session_state.selected_square is not None:
        from_square = st.session_state.selected_square
        to_square = square
        move = chess.Move(from_square, to_square)
        piece = st.session_state.board.piece_at(from_square)
        if move in st.session_state.board.legal_moves:
            if piece and piece.piece_type == chess.PAWN:
                # Auto-promote to queen if reaching last rank
                if (piece.color and to_square >= 56) or (not piece.color and to_square <= 7):
                    move = chess.Move(from_square, to_square, chess.QUEEN)
            if make_move(str(move)):
                st.experimental_rerun()
        else:
            select_square(square)
    else:
        select_square(square)


def get_game_status(board):
    if board.is_checkmate():
        return "checkmate", "💎 CHECKMATE! The game is over! 💎"
    elif board.is_stalemate():
        return "stalemate", "⚖️ STALEMATE! The game is a draw! ⚖️"
    elif board.is_insufficient_material():
        return "stalemate", "⚖️ Insufficient material! Draw! ⚖️"
    elif board.is_check():
        return "check", "⚡ CHECK! Your king is in danger! ⚡"
    else:
        return "normal", "💎 Game in progress 💎"


def evaluate_position(board):
    piece_values = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
    }

    white_material = 0
    black_material = 0

    pawn_table = [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    knight_table = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]

            if piece.piece_type == chess.PAWN:
                if piece.color:
                    value += pawn_table[square]
                else:
                    value += pawn_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.KNIGHT:
                if piece.color:
                    value += knight_table[square]
                else:
                    value += knight_table[chess.square_mirror(square)]

            if piece.color:
                white_material += value
            else:
                black_material += value

    white_mobility = len(list(board.legal_moves))
    board.turn = not board.turn
    black_mobility = len(list(board.legal_moves))
    board.turn = not board.turn

    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    center_control = 0
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            center_control += 10 if piece.color else -10

    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)

    white_king_safety = 0
    black_king_safety = 0

    if white_king_square is not None:
        white_king_safety = -10 * (chess.square_rank(white_king_square) + 1)
    if black_king_square is not None:
        black_king_safety = -10 * (8 - chess.square_rank(black_king_square))

    total_eval = (white_material - black_material) + \
                 (white_mobility - black_mobility) * 5 + \
                 center_control + \
                 (white_king_safety - black_king_safety)

    return total_eval


def get_best_moves(board, num_moves=3, difficulty="intermediate"):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return []

    move_evaluations = []
    for move in legal_moves:
        board.push(move)
        evaluation = evaluate_position(board)
        board.pop()
        move_evaluations.append((move, evaluation))

    if board.turn:
        move_evaluations.sort(key=lambda x: x[1], reverse=True)
    else:
        move_evaluations.sort(key=lambda x: x[1])

    if difficulty == "beginner":
        good_moves = move_evaluations[:len(move_evaluations)//2]
        random_moves = random.sample(move_evaluations, min(2, len(move_evaluations)))
        filtered_moves = good_moves + random_moves
        random.shuffle(filtered_moves)
    elif difficulty == "intermediate":
        cutoff = int(len(move_evaluations) * 0.7)
        filtered_moves = move_evaluations[:cutoff]
    elif difficulty == "advanced":
        cutoff = int(len(move_evaluations) * 0.5)
        filtered_moves = move_evaluations[:cutoff]
    elif difficulty == "expert":
        cutoff = int(len(move_evaluations) * 0.3)
        filtered_moves = move_evaluations[:cutoff]
    else:  # master
        cutoff = int(len(move_evaluations) * 0.2)
        filtered_moves = move_evaluations[:cutoff]

    return [(move, score) for move, score in filtered_moves[:num_moves]]


def get_ai_move(board, difficulty="intermediate"):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    if difficulty == "beginner":
        if random.random() < 0.7:
            return random.choice(legal_moves)
        else:
            best_moves = get_best_moves(board, 1, "beginner")
            return best_moves[0][0] if best_moves else random.choice(legal_moves)

    elif difficulty == "intermediate":
        best_moves = get_best_moves(board, 3, "intermediate")
        if random.random() < 0.5:
            return random.choice([m for m, _ in best_moves])
        else:
            return best_moves[0][0] if best_moves else random.choice(legal_moves)

    elif difficulty == "advanced":
        best_moves = get_best_moves(board, 2, "advanced")
        if random.random() < 0.3:
            return random.choice([m for m, _ in best_moves])
        else:
            return best_moves[0][0] if best_moves else random.choice(legal_moves)

    elif difficulty == "expert":
        best_moves = get_best_moves(board, 2, "expert")
        if random.random() < 0.1:
            return random.choice([m for m, _ in best_moves])
        else:
            return best_moves[0][0] if best_moves else random.choice(legal_moves)

    else:  # master
        best_moves = get_best_moves(board, 1, "master")
        return best_moves[0][0] if best_moves else random.choice(legal_moves)


def evaluate_move_quality(move, board):
    board.push(move)
    evaluation = evaluate_position(board)
    board.pop()

    max_eval = 1000
    normalized = max(-1, min(1, evaluation / max_eval))

    if board.turn:
        quality = (normalized + 1) / 2
    else:
        quality = (1 - normalized) / 2

    return quality


def get_tutor_hint(board, selected_square):
    if selected_square is None:
        return None

    piece = board.piece_at(selected_square)
    if not piece or piece.color != board.turn:
        return None

    legal_moves = [m for m in board.legal_moves if m.from_square == selected_square]
    if not legal_moves:
        return None

    move_qualities = []
    for move in legal_moves:
        quality = evaluate_move_quality(move, board)
        move_qualities.append((move, quality))

    move_qualities.sort(key=lambda x: x[1], reverse=True)
    best_move, best_quality = move_qualities[0]

    if best_quality > 0.8:
        hint = f"Excellent move! {chess.square_name(best_move.from_square)} to {chess.square_name(best_move.to_square)}"
    elif best_quality > 0.6:
        hint = f"Good move: {chess.square_name(best_move.from_square)} to {chess.square_name(best_move.to_square)}"
    elif best_quality > 0.4:
        hint = f"Decent move: {chess.square_name(best_move.from_square)} to {chess.square_name(best_move.to_square)}"
    else:
        hint = f"Consider: {chess.square_name(best_move.from_square)} to {chess.square_name(best_move.to_square)}"

    return hint, best_quality


def display_board(board):
    selected_square = st.session_state.get('selected_square', None)
    valid_moves = st.session_state.get('valid_moves', [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)

    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = rank * 8 + file
            piece = board.piece_at(square)

            piece_symbols = {
                'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
                'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
            }

            piece_symbol = piece_symbols.get(piece.symbol(), "") if piece else ""

            piece_class = ""
            if piece:
                pt = piece.symbol().lower()
                piece_class_map = {
                    'k': "piece-king",
                    'q': "piece-queen",
                    'r': "piece-rook",
                    'b': "piece-bishop",
                    'n': "piece-knight",
                    'p': "piece-pawn"
                }
                piece_class = piece_class_map.get(pt, "")

            tutor_hint = ""
            if st.session_state.get('tutor_mode', False) and st.session_state.get('show_hints', True):
                hint_result = get_tutor_hint(board, selected_square)
                if hint_result and selected_square == square:
                    hint_text, _ = hint_result
                    tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'

            button_classes = ["chess-square-button"]
            if piece_class:
                button_classes.append(piece_class)
            if st.session_state.get('tutor_mode', False):
                button_classes.append("tutor-mode-active")

            bg_color = (
                'rgba(64, 156, 255, 0.8)' if square == selected_square else
                'rgba(40, 167, 69, 0.8)' if any(move.to_square == square for move in valid_moves) else
                'rgba(248, 249, 250, 0.9)' if (rank + file) % 2 == 0 else
                'rgba(108, 117, 125, 0.9)'
            )

            color = (
                'white' if square == selected_square or
                any(move.to_square == square for move in valid_moves) or (rank + file) % 2 != 0 else
                'black'
            )

            with cols[file]:
                st.markdown(f"""
                    <div style="position: relative;">
                        <button
                            class="{' '.join(button_classes)}"
                            onclick="handleChessClick({square})"
                            style="background: {bg_color}; color: {color}; width: 100%; height: 70px;
                            border: 3px solid rgba(64, 156, 255, 0.3); border-radius: 12px;
                            font-family: 'SF Mono', 'Monaco', 'Menlo', monospace; font-weight: 700;
                            font-size: 2.5rem; cursor: pointer; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                            display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;"
                            title="Square {chr(97 + file)}{rank + 1}"
                        >{piece_symbol}</button>
                        {tutor_hint}
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    function handleChessClick(square) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        const existing = document.getElementById('chess-click-input');
        if (existing) existing.remove();
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def export_pgn(board, move_history):
    try:
        game_board = chess.Board()
        pgn_moves = []
        for move_uci in move_history:
            move = chess.Move.from_uci(move_uci)
            pgn_moves.append(game_board.san(move))
            game_board.push(move)

        pgn = f"""[Event "Glass Chess Game"]
[Site "Streamlit App"]
[Date "{time.strftime('%Y.%m.%d')}"]
[Round "1"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]

{' '.join(pgn_moves)} *"""
        return pgn
    except:
        return "PGN export failed"


def main():
    init_chess_game()
    if 'chess_square_click' in st.query_params:
        try:
            clicked_square = int(st.query_params['chess_square_click'][0])
            handle_square_click(clicked_square)
            # Clear the query param to prevent repeated handling
            st.experimental_set_query_params()
        except:
            pass

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        status_class = f"status-{status}"
        st.markdown(f'<div class="status-message {status_class}">{message}</div>', unsafe_allow_html=True)

    if st.session_state.game_mode == "multiplayer":
        load_game_state()
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🌐 Multiplayer Game")

        if st.session_state.room_code:
            st.markdown(f"**Room Code:** `{st.session_state.room_code}`")
            st.markdown(f"**Your Color:** {get_player_color().title()}")

            if st.session_state.waiting_for_opponent:
                st.markdown("⏳ **Waiting for opponent to join...** Share the room code with your friend!")
            else:
                if is_player_turn():
                    st.markdown("✅ **Your turn!**")
                else:
                    st.markdown("⏳ **Opponent's turn**")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔙 Back to Single Player", key="back_to_single"):
                st.session_state.game_mode = "single"
                st.session_state.room_code = None
                st.session_state.waiting_for_opponent = False
                st.experimental_rerun()
        with col2:
            if st.button("🔄 Refresh Game", key="refresh_multiplayer"):
                st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🎮 Game Mode")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🌐 Create Multiplayer Game", key="create_multiplayer"):
                room_code = create_multiplayer_game()
                st.success(f"Multiplayer game created! Room code: {room_code}")
                st.experimental_rerun()
        with col2:
            room_input = st.text_input("Join Room Code:", key="join_room_input", placeholder="ABC123")
            if st.button("🎯 Join Game", key="join_multiplayer"):
                if join_multiplayer_game(room_input):
                    st.success("Joined multiplayer game!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid room code!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Difficulty & Tutor Settings
    st.markdown('<div class="glass-info">', unsafe_allow_html=True)
    st.markdown("### 🎯 Difficulty & Tutor Settings")

    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        difficulty = st.selectbox("🤖 AI Difficulty:", ["beginner", "intermediate", "advanced", "expert", "master"],
            index=["beginner", "intermediate", "advanced", "expert", "master"].index(st.session_state.difficulty_level),
            key="difficulty_select")
        if difficulty != st.session_state.difficulty_level:
            st.session_state.difficulty_level = difficulty
            st.experimental_rerun()

    with col2:
        tutor_mode = st.checkbox("🎓 Tutor Mode", value=st.session_state.tutor_mode, key="tutor_checkbox")
        if tutor_mode != st.session_state.tutor_mode:
            st.session_state.tutor_mode = tutor_mode
            st.experimental_rerun()

    with col3:
        show_hints = st.checkbox("💡 Show Hints", value=st.session_state.show_hints, key="hints_checkbox")
        if show_hints != st.session_state.show_hints:
            st.session_state.show_hints = show_hints
            st.experimental_rerun()

    with col4:
        thinking_time = st.slider("⏱️ AI Thinking Time (sec):", 1, 10, st.session_state.ai_thinking_time, key="thinking_slider")
        if thinking_time != st.session_state.ai_thinking_time:
            st.session_state.ai_thinking_time = thinking_time
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Game Controls
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        if st.button("💎 NEW GAME", key="new_game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.game_over = False
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()

    with col2:
        if st.button("↩️ UNDO", key="undo_move"):
            if len(st.session_state.move_history) > 0:
                st.session_state.board.pop()
                st.session_state.move_history.pop()
                st.session_state.selected_square = None
                st.session_state.valid_moves = []
                st.experimental_rerun()

    with col3:
        if st.button("🎲 RANDOM", key="random_move"):
            legal_moves = list(st.session_state.board.legal_moves)
            if legal_moves:
                random_move = str(random.choice(legal_moves))
                if make_move(random_move):
                    st.experimental_rerun()

    with col4:
        if st.button("📋 FEN", key="copy_fen"):
            st.code(st.session_state.board.fen())

    col5, col6, col7, col8 = st.columns([1,1,1,1])

    with col5:
        if st.button("📊 STATS", key="show_stats"):
            stats = get_game_statistics(st.session_state.board, st.session_state.move_history)
            st.session_state.show_stats = not st.session_state.get('show_stats', False)

    with col6:
        if st.button("📄 PGN", key="export_pgn"):
            pgn = export_pgn(st.session_state.board, st.session_state.move_history)
            st.code(pgn)

    with col7:
        if st.button("🔄 FLIP", key="flip_board"):
            st.session_state.flip_board = not st.session_state.get('flip_board', False)

    with col8:
        if st.button("💾 SAVE", key="save_game"):
            st.success("Game state saved!")

    st.markdown("""
    <div class="drag-instructions">
        🎯 <strong>How to Play:</strong> Click on a piece to select it, then click on a destination square to move!<br>
        💎 <strong>Selected pieces</strong> are highlighted in blue, <strong>valid moves</strong> in green.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.game_mode == "single":
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("🤖 AI MOVE", key="ai_move", help="Let the AI make a move"):
                legal_moves = list(st.session_state.board.legal_moves)
                if legal_moves:
                    ai_move = get_ai_move(st.session_state.board, st.session_state.difficulty_level)
                    if ai_move:
                        if make_move(str(ai_move)):
                            st.experimental_rerun()

        with col2:
            if st.button("🔄 Refresh", key="refresh_single"):
                st.experimental_rerun()
    else:
        if not is_player_turn():
            st.markdown("⏳ **Waiting for opponent's move...**")
            if st.button("🔄 Refresh Game", key="refresh_multiplayer_move"):
                st.experimental_rerun()

    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 💎 Game Info")
        st.markdown(f"**Turn:** {'⚪ White' if st.session_state.board.turn else '⚫ Black'}")
        st.markdown(f"**Moves Made:** {len(st.session_state.move_history)}")
        st.markdown(f"**Legal Moves:** {st.session_state.board.legal_moves.count()}")

        if st.session_state.game_mode == "multiplayer":
            st.markdown("**Game Mode:** 🌐 Multiplayer")
            st.markdown(f"**Your Color:** {get_player_color().title()}")
            if is_player_turn():
                st.markdown("**Status:** ✅ Your turn")
            else:
                st.markdown("**Status:** ⏳ Opponent's turn")
        else:
            st.markdown("**Game Mode:** 🎮 Single Player")

        best_moves = get_best_moves(st.session_state.board, 3, st.session_state.difficulty_level)
        if best_moves:
            st.markdown(f"**💎 Suggested Moves ({st.session_state.difficulty_level.title()}):**")
            for i, (move, evaluation) in enumerate(best_moves, 1):
                eval_text = f"{evaluation:+.0f}"
                st.markdown(f"  {i}. `{move}` ({eval_text})")
        st.markdown(f"**FEN:** `{st.session_state.board.fen()}`")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="move-history">', unsafe_allow_html=True)
        st.markdown("### 📜 Move History")
        if st.session_state.move_history:
            for i, move in enumerate(st.session_state.move_history, 1):
                st.markdown(f"**{i}.** `{move}`")
        else:
            st.markdown("No moves made yet. Start the game! 💎")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Analysis")
        analysis, status = analyze_position(st.session_state.board)
        st.markdown(f"**Position:** {analysis}")
        summary = generate_game_summary(st.session_state.move_history)
        st.markdown(f"**Summary:** {summary}")

        if 'move_input' in st.session_state and st.session_state.move_input:
            move_analysis, move_type = get_move_analysis(st.session_state.move_input, st.session_state.board)
            st.markdown(f"**Move Analysis:** {move_analysis}")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get('show_stats', False):
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 📊 Game Statistics")
        stats = get_game_statistics(st.session_state.board, st.session_state.move_history)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Piece Count:**")
            for color, pieces in stats['piece_counts'].items():
                st.markdown(f"**{color.title()}:** {', '.join([f'{piece}: {count}' for piece, count in pieces.items()])}")

        with col2:
            st.markdown(f"**Game Phase:** {stats['phase']}")
            st.markdown(f"**Center Control:** White: {stats['center_control']['white']}, Black: {stats['center_control']['black']}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
