import streamlit as st
import chess
import time
import random

st.set_page_config(page_title="💎 Glass Chess Blue Elegance", page_icon="💎", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;700&display=swap');

body, .stApp {
    margin: 0; padding: 0;
    background: linear-gradient(135deg, #0a1f44 0%, #01294f 50%, #105385 100%);
    color: #c1dbee;
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
}

.glass-container {
    max-width: 1000px;
    margin: 2rem auto;
    background: rgba(16, 60, 124, 0.17);
    border-radius: 32px;
    backdrop-filter: blur(28px);
    border: 1px solid rgba(54, 120, 200, 0.6);
    box-shadow: 0 0 40px rgba(10, 110, 220, 0.3), inset 0 0 15px rgba(0,120,220,0.15);
    padding: 2.5rem;
    position: relative;
    user-select: none;
}

.glass-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 700;
    color: #58a6ff;
    text-shadow: 
      0 0 30px #58a6ff, 
      0 0 50px #79b4ff;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    animation: titleGlow 4s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    0% { text-shadow: 0 0 20px #1f6fe1; }
    100% { text-shadow: 0 0 50px #a1c9ff; }
}

.glass-subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #a6c8ffcc;
    font-weight: 400;
    margin-bottom: 2rem;
    text-shadow: 0 0 4px #71a7ff;
    animation: subtitlePulse 5s ease-in-out infinite;
}

@keyframes subtitlePulse {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
}

.chess-board-container {
    display: grid;
    grid-template-columns: repeat(8, 80px);
    grid-template-rows: repeat(8, 80px);
    justify-content: center;
    margin: 1.5rem auto 3rem auto;
    border-radius: 20px;
    box-shadow: 0 0 55px rgba(58,123,212,0.8);
    background: linear-gradient(135deg, #134ba8, #abcfff);
    user-select:none;
}

.square {
    width: 80px;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3.7rem;
    font-weight: 700;
    border-radius: 14px;
    color: #dbe9ff;
    cursor: pointer;
    transition: background 0.4s cubic-bezier(0.4,0,0.2,1), box-shadow 0.3s ease;
    box-shadow: inset 0 0 3px 0 rgba(0,70, 210, 0.4);
    filter: drop-shadow(0 0 3px rgba(18,123,255,0.5));
    user-select:none;
}

.square.light {
    background: linear-gradient(145deg, #a9c9ff, #7aaaff);
    color: #143a70;
    box-shadow: 0 0 6px 2px #88aaff7f;
}

.square.dark {
    background: linear-gradient(145deg, #1a2e6c, #134874);
}

.square.selected {
    background: #3f7be8ff !important;
    box-shadow: 0 0 18px 8px #3f7be8bb !important;
    color: #e2f3ff !important;
    transform: scale(1.07) !important;
    font-weight: 900;
}

.square.move {
    background: #5fa1fff0 !important;
    box-shadow: 0 0 14px 5px #88b7ffcc !important;
}

.square:hover:not(.selected):not(.move) {
    filter: drop-shadow(0 0 11px #0d59b9cc);
    transform: scale(1.05);
    transition: transform 0.15s ease;
}

/* Piece floating animations */
.piece-king { animation: kingFloat 4s ease-in-out infinite; }
.piece-queen { animation: queenGlow 3s ease-in-out infinite; }
.piece-rook { animation: rookPulse 2.5s ease-in-out infinite; }
.piece-bishop { animation: bishopFloat 3.5s ease-in-out infinite; }
.piece-knight { animation: knightBounce 2s ease-in-out infinite; }
.piece-pawn { animation: pawnWave 2.8s ease-in-out infinite; }

@keyframes kingFloat {
    0%, 100% { transform: translateY(2px); text-shadow: 0 0 12px #1d59ff; }
    50% { transform: translateY(-4px); text-shadow: 0 0 24px #346aff; }
}

@keyframes queenGlow {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
}

@keyframes rookPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}

@keyframes bishopFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}

@keyframes knightBounce {
    0%, 100% { transform: translateY(0) rotate(0); }
    25% { transform: translateY(-3px) rotate(1deg); }
    75% { transform: translateY(-3px) rotate(-1deg); }
}

@keyframes pawnWave {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-1.5px) scale(1.02); }
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3a68ffcc, #1151d1cc) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    box-shadow: 0 0 25px 5px #4488ffcc;
    padding: 0.8rem 1.8rem !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #568eff, #2965c0) !important;
    box-shadow: 0 0 40px 8px #87aaffcc;
    transform: translateY(-3px) scale(1.06) !important;
}

/* Info Panels */
.glass-info {
    background: rgba(70, 120, 230, 0.12);
    border-radius: 24px;
    padding: 16px 28px;
    margin-top: 1.5rem;
    color: #bbd2ff;
    text-align: center;
    box-shadow: 0 0 30px rgba(82, 114, 255, 0.55);
    font-weight: 600;
    user-select:none;
}

/* Move history */
.move-history {
    max-height: 320px;
    overflow-y: auto;
    background: rgba(30, 60, 110, 0.3);
    border-radius: 20px;
    color: #a8c3ff;
    padding: 1rem 1.5rem;
    font-weight: 500;
    box-shadow: 0 0 24px rgba(60, 80, 120, 0.55);
}

/* Scrollbar styling */
.move-history::-webkit-scrollbar {
    width: 10px;
}
.move-history::-webkit-scrollbar-thumb {
    background: rgba(100,140,255,0.6);
    border-radius: 30px;
}

</style>
""", unsafe_allow_html=True)

def display_board(board):
    selected_square = st.session_state.get("selected_square", None)
    valid_moves = st.session_state.get("valid_moves", [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)

    for rank in range(7, -1, -1):
        for file in range(8):
            square = rank * 8 + file
            piece = board.piece_at(square)

            square_color = "light" if (rank + file) % 2 == 0 else "dark"
            classes = ["square", square_color]
            if selected_square == square:
                classes.append("selected")
            elif any(move.to_square == square for move in valid_moves):
                classes.append("move")

            piece_symbol = ""
            piece_class = ""
            if piece:
                piece_symbols = {
                    'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
                    'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
                }
                piece_symbol = piece_symbols.get(piece.symbol(), piece.symbol())
                piece_class = f"piece-{piece.symbol().lower()}"

            style = f"width: 100%; height: 80px; font-size: 3.7rem; color: {'#5746be' if piece and piece.color else 'rgb(124 137 237)'}; user-select:none;"

            btn_html = f"""
            <div class="{' '.join(classes)}" style="position:relative;">
                <button 
                    style="{style} border:none; background:none; outline:none; cursor:pointer;" 
                    onclick="handleChessClick({square})" 
                    title="{chr(97 + file)}{rank +1}">
                    <span class="{piece_class}">{piece_symbol}</span>
                </button>
            </div>"""

            st.markdown(btn_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Javascript for seamless clicks
    st.markdown("""
        <script>
        function handleChessClick(square) {
            const eInput = document.createElement('input');
            eInput.type = 'hidden';
            eInput.name = 'chess_square_click';
            eInput.value = square;
            eInput.id = 'chess-click-input';
            if (document.getElementById('chess-click-input'))
                document.getElementById('chess-click-input').remove();
            document.body.appendChild(eInput);
            const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
            document.dispatchEvent(event);
        }
        </script>
    """, unsafe_allow_html=True)
