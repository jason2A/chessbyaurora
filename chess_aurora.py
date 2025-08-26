import streamlit as st
import chess
import chess.svg
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

# Glassy luxurious bubble + animations CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;700&family=SF+Mono&display=swap');

body, .stApp {
    margin: 0; padding: 0;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f3460, #533483);
    background-size: 400% 400%;
    animation: glassGradient 12s ease infinite;
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    color: white;
}
@keyframes glassGradient {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

.glass-container {
    background: rgba(255 255 255 / 0.12);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border-radius: 48px;
    border: 1.5px solid rgba(64 156 255 / 0.3);
    box-shadow:
        0 12px 36px rgba(64 156 255 / 0.35),
        inset 0 0 12px rgba(255 255 255 / 0.2);
    max-width: 750px;
    margin: 3rem auto 2rem auto;
    padding: 2rem;
    animation: floatBubble 8s ease-in-out infinite;
    user-select: none;
}

@keyframes floatBubble {
  0%,100% {transform: translateY(0) scale(1);}
  50% {transform: translateY(-15px) scale(1.02);}
}

.glass-title {
    text-align: center;
    font-weight: 700;
    font-size: 3.8rem;
    margin-bottom: 0.75rem;
    color: #58abff;
    text-shadow:
      0 0 10px #3388ff,
      0 0 25px #5ab0ff;
    letter-spacing: -.02em;
    animation: titleGlow 4s ease-in-out infinite alternate;
}
@keyframes titleGlow {
    0% {text-shadow: 0 0 10px #3388ff;}
    100% {text-shadow: 0 0 20px #5ab0ff;}
}
.glass-subtitle {
    font-weight: 400;
    text-align: center;
    font-size: 1.3rem;
    margin-bottom: 2.5rem;
    color: #acd4ffcc;
    text-shadow: 0 0 5px #3388ffcc;
    animation: subtitlePulse 5s ease-in-out infinite;
}
@keyframes subtitlePulse {
    0%,100% {opacity:.85; transform: translateY(0);}
    50% {opacity:1; transform: translateY(-2px);}
}

.chess-bubble {
    border-radius: 42px;
    box-shadow:
      0 0 40px rgba(64 156 255 / 0.7),
      inset 0 0 40px rgba(255 255 255 / 0.25);
    overflow: hidden;
    padding: 1.25rem;
    background: radial-gradient(circle at center, rgba(64 156 255 / 0.12), transparent);
    transition: box-shadow 0.4s ease;
    user-select: none;
}
.chess-bubble:hover {
    box-shadow:
      0 0 72px rgba(64 156 255 / 0.9),
      inset 0 0 66px rgba(255 255 255 / 0.35);
}

.chessboard {
    display: grid;
    grid-template-columns: repeat(8, 72px);
    grid-template-rows: repeat(8, 72px);
    border-radius: 36px;
    box-shadow: 0 0 30px rgba(64 156 255 / 0.6);
    margin: 0 auto;
}

.square {
    border-radius: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: 0.3s ease all;
    cursor: pointer;
}
.square.light {
    background: linear-gradient(135deg, #c6d7ff, #a6c9ff);
    color: #1b3169;
    box-shadow: inset 0 0 8px rgba(255 255 255 / 0.75);
}
.square.dark {
    background: linear-gradient(135deg, #5079c5, #2f51a2);
    color: #cde3ff;
}
.square.selected {
    background: radial-gradient(circle at center, #ffd700a0, #bf9a00a0);
    box-shadow: 0 0 28px 6px #ffd700cc, inset 0 0 20px #fff2aaaa;
    transform: scale(1.15);
    transition: 0.2s ease all;
    z-index: 5;
    position: relative;
}
.square.move {
    background: radial-gradient(circle at center, #54a0ffc2, #1972deae);
    box-shadow: 0 0 28px 5px #1972dea9;
}
.square:hover:not(.selected):not(.move) {
    transform: scale(1.10);
    box-shadow: 0 0 16px 6px #5aa4ffcc;
}

.piece {
    font-size: 3.8rem;
    user-select: none;
    filter: drop-shadow(0 0 4px #72a0ff);
    transition: filter 0.3s ease, transform 0.3s ease;
}

.piece.king {
    animation: kingGlow 6s ease-in-out infinite;
}
@keyframes kingGlow {
  0%, 100% {filter: drop-shadow(0 0 6px #ffd700cc);}
  50% {filter: drop-shadow(0 0 20px #fff166cc);}
}

.piece.queen {
    animation: queenGlow 4s ease-in-out infinite;
}
@keyframes queenGlow {
  0%, 100% {opacity: 1; filter: drop-shadow(0 0 10px #54a0ffcc);}
  50% {opacity: 0.85; filter: drop-shadow(0 0 24px #7cc3ffcc);}
}

.piece.rook, .piece.bishop, .piece.knight, .piece.pawn {
    animation: pulse 5s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% {filter: drop-shadow(0 0 6px #5dd0ffcc);}
  50% {filter: drop-shadow(0 0 20px #a6d5ffcc);}
}

.chess-bubble button:hover > .piece {
    transform: scale(1.22);
    filter: drop-shadow(0 0 30px #ffd966cc);
}

</style>
""", unsafe_allow_html=True)


def init_game():
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
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "intermediate"
    if 'waiting' not in st.session_state:
        st.session_state.waiting = False


def square_name_from_index(index):
    file = index % 8
    rank = 8 - (index // 8)
    return chr(ord('a') + file) + str(rank)


def handle_clicks():
    # Using latest recommended way to read query params
    qp = st.experimental_get_query_params()
    if 'square' in qp:
        clicked = int(qp['square'][0])
        selected = st.session_state.selected_square
        board = st.session_state.board

        # Deselect if clicked same square
        if selected == clicked:
            st.session_state.selected_square = None
            st.experimental_set_query_params()
            st.experimental_rerun()
            return

        if selected is None:
            piece = board.piece_at(clicked)
            if piece is not None and piece.color == board.turn:
                st.session_state.selected_square = clicked
            st.experimental_set_query_params()
            st.experimental_rerun()
            return

        # Try move if second click
        move = chess.Move(selected, clicked)

        # Check for promotion case on last rank
        piece = board.piece_at(selected)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color and clicked >= 56) or (not piece.color and clicked < 8):
                move = chess.Move(selected, clicked, promotion=chess.QUEEN)

        if move in board.legal_moves:
            board.push(move)
            st.session_state.move_history.append(move.uci())
            st.session_state.selected_square = None
            st.experimental_set_query_params()
            st.experimental_rerun()
        else:
            # Select new square if invalid move
            piece = board.piece_at(clicked)
            if piece and piece.color == board.turn:
                st.session_state.selected_square = clicked
                st.experimental_set_query_params()
                st.experimental_rerun()
            else:
                st.session_state.selected_square = None
                st.experimental_set_query_params()
                st.experimental_rerun()


def render_board():
    board = st.session_state.board
    selected = st.session_state.selected_square

    files = 'abcdefgh'
    ranks = range(8, 0, -1)

    st.markdown('<div class="chess-bubble">', unsafe_allow_html=True)
    st.markdown('<div class="chessboard">', unsafe_allow_html=True)

    for rank in ranks:
        for file_i in range(8):
            square = chess.square(file_i, rank - 1)
            color_square = 'light' if (rank + file_i) % 2 == 0 else 'dark'
            is_selected = (selected == square)
            has_move = False
            if selected is not None:
                legal = [move for move in board.legal_moves if move.from_square == selected]
                has_move = any(move.to_square == square for move in legal)
            piece = board.piece_at(square)

            classes = f"square {color_square}"
            if is_selected:
                classes = 'square selected'
            elif has_move:
                classes = 'square move'

            # Piece unicode with styling classes for animation
            piece_unicode = ''
            piece_class = ''
            if piece:
                piece_unicode_map = {
                    chess.PAWN: ('♙', 'pawn'),
                    chess.KNIGHT: ('♘','knight'),
                    chess.BISHOP: ('♗','bishop'),
                    chess.ROOK: ('♖','rook'),
                    chess.QUEEN: ('♕','queen'),
                    chess.KING: ('♔','king'),
                }
                p_char, p_class = piece_unicode_map.get(piece.piece_type, ('', ''))
                # flip color for black pieces
                if not piece.color:
                    p_char = p_char.lower()
                piece_unicode = p_char
                piece_class = f'piece {p_class}'

            sq_name = square_name_from_index(square)

            # Render each square button
            html = f"""
            <div class="{classes}" title="{sq_name}">
              <button style="all:unset; width:100%; height:100%; cursor:pointer; user-select:none;"
                onclick="(() => {{
                  const queryParams = new URLSearchParams(window.location.search);
                  queryParams.set('square', {square});
                  window.history.replaceState(null, '', window.location.pathname + '?' + queryParams);
                  const input = document.createElement('input');
                  input.type = 'hidden';
                  input.name = 'square';
                  input.value = {square};
                  input.id = 'square-input';
                  if(document.getElementById('square-input')) document.getElementById('square-input').remove();
                  document.body.appendChild(input);
                  const evt = new Event('submit');
                  document.dispatchEvent(evt);
                }})()">
                <span class="{piece_class}">{piece_unicode}</span>
              </button>
            </div>"""
            st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


def main():
    init_game()
    handle_clicks()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 Glass Chess 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)

    render_board()

    # Show game info
    board = st.session_state.board
    status, msg = "normal", "Game in progress"

    if board.is_checkmate():
        status, msg = "checkmate", "💥 Checkmate! Game over."
    elif board.is_stalemate():
        status, msg = "stalemate", "♖ Stalemate! Draw."
    elif board.is_check():
        status, msg = "check", "🛡️ Check! Protect your king."

    st.markdown(f'<div class="glass-subtitle" style="text-align:center; margin-top:1rem;">{msg}</div>', unsafe_allow_html=True)

    # Show move history
    st.markdown("<h3 style='text-align:center;'>Move History</h3>", unsafe_allow_html=True)
    moves_str = ""
    for idx, move in enumerate(st.session_state.move_history, 1):
        moves_str += f"{idx}. {move} &nbsp;&nbsp; "
        if idx % 5 == 0:
            moves_str += "<br>"

    st.markdown(f"<div style='font-family: SF Mono, monospace; font-size:14px; color:#aad4ff; max-height:150px; overflow:auto; background: rgba(20,30,60,0.5); border-radius:12px; padding:10px;'>{moves_str}</div>", unsafe_allow_html=True)

    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 New Game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.selected_square = None
            st.experimental_set_query_params()
            st.experimental_rerun()
    with col2:
        if st.button("↩️ Undo Move"):
            if len(st.session_state.board.move_stack) > 0:
                st.session_state.board.pop()
                if st.session_state.move_history:
                    st.session_state.move_history.pop()
                st.session_state.selected_square = None
                st.experimental_set_query_params()
                st.experimental_rerun()
    with col3:
        if st.button("🤖 AI Move"):
            if st.session_state.board.turn and len(list(st.session_state.board.legal_moves)) > 0:
                moves = list(st.session_state.board.legal_moves)
                ai_move = random.choice(moves)
                st.session_state.board.push(ai_move)
                st.session_state.move_history.append(ai_move.uci())
                st.session_state.selected_square = None
                st.experimental_set_query_params()
                st.experimental_rerun()
    with col4:
        if st.button("📋 Show FEN"):
            st.code(st.session_state.board.fen())

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
