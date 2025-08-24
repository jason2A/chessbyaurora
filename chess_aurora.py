import streamlit as st
import chess
import time
import random

st.set_page_config(
    page_title="💎 Glass Chess",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main, .stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
    background-size: 400% 400%; min-height: 100vh; padding: 0;
}
.chess-board-container {display:flex;justify-content:center;margin:2.5rem 0;}
.chess-square-button {
    border-radius: 12px !important;
    border: 2px solid #409cff !important;
    font-family: 'SF Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    background: #132a47 !important;
    min-height:70px; min-width:70px; color:white;
}
.chess-square-button.selected {background:#409cff !important;}
.chess-square-button.move {background:#533483 !important;}
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "selected_square" not in st.session_state:
        st.session_state.selected_square = None
    if "valid_moves" not in st.session_state:
        st.session_state.valid_moves = []
    if "move_history" not in st.session_state:
        st.session_state.move_history = []

def display_board(board):
    selected_square = st.session_state.selected_square
    valid_moves = st.session_state.valid_moves
    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)
    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = rank*8 + file
            piece = board.piece_at(square)
            piece_symbols = {'k':'♔','q':'♕','r':'♖','b':'♗','n':'♘','p':'♙','K':'♚','Q':'♛','R':'♜','B':'♝','N':'♞','P':'♟'}
            piece_symbol = piece_symbols.get(piece.symbol(),"") if piece else ""
            is_selected = square == selected_square
            is_valid = any(move.to_square == square for move in valid_moves)
            btn_class = "chess-square-button"
            if is_selected: btn_class += " selected"
            elif is_valid: btn_class += " move"
            if cols[file].button(piece_symbol or " ", key=f"{rank}_{file}", help=f"Square {chr(97+file)}{rank+1}"):
                handle_square_click(square)
    st.markdown('</div>', unsafe_allow_html=True)

def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        st.session_state.selected_square = square
        st.session_state.valid_moves = [move for move in st.session_state.board.legal_moves if move.from_square == square]
    else:
        st.session_state.selected_square = None
        st.session_state.valid_moves = []

def handle_square_click(square):
    if st.session_state.selected_square is not None:
        from_square = st.session_state.selected_square
        to_square = square
        move = chess.Move(from_square, to_square)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(str(move))
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.rerun()
        else:
            select_square(square)
    else:
        select_square(square)

def main():
    init_chess_game()
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    display_board(st.session_state.board)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("New Game"):
        st.session_state.board = chess.Board()
        st.session_state.selected_square = None
        st.session_state.valid_moves = []
        st.session_state.move_history = []

if __name__ == "__main__":
    main()
