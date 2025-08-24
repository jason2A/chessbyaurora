import streamlit as st
import chess
import time
import random

# Page config
st.set_page_config(
    page_title="💎 Glass Chess Blue Elegance",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Blue Glass CSS with animations
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
    text-shadow: 0 0 30px #58a6ff, 0 0 50px #79b4ff;
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
    margin: 1.5rem auto 3rem;
    border-radius: 20px;
    box-shadow: 0 0 55px rgba(58,123,212,0.8);
    background: linear-gradient(135deg, #134ba8, #abcfff);
    user-select: none;
}

/* Squares */
.square {
    width: 80px;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 14px;
    transition: background 0.4s cubic-bezier(0.4,0,0.2,1), box-shadow 0.3s ease;
    box-shadow: inset 0 0 3px 0 rgba(0,70, 210, 0.4);
    filter: drop-shadow(0 0 3px rgba(18,123,255,0.5));
    cursor: pointer;
}

.square.light {
    background: linear-gradient(145deg, #a9c9ff, #7aaaff);
    color: #143a70;
    box-shadow: 0 0 6px 2px #88aaff7f;
}

.square.dark {
    background: linear-gradient(145deg, #1a2e6c, #134874);
    color: #dcefff98;
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

/* Chess piece animations */
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
    user-select:none;
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
    if 'ai_thinking_time' not in st.session_state:
        st.session_state.ai_thinking_time = 2
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True


def make_move(move_uci):
    try:
        move = chess.Move.from_uci(move_uci)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_uci)
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            return True
    except:
        pass
    return False


def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        st.session_state.selected_square = square
        st.session_state.valid_moves = [move for move in st.session_state.board.legal_moves if move.from_square == square]
    else:
        st.session_state.selected_square = None
        st.session_state.valid_moves = []


def handle_square_click():
    if "chess_square_click" not in st.experimental_get_query_params():
        return
    square = int(st.experimental_get_query_params()["chess_square_click"][0])
    current_time = time.time()

    if st.session_state.selected_square is not None:
        from_square = st.session_state.selected_square
        to_square = square
        move = chess.Move(from_square, to_square)

        piece = st.session_state.board.piece_at(from_square)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color and to_square >= 56) or (not piece.color and to_square <= 7):
                move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

        if move in st.session_state.board.legal_moves:
            if make_move(str(move)):
                st.experimental_set_query_params()
                st.experimental_rerun()
        else:
            select_square(square)
            st.experimental_set_query_params()
            st.experimental_rerun()
    else:
        select_square(square)
        st.experimental_set_query_params()
        st.experimental_rerun()

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

            color_style = "color:#dcefff;" if piece and piece.color else "color:#4b6ec8;"

            square_html = f"""
            <div class="{' '.join(classes)}">
              <button 
                style="all:unset;cursor:pointer;width:100%;height:100%;font-size:3.7rem;{color_style}" 
                onclick="handleChessClick({square})" 
                title="{chr(97 + file)}{rank + 1}">
                <span class="{piece_class}">{piece_symbol}</span>
              </button>
            </div>"""

            st.markdown(square_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <script>
    function handleChessClick(square) {
        const eInput = document.getElementById('chess-click-input');
        if (eInput) eInput.remove();
        let input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', {detail:{square: square}});
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)

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

def main():
    init_chess_game()
    handle_square_click()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        st.markdown(f'<div class="status-message status-{status}">{message}</div>', unsafe_allow_html=True)

    # Include your other UI elements: game controls, multiplayer, AI, stats, etc., here

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
