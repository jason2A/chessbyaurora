import streamlit as st
import chess
import chess.svg
import time
import random
import os
import json

# Page Config
st.set_page_config(
    page_title="💎 Glass Chess",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for glassy UI with animated pieces, inspired by iOS 26 style
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');

body, .stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
    background-size: 400% 400%;
    animation: glassGradient 12s ease infinite;
    color: white;
    font-family: 'SF Pro Display', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

@keyframes glassGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.glass-container {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(24px);
    border-radius: 28px;
    padding: 24px;
    margin: 24px auto;
    max-width: 900px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    animation: floatContainer 6s ease-in-out infinite;
}

@keyframes floatContainer {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-8px);}
}

.glass-title {
    font-weight: 700;
    font-size: 3rem;
    text-align: center;
    color: #8ab6ff;
    text-shadow: 0 0 10px #8ab6ff;
    margin-bottom: 8px;
    animation: titleGlow 4s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    0% { text-shadow: 0 0 10px #6fa6ff;}
    50% { text-shadow: 0 0 25px #94b9ff;}
    100% { text-shadow: 0 0 10px #6fa6ff;}
}

/* Chess Board */

.chess-board {
    display: grid;
    grid-template-columns: repeat(8, 60px);
    grid-template-rows: repeat(8, 60px);
    border-radius: 16px;
    overflow: hidden;
    margin: auto;
    box-shadow: 0 0 12px #4ba1ffaa;
}

.square {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 36px;
    font-weight: 700;
    user-select: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-family: 'SF Pro Display', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
    position: relative;
}

.square.light {
    background-color: rgba(255, 255, 255, 0.12);
}

.square.dark {
    background-color: rgba(0, 0, 0, 0.35);
}

.square.selected {
    background-color: #5599ffcc !important;
    box-shadow: 0 0 14px #5599ffcc;
}

.square.move {
    background-color: #2ecc7122 !important;
    box-shadow: 0 0 12px #2ecc7122;
}

.square:hover {
    background-color: #4a6fffdd !important;
    box-shadow: 0 0 10px #4a6fffdd;
}

.square > .piece {
    pointer-events: none;
    animation: pieceFloat 6s ease-in-out infinite alternate;
}

@keyframes pieceFloat {
    0% { transform: translateY(0) }
    50% { transform: translateY(-4px) }
    100% { transform: translateY(0) }
}

/* Piece animations */

.piece.king {
    color: #7bb4ff;
    animation: kingGlow 4s ease-in-out infinite alternate;
}

@keyframes kingGlow {
    0% { text-shadow: 0 0 6px #7bb4ff; }
    50% { text-shadow: 0 0 16px #a5c5ff; }
    100% { text-shadow: 0 0 6px #7bb4ff; }
}

.piece.queen {
    color: #a1baff;
    animation: queenGlow 3s ease-in-out infinite;
}

@keyframes queenGlow {
    0%,100% { opacity: 1; filter: drop-shadow(0 0 2px #a6c3ff);}
    50% { opacity: 0.85; filter: drop-shadow(0 0 8px #bbe0ff);}
}

.piece.rook {
    color: #8eaed9;
    animation: rookPulse 3s ease-in-out infinite alternate;
}

@keyframes rookPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

.piece.bishop {
    color: #7492c2;
    animation: bishopFloat 4s ease-in-out infinite alternate;
}

@keyframes bishopFloat {
    0% { transform: translateY(0);}
    50% { transform: translateY(-3px);}
    100% { transform: translateY(0);}
}

.piece.knight {
    color: #6a84bb;
    animation: knightBounce 2s ease-in-out infinite;
}

@keyframes knightBounce {
    0%, 100% { transform: translateY(0) rotate(0deg);}
    25% { transform: translateY(-2px) rotate(3deg);}
    75% { transform: translateY(-2px) rotate(-3deg);}
}

.piece.pawn {
    color: #5e79b0;
    animation: pawnWave 3s ease-in-out infinite;
}

@keyframes pawnWave {
    0%, 100% { transform: translateY(0);}
    50% { transform: translateY(-3px);}
}

.drag-instructions {
    background: rgba(255, 255, 255, 0.1);
    color: #9ec9ff;
    border-radius: 12px;
    text-align: center;
    margin: 20px;
    padding: 10px;
    font-size: 1.1rem;
}

.status-message {
    text-align: center;
    margin: 10px 0;
    font-weight: 600;
    font-size: 1.1rem;
    color: #accfff;
    text-shadow: 0 0 3px #5a98ff;
}


button:focus {
    outline: none;
}
</style>
""", unsafe_allow_html=True)


def init_game():
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'ai_thinking' not in st.session_state:
        st.session_state.ai_thinking = False
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "intermediate"


def is_player_turn():
    return True  # For now single player only


def get_piece_char(piece):
    unicode_pieces = {
        'P': '♙', 'N': '♘', 'B': '♗',
        'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝',
        'r': '♜', 'q': '♛', 'k': '♚',
    }
    return unicode_pieces.get(piece.symbol(), '')


def render_board():
    board = st.session_state.board
    selected = st.session_state.selected_square
    valid_moves = st.session_state.valid_moves

    columns = []
    for rank in range(7, -1, -1):
        row_cols = st.columns(8)
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            is_light = (file + rank) % 2 == 0
            classes = ["square"]
            classes.append("light" if is_light else "dark")

            if selected == square:
                classes.append("selected")
            elif any(move.to_square == square for move in valid_moves):
                classes.append("move")

            piece_char = get_piece_char(piece) if piece else ""

            piece_class = ''
            if piece:
                piece_type = piece.symbol().lower()
                if piece_type == 'k':
                    piece_class = 'king'
                elif piece_type == 'q':
                    piece_class = 'queen'
                elif piece_type == 'r':
                    piece_class = 'rook'
                elif piece_type == 'b':
                    piece_class = 'bishop'
                elif piece_type == 'n':
                    piece_class = 'knight'
                elif piece_type == 'p':
                    piece_class = 'pawn'

            button_label = f'<div class="piece {piece_class}">{piece_char}</div>'

            if row_cols[file].button(label="", key=f'sq_{file}_{rank}', help=chess.square_name(square)):
                handle_click(square)

            st.markdown(
                f"""
                <style>
                .stButton button[key="{f'sq_{file}_{rank}'}"] {{
                    all: unset;
                    cursor: pointer;
                    width:60px;
                    height:60px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border-radius: 12px;
                    border: none;
                }}
                </style>
                """, unsafe_allow_html=True)

            # We place div for decoration in markdown (not inside button, because can't nest)
            st.markdown(
                f"""
                <div class="{' '.join(classes)}" style="position:relative; width:60px; height:60px; margin-top:-64px; margin-left:-12px;">
                  {button_label}
                </div>
                """, unsafe_allow_html=True)


def handle_click(square):
    board = st.session_state.board
    selected = st.session_state.selected_square

    if selected is None:
        piece = board.piece_at(square)
        if piece and piece.color == board.turn:
            st.session_state.selected_square = square
            st.session_state.valid_moves = [move for move in board.legal_moves if move.from_square == square]
    else:
        move = chess.Move(selected, square)
        if move in board.legal_moves:
            board.push(move)
            st.session_state.move_history.append(move.uci())
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()
        else:
            # Deselect or select new square
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                st.session_state.selected_square = square
                st.session_state.valid_moves = [move for move in board.legal_moves if move.from_square == square]
            else:
                st.session_state.selected_square = None
                st.session_state.valid_moves = []


def main():
    init_game()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

    st.markdown('<div class="glass-title">💎 Glass Chess</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-subtitle">Where elegance meets strategy in crystal clarity</div>', unsafe_allow_html=True)

    render_board()

    board = st.session_state.board
    status, message = check_status(board)
    st.markdown(f'<div class="status-message">{message}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("New Game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history.clear()
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()
    with col2:
        if st.button("Undo"):
            if len(st.session_state.board.move_stack) > 0:
                st.session_state.board.pop()
                st.session_state.move_history.pop()
                st.session_state.selected_square = None
                st.experimental_rerun()
    with col3:
        if st.button("Random Move"):
            moves = list(st.session_state.board.legal_moves)
            if moves:
                move = random.choice(moves)
                st.session_state.board.push(move)
                st.session_state.move_history.append(move.uci())
                st.experimental_rerun()
    with col4:
        if st.button("Flip Board"):
            # Not implemented. Add flip logic if needed.
            pass

    st.markdown(
        """<div class="drag-instructions">Click on a piece, then on a square to move it.<br>Selected squares glow blue, valid moves highlight green.</div>""",
        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def check_status(board):
    if board.is_checkmate():
        return "checkmate", "💎 Checkmate! Game over."
    elif board.is_stalemate():
        return "stalemate", "⚖️ Stalemate! Draw!"
    elif board.is_insufficient_material():
        return "draw", "♻️ Draw due to insufficient material."
    elif board.is_check():
        return "check", "⚠️ Check! Protect your king."
    else:
        return "normal", "♟️ Game in progress"


if __name__ == "__main__":
    main()
