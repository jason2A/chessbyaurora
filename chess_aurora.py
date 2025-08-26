import streamlit as st
import chess
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

# CSS for glass theme and piece animations (shortened for brevity, use your full CSS)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;700&family=SF+Mono&display=swap');
* { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.glass-container {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(30px);
    border-radius: 32px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 3rem;
    margin: 2rem auto;
    max-width: 1400px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3),
                0 0 0 1px rgba(255,255,255,0.05),
                inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
    animation: containerFloat 6s ease-in-out infinite;
}
@keyframes containerFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
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
.chess-square-button {
    border-radius: 12px !important;
    border: 3px solid rgba(64,156,255,0.3) !important;
    font-family: 'SF Mono', 'Monaco', 'Menlo', monospace !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 16px rgba(64,156,255,0.2),0 0 0 1px rgba(64,156,255,0.1),inset 0 1px 0 rgba(255,255,255,0.2) !important;
    min-height: 70px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: relative !important;
    overflow: hidden !important;
    background: linear-gradient(135deg, rgba(64,156,255,0.1), rgba(100,200,255,0.15), rgba(64,156,255,0.1)) !important;
}
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = "single"
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "intermediate"
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'move_quality_threshold' not in st.session_state:
        st.session_state.move_quality_threshold = 0.7

def make_move(move_uci):
    try:
        move = chess.Move.from_uci(move_uci)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_uci)
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            return True
        else:
            st.error("💎 Invalid move! Try again!")
            return False
    except ValueError:
        st.error("💎 Invalid move format! Use UCI notation (e.g., 'e2e4', 'g1f3')")
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
        from_sq = st.session_state.selected_square
        to_sq = square
        move = chess.Move(from_sq, to_sq)
        piece = st.session_state.board.piece_at(from_sq)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color and to_sq >= 56) or (not piece.color and to_sq <= 7):
                move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
        if move in st.session_state.board.legal_moves:
            if make_move(move.uci()):
                st.experimental_rerun()
        else:
            select_square(square)
    else:
        select_square(square)

def is_player_turn():
    if st.session_state.game_mode == "single":
        return True
    # Multiplayer turn logic can be added here
    return True

def display_board(board):
    selected_square = st.session_state.get('selected_square', None)
    valid_moves = st.session_state.get('valid_moves', [])
    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)
    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            piece_symbols = {
                'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗',
                'n': '♘', 'p': '♙', 'K': '♚', 'Q': '♛',
                'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'
            }
            piece_symbol = piece_symbols.get(piece.symbol(), '') if piece else ''
            piece_class = ''
            if piece:
                pt = piece.symbol().lower()
                if pt == 'k': piece_class = "piece-king"
                elif pt == 'q': piece_class = "piece-queen"
                elif pt == 'r': piece_class = "piece-rook"
                elif pt == 'b': piece_class = "piece-bishop"
                elif pt == 'n': piece_class = "piece-knight"
                elif pt == 'p': piece_class = "piece-pawn"
            bg_color = 'rgba(64, 156, 255, 0.8)' if square == selected_square else \
                       'rgba(40, 167, 69, 0.8)' if any(move.to_square == square for move in valid_moves) else \
                       'rgba(248, 249, 250, 0.9)' if (rank + file) % 2 == 0 else 'rgba(108, 117, 125, 0.9)'
            text_color = 'white' if square==selected_square or any(move.to_square==square for move in valid_moves) or ((rank+file)%2!=0) else 'black'
            with cols[file]:
                button_html = f"""
                <div style="position: relative;">
                    <button class="chess-square-button {piece_class}" onclick="handleChessClick({square})"
                        style="background: {bg_color}; color: {text_color}; width: 100%; height: 70px; border-radius: 12px;
                               font-family: 'SF Mono', 'Monaco', 'Menlo', monospace; font-weight: 700; font-size: 2.5rem;
                               cursor: pointer; display: flex; align-items: center; justify-content: center;
                               position: relative; overflow: hidden;">
                        {piece_symbol}
                    </button>
                </div>
                """
                st.markdown(button_html, unsafe_allow_html=True)
    st.markdown("""
    <script>
    function handleChessClick(square) {
        const prev = document.getElementById('chess-click-input');
        if(prev) prev.remove();
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    init_chess_game()

    # Handle chess square click from HTML/JS if any
    if 'chess_square_click' in st.experimental_get_query_params():
        clicked_square = int(st.experimental_get_query_params()['chess_square_click'][0])
        handle_square_click(clicked_square)
        # Clear query param to prevent repeated clicks
        st.experimental_set_query_params()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        st.markdown(f'<div class="status-message status-{status}">{message}</div>', unsafe_allow_html=True)

    # Game controls simplified for demo
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💎 NEW GAME"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()
    with col2:
        if st.button("↩️ UNDO"):
            if len(st.session_state.board.move_stack) > 0:
                st.session_state.board.pop()
                if st.session_state.move_history:
                    st.session_state.move_history.pop()
                st.session_state.selected_square = None
                st.session_state.valid_moves = []
                st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()
