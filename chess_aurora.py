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

# CSS with blue-only luxury hues (no yellow)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');

    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .main, .stApp {
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

    .glass-container {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(30px);
        border-radius: 32px;
        border: 1px solid rgba(255,255,255,0.12);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow:
            0 8px 32px rgba(0,0,0,0.3),
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
    .glass-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(64,156,255,0.05) 50%, transparent 70%);
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
        text-shadow: 0 0 20px rgba(64,156,255,0.5);
        animation: glassTitle 4s ease-in-out infinite alternate;
        letter-spacing: -0.02em;
        position: relative;
    }
    @keyframes glassTitle {
        0% { 
            text-shadow: 0 0 20px rgba(64,156,255,0.5);
            transform: scale(1) rotateY(0deg);
        }
        100% { 
            text-shadow: 0 0 30px rgba(64,190,255,0.8);
            transform: scale(1.02) rotateY(2deg);
        }
    }

    .glass-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
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

    /* Chess square button styling - Blue luxury theme */
    .chess-square-button {
        border-radius: 12px !important;
        border: 3px solid rgba(64,156,255,0.3) !important;
        font-family: 'SF Mono', 'Monaco', 'Menlo', monospace !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow:
            0 4px 16px rgba(64,156,255,0.3),
            0 0 0 1px rgba(64,156,255,0.15),
            inset 0 1px 0 rgba(255,255,255,0.25) !important;
        min-height: 70px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
        background: linear-gradient(135deg,
            rgba(64,156,255,0.1),
            rgba(100,200,255,0.15),
            rgba(64,156,255,0.1)) !important;
    }
    .chess-square-button::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(64,156,255,0.1) 0%, transparent 70%);
        animation: liquidFlow 3s ease-in-out infinite;
        pointer-events: none;
    }
    @keyframes liquidFlow {
        0%,100% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-50%, -50%) rotate(180deg); }
    }
    .chess-square-button:hover {
        transform: scale(1.05) translateY(-2px) !important;
        box-shadow:
            0 8px 32px rgba(64,156,255,0.5),
            0 0 0 2px rgba(64,156,255,0.4),
            inset 0 1px 0 rgba(255,255,255,0.35) !important;
        border-color: rgba(64,156,255,0.6) !important;
        background: linear-gradient(135deg,
            rgba(64,156,255,0.2),
            rgba(100,200,255,0.25),
            rgba(64,156,255,0.2)) !important;
    }
    .chess-square-button:active {
        transform: scale(0.98) translateY(0px) !important;
        animation: pieceClick 0.3s ease-out !important;
    }
    @keyframes pieceClick {
        0% { transform: scale(1.05) translateY(-2px); }
        50% { transform: scale(0.95) translateY(1px); }
        100% { transform: scale(0.98) translateY(0px); }
    }

    /* Selected square highlight - blue glow */
    .chess-square-button.selected {
        background: rgba(0,120,255,0.85) !important;
        border-color: rgba(0,100,255,0.95) !important;
        box-shadow:
            0 0 20px rgba(0,120,255,1),
            inset 0 1px 0 rgba(255,255,255,0.4) !important;
        color: #d0eaff !important;
    }

    /* Valid move highlight - lighter blue */
    .chess-square-button.valid-move {
        background: rgba(0,150,255,0.6) !important;
        border-color: rgba(0,140,255,0.85) !important;
        box-shadow:
            0 0 15px rgba(0,180,255,0.8),
            inset 0 1px 0 rgba(255,255,255,0.25) !important;
        color: white !important;
    }

    /* Tutor hint styling with blue */
    .tutor-hint {
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(64,156,255,0.95) !important;
        color: #000e2b !important;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
        z-index: 1000;
        animation: hintFloat 2s ease-in-out infinite;
        box-shadow: 0 0 25px rgba(64,156,255,0.8) !important;
    }
    @keyframes hintFloat {
        0%, 100% { transform: translateX(-50%) translateY(0px); }
        50% { transform: translateX(-50%) translateY(-3px); }
    }
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    # Initialize all needed session state variables with defaults
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "intermediate"

def get_tutor_hint(board, selected_square):
    # Your existing tutor hint logic here or None if none available
    return None

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
                'k': '♔', 'q': '♕', 'r': '♖',
                'b': '♗', 'n': '♘', 'p': '♙',
                'K': '♚', 'Q': '♛', 'R': '♜',
                'B': '♝', 'N': '♞', 'P': '♟',
            }
            piece_symbol = piece_symbols.get(piece.symbol(), "") if piece else ""

            piece_class = ""
            if piece:
                pt = piece.symbol().lower()
                classes = {
                    'k': "piece-king",
                    'q': "piece-queen",
                    'r': "piece-rook",
                    'b': "piece-bishop",
                    'n': "piece-knight",
                    'p': "piece-pawn"
                }
                piece_class = classes.get(pt, "")

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
            if square == selected_square:
                button_classes.append("selected")
            elif any(move.to_square == square for move in valid_moves):
                button_classes.append("valid-move")

            bg_color = (
                'rgba(64,156,255,0.8)' if square == selected_square else
                'rgba(40,167,69,0.8)' if any(move.to_square == square for move in valid_moves) else
                'rgba(248,249,250,0.9)' if (rank + file) % 2 == 0 else
                'rgba(108,117,125,0.9)'
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
                        style="background: {bg_color};
                               color: {color};
                               width: 100%; height: 70px;
                               border: 3px solid rgba(64,156,255,0.3);
                               border-radius: 12px;
                               font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
                               font-weight: 700;
                               font-size: 2.5rem;
                               cursor: pointer;
                               transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                               display: flex;
                               align-items: center;
                               justify-content: center;
                               position: relative;
                               overflow: hidden;"
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
        if(existing) existing.remove();
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize game state variables and additional game logic as needed...

def main():
    init_chess_game()
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)
    display_board(st.session_state.board)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
