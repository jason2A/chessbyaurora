import streamlit as st
import chess
import json
import random
import time
import os

# Paste here your CSS from original with minor addition for piece smooth transitions:
st.markdown("""
<style>
.chess-square-button {
    transition: background-color 0.5s ease, color 0.5s ease, box-shadow 0.5s ease;
    /* your original styles */
}
.chess-square-button.move-animate {
    animation: pieceMoveGlow 1s ease forwards;
}
@keyframes pieceMoveGlow {
    0% { box-shadow: 0 0 5px rgba(64, 156, 255, 0.5); }
    100% { box-shadow: none; }
}

/* Keep your full original glassy blue, gold, red hues, add smooth hover effects */
</style>
""", unsafe_allow_html=True)

# Initialize state
def init_chess_game():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "selected_square" not in st.session_state:
        st.session_state.selected_square = None
    if "valid_moves" not in st.session_state:
        st.session_state.valid_moves = []
    if "move_history" not in st.session_state:
        st.session_state.move_history = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "last_move" not in st.session_state:
        st.session_state.last_move = None
    if "previous_board" not in st.session_state:
        st.session_state.previous_board = None

def display_board():
    board = st.session_state.board
    selected = st.session_state.selected_square
    valids = st.session_state.valid_moves

    cols = st.columns(8)
    for rank in range(7, -1, -1):
        for file in range(8):
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            piece_symbols = {'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
                             'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'}
            symbol = piece_symbols.get(piece.symbol(), '') if piece else ''

            bg = ("rgba(64, 156, 255, 0.6)" if sq == selected else
                  "rgba(40, 167, 69, 0.6)" if any(m.to_square == sq for m in valids) else
                  "#f8f9fa" if (rank+file) % 2 ==0 else "#6c757d")
            color = "white" if sq == selected or any(m.to_square == sq for m in valids) else ("black" if (rank+file)%2 ==0 else "white")

            class_names = "chess-square-button"
            # Animate last move squares
            if st.session_state.last_move:
                if sq == st.session_state.last_move.from_square or sq == st.session_state.last_move.to_square:
                    class_names += " move-animate"

            # Button style
            style=f'''
                background-color: {bg};
                color: {color};
                font-size: 2.8rem;
                border-radius: 12px;
                border: 2px solid rgba(64, 156, 255, 0.4);
                min-height: 70px;
                transition: all 0.3s ease;
                '''

            with cols[file]:
                if st.button(symbol, key=f"square_{sq}", help=f"{chess.square_name(sq)}", on_click=handle_click, args=(sq,), kwargs=None):
                    pass

def handle_click(sq):
    board = st.session_state.board
    if st.session_state.selected_square is None:
        # Select piece if player's color turn
        piece = board.piece_at(sq)
        if piece and piece.color == board.turn:
            st.session_state.selected_square = sq
            st.session_state.valid_moves = [m for m in board.legal_moves if m.from_square == sq]
    else:
        move = chess.Move(st.session_state.selected_square, sq)
        # Auto promote to queen
        piece = board.piece_at(st.session_state.selected_square)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color and sq >= 56) or (not piece.color and sq <= 7):
                move = chess.Move(st.session_state.selected_square, sq, promotion=chess.QUEEN)
        if move in board.legal_moves:
            board.push(move)
            st.session_state.move_history.append(move.uci())
            st.session_state.last_move = move
        st.session_state.selected_square = None
        st.session_state.valid_moves = []

def get_game_status(board):
    if board.is_checkmate():
        return "checkmate", "💎 CHECKMATE! The game is over! 💎"
    if board.is_stalemate():
        return "stalemate", "⚖️ STALEMATE! The game is a draw! ⚖️"
    if board.is_insufficient_material():
        return "draw", "⚖️ Insufficient material! Draw! ⚖️"
    if board.is_check():
        return "check", "⚡ CHECK! Your king is in danger! ⚡"
    return "normal", "💎 Game in progress 💎"

def main():
    init_chess_game()
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.title("💎 Glass Chess Velvet Multiplayer Enhanced")
    st.markdown('<p class="glass-subtitle">Elegant blue hues with glowing animations & multiplayer</p>', unsafe_allow_html=True)

    display_board()
    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        st.markdown(f'<div class="status-message status-{status}">{message}</div>', unsafe_allow_html=True)

    # Show last move
    if st.session_state.last_move:
        st.markdown(f"Last move: {st.session_state.last_move.uci()}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("New Game"):
            st.session_state.board.reset()
            st.session_state.move_history.clear()
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.session_state.last_move = None

    with col2:
        if len(st.session_state.move_history) > 0 and st.button("Undo Move"):
            st.session_state.board.pop()
            st.session_state.move_history.pop()
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.session_state.last_move = None

    with col3:
        if st.button("Show PGN"):
            pgn = " ".join(st.session_state.move_history)
            st.text_area("PGN Moves", value=pgn, height=150)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
