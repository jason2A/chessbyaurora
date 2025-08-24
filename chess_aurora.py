import streamlit as st
import chess
import time

st.set_page_config(page_title="💎 Glass Chess Animated Pieces", page_icon="💎", layout="wide")

# CSS: Transparent blue luxury pieces with animations inspired by Dr. Wolf
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Mono&display=swap');

    body, .stApp {
        background: linear-gradient(135deg, #0a1227 0%, #152a70 50%, #0a1b5e 100%);
        color: #e0eaff;
        font-family: 'SF Mono', monospace, monospace;
    }

    .glass-container {
        background: rgba(20, 35, 70, 0.15);
        border-radius: 28px;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 900px;
        box-shadow: 0 8px 30px rgba(0, 90, 255, 0.4);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        position: relative;
    }

    .chess-board-container {
        display: grid;
        grid-template-columns: repeat(8, 70px);
        grid-template-rows: repeat(8, 70px);
        gap: 5px;
        justify-content: center;
        margin: 2rem auto;
        user-select: none;
    }

    .chess-square-button {
        border-radius: 12px;
        border: 3px solid rgba(64, 156, 255, 0.3);
        font-family: 'SF Mono', monospace;
        font-weight: 700;
        font-size: 2.8rem;
        background: rgba(64, 156, 255, 0.1);
        color: rgba(255, 255, 255, 0.85);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        position: relative;
        overflow: visible;
        box-shadow:
            0 0 15px rgba(64, 156, 255, 0.3),
            inset 0 0 8px rgba(64, 156, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        animation: pieceGlint 6s ease-in-out infinite alternate;
    }
    /* Hover glow */
    .chess-square-button:hover {
        color: #cce6ff;
        box-shadow:
            0 0 30px rgba(64, 200, 255, 0.8),
            inset 0 0 15px rgba(64, 200, 255, 0.45);
        transform: scale(1.1);
        z-index: 10;
    }

    /* Selected square */
    .chess-square-button.selected {
        background: rgba(0, 120, 255, 0.6);
        box-shadow:
            0 0 30px rgba(0, 140, 255, 1),
            inset 0 0 20px rgba(64, 180, 255, 0.7);
        color: #e0f4ff;
        animation: selectedPulse 2.5s ease-in-out infinite;
    }

    /* Valid move highlight */
    .chess-square-button.valid-move {
        background: rgba(0, 180, 255, 0.35);
        box-shadow:
            0 0 18px rgba(0, 180, 255, 0.75);
        color: white;
    }

    /* Subtle piece glow animation */
    @keyframes pieceGlint {
        0% {
            text-shadow: 0 0 12px rgba(64, 156, 255, 0.5);
            filter: brightness(1);
        }
        50% {
            text-shadow: 0 0 20px rgba(64, 200, 255, 0.9);
            filter: brightness(1.15);
        }
        100% {
            text-shadow: 0 0 12px rgba(64, 156, 255, 0.5);
            filter: brightness(1);
        }
    }

    /* Selected square pulse glow */
    @keyframes selectedPulse {
        0%, 100% {
            box-shadow:
                0 0 30px rgba(0, 140, 255, 1),
                inset 0 0 20px rgba(64, 180, 255, 0.7);
        }
        50% {
            box-shadow:
                0 0 45px rgba(0, 170, 255, 1),
                inset 0 0 30px rgba(64, 220, 255, 0.9);
        }
    }

    .tutor-hint {
        position: absolute;
        top: -26px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(64, 156, 255, 0.9);
        color: #00152d;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
        pointer-events: none;
        box-shadow: 0 0 20px rgba(64, 156, 255, 0.7);
        animation: hintFloat 2.5s ease-in-out infinite;
        user-select: none;
    }

    @keyframes hintFloat {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-4px); }
    }

</style>
""", unsafe_allow_html=True)


def init_chess_game():
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True


def get_tutor_hint(board, selected_square):
    if selected_square is None:
        return None
    piece = board.piece_at(selected_square)
    if not piece or piece.color != board.turn:
        return None
    moves = [m for m in board.legal_moves if m.from_square == selected_square]
    if not moves:
        return None
    return f"Try {board.san(moves[0])}", 0.8


def display_board(board):
    selected_square = st.session_state.get('selected_square')
    valid_moves = st.session_state.get('valid_moves', [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)
    piece_symbols = {
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
    }

    for rank in range(7, -1, -1):
        for file in range(8):
            square = rank * 8 + file
            piece = board.piece_at(square)
            symbol = piece_symbols.get(piece.symbol(), "") if piece else ""

            tutor_hint = ""
            if st.session_state.get('tutor_mode') and st.session_state.get('show_hints'):
                hint = get_tutor_hint(board, selected_square)
                if hint and selected_square == square:
                    hint_text, _ = hint
                    tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'

            class_names = ["chess-square-button"]
            if square == selected_square:
                class_names.append("selected")
            elif any(move.to_square == square for move in valid_moves):
                class_names.append("valid-move")

            st.markdown(f"""
            <div style="position:relative;">
                <button class="{' '.join(class_names)}" 
                    onclick="handleChessClick({square})"
                    title="{chr(97+file)}{rank+1}" aria-label="Square {chr(97+file)}{rank+1}">
                    {symbol}
                </button>
                {tutor_hint}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    function handleChessClick(square) {
        const input = document.createElement('input');
        input.type='hidden';
        input.name='chess_square_click';
        input.value=square;
        input.id='chess-click-input';
        const existing = document.getElementById('chess-click-input');
        if(existing) existing.remove();
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', {detail:{square:square}});
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        st.session_state.selected_square = square
        st.session_state.valid_moves = [m for m in st.session_state.board.legal_moves if m.from_square == square]
    else:
        st.session_state.selected_square = None
        st.session_state.valid_moves = []


def make_move(from_sq, to_sq):
    move = chess.Move(from_sq, to_sq)
    if move in st.session_state.board.legal_moves:
        st.session_state.board.push(move)
        st.session_state.selected_square = None
        st.session_state.valid_moves = []
        return True
    return False


def handle_square_click():
    if "chess_square_click" in st.experimental_get_query_params():
        try:
            clicked = int(st.experimental_get_query_params()["chess_square_click"][0])
            selected = st.session_state.get('selected_square')
            if selected is None:
                select_square(clicked)
            else:
                if make_move(selected, clicked):
                    st.experimental_rerun()
                else:
                    select_square(clicked)
        except Exception:
            pass


def main():
    init_chess_game()
    handle_square_click()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS Animated Transparent Pieces 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Interactive transparent glassy blue pieces with animations</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
