import streamlit as st
import chess
import time
import random
import json
import os

# Page config
st.set_page_config(
    page_title="💎 Glass Chess - Luxurious Red",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Luxurious Red Glassy CSS with animations and multiplayer styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');

body, .stApp {
    background: linear-gradient(135deg, #1a0a0a 0%, #3e1212 25%, #5c1818 50%, #7d2121 75%, #9e2b2b 100%);
    background-size: 400% 400%;
    animation: glassGradient 12s ease infinite;
    color: white;
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
}

@keyframes glassGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.glass-container {
    background: rgba(255, 230, 230, 0.12);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-radius: 32px;
    border: 1px solid rgba(195, 40, 40, 0.4);
    padding: 3rem;
    margin: 2rem auto;
    max-width: 1400px;
    box-shadow: 0 8px 32px rgba(195, 40, 40, 0.6),
                inset 0 1px 0 rgba(255, 69, 58, 0.2);
    animation: containerFloat 6s ease-in-out infinite;
    position: relative;
}

@keyframes containerFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.glass-title {
    text-align: center;
    color: #c32828;
    font-weight: 700;
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    text-shadow:
        0 0 20px rgba(255, 69, 58, 0.9),
        0 0 40px rgba(255, 215, 0, 0.5);
    animation: glassTitle 4s ease-in-out infinite alternate;
    letter-spacing: -0.02em;
    position: relative;
}

@keyframes glassTitle {
    0% {
        text-shadow: 0 0 20px rgba(195, 40, 40, 0.8), 0 0 40px rgba(255,69,58,0.7);
        transform: scale(1) rotateY(0deg);
    }
    100% {
        text-shadow: 0 0 30px rgba(255, 69, 58, 0.9), 0 0 50px rgba(255, 215, 0, 0.7);
        transform: scale(1.02) rotateY(2deg);
    }
}

.glass-subtitle {
    text-align: center;
    color: rgba(255, 120, 120, 0.8);
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
    display: grid;
    grid-template-columns: repeat(8, 70px);
    grid-template-rows: repeat(8, 70px);
    justify-content: center;
    margin: 2.5rem 0;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(255, 69, 58, 0.8);
    background: linear-gradient(135deg, rgba(195,40,40,0.7), rgba(255,69,58,0.5));
    user-select: none;
}

.square {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3rem;
    font-weight: 700;
    cursor: pointer;
    border-radius: 12px;
    transition: background-color 0.4s ease, box-shadow 0.3s ease;
}

.square.light {
    background: rgba(255, 200, 200, 0.15);
}

.square.dark {
    background: rgba(120, 20, 20, 0.8);
}

.square.selected {
    background: rgba(255, 69, 58, 0.85) !important;
    box-shadow: 0 0 15px 4px rgba(255, 69, 58, 0.9);
}

.square.move {
    background: rgba(255, 180, 180, 0.7) !important;
    box-shadow: 0 0 12px 3px rgba(255, 115, 115, 0.9);
}

.square:hover {
    box-shadow: 0 0 25px 6px rgba(255, 80, 80, 0.8);
}

.piece {
    animation-duration: 4s;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
}

.piece-king { animation-name: kingGlow; color: #ff6b6b; }
.piece-queen { animation-name: queenGlow; color: #ff8383; }
.piece-rook { animation-name: rookPulse; color: #ff5252; }
.piece-bishop { animation-name: bishopFloat; color: #ff4c4c; }
.piece-knight { animation-name: knightBounce; color: #ff5959; }
.piece-pawn { animation-name: pawnWave; color: #ff6565; }

@keyframes kingGlow {
    0%,100% { text-shadow: 0 0 7px rgba(255, 105, 105, 0.7); }
    50% { text-shadow: 0 0 30px rgba(255, 0, 0, 0.9); }
}

@keyframes queenGlow {
    0%,100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes rookPulse {
    0%,100% { transform: scale(1);}
    50% { transform: scale(1.07);}
}

@keyframes bishopFloat {
    0%,100% { transform: translateY(0);}
    50% { transform: translateY(-3px);}
}

@keyframes knightBounce {
    0%,100% { transform: translateY(0) rotate(0);}
    25% { transform: translateY(-3px) rotate(2deg);}
    75% { transform: translateY(-3px) rotate(-2deg);}
}

@keyframes pawnWave {
    0%,100% { transform: translateY(0);}
    50% { transform: translateY(-1.7px);}
}

.glass-info {
    background: rgba(255, 180, 180, 0.15);
    backdrop-filter: blur(18px);
    border-radius: 24px;
    border: 1px solid rgba(255, 69, 58, 0.4);
    padding: 2rem;
    margin: 1.5rem 0;
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    box-shadow: 0 8px 32px rgba(255, 80, 80, 0.35);
    color: #ffc2c2;
    user-select: none;
}

.status-message {
    font-weight: 700;
    text-align: center;
    padding: 1rem;
    font-size: 1.1rem;
    color: #ff4c4c;
    text-shadow: 0 0 5px rgba(255,69,58,0.8);
}

.drag-instructions {
    background: rgba(255, 220, 220, 0.15);
    border-radius: 20px;
    color: #ff6969;
    font-weight: 600;
    padding: 1rem;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 0 15px rgba(255, 100, 100, 0.6);
    user-select: none;
}

/* Button styling retained but changed to red gradients */
.stButton > button {
    background: linear-gradient(135deg, rgba(255, 69, 58, 0.85), rgba(195, 40, 40, 0.85)) !important;
    border-radius: 20px !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 8px 32px rgba(255, 69, 58, 0.5);
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(255, 115, 115, 0.85), rgba(215, 80, 80, 0.85)) !important;
    box-shadow: 0 0 40px rgba(255, 69, 58, 0.9);
    transform: translateY(-3px) scale(1.05);
    transition: all 0.3s ease;
}

</style>
""", unsafe_allow_html=True)


def init_chess_game():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "move_history" not in st.session_state:
        st.session_state.move_history = []
    if "selected_square" not in st.session_state:
        st.session_state.selected_square = None
    if "valid_moves" not in st.session_state:
        st.session_state.valid_moves = []
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "single"
    if "room_code" not in st.session_state:
        st.session_state.room_code = None
    if "waiting_for_opponent" not in st.session_state:
        st.session_state.waiting_for_opponent = False
    if "difficulty_level" not in st.session_state:
        st.session_state.difficulty_level = "intermediate"
    if "show_hints" not in st.session_state:
        st.session_state.show_hints = True
    if "ai_thinking_time" not in st.session_state:
        st.session_state.ai_thinking_time = 2


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
            st.error("💎 Invalid move!")
            return False
    except:
        st.error("💎 Invalid move format!")
        return False


def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        st.session_state.selected_square = square
        st.session_state.valid_moves = [m for m in st.session_state.board.legal_moves if m.from_square == square]
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
        if piece and piece.piece_type == chess.PAWN and (to_sq >= 56 or to_sq <= 7):
            move = chess.Move(from_sq, to_sq, chess.QUEEN)
        if move in st.session_state.board.legal_moves:
            if make_move(move.uci()):
                st.experimental_rerun()
        else:
            select_square(square)
    else:
        select_square(square)


def display_board():
    board = st.session_state.board
    selected = st.session_state.get("selected_square", None)
    valid_moves = st.session_state.get("valid_moves", [])

    cols = st.columns(8, gap="small")
    for rank in range(7, -1, -1):
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)

            is_light = (file + rank) % 2 == 0
            classes = ["square", "light" if is_light else "dark"]
            if selected == square:
                classes.append("selected")
            elif any(m.to_square == square for m in valid_moves):
                classes.append("move")

            piece_char = ""
            piece_class = ""

            if piece:
                unicode_map = {
                    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
                    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
                }
                piece_char = unicode_map[piece.symbol()]
                piece_class = "piece-" + piece.symbol().lower()

            container = st.container()
            with container:
                btn = st.button(piece_char or " ", key=f"square_{square}", help=chess.square_name(square))
                if btn:
                    handle_square_click(square)

                # Inject styling for button
                st.markdown(f'''
                <style>
                div.stButton > button[key="square_{square}"] {{
                    all: unset;
                    cursor: pointer;
                    font-size: 3rem;
                    width: 70px;
                    height: 70px;
                    text-align: center;
                    color: {'#ff6969' if piece and piece.color else 'rgba(255,255,255,0.5)'};
                    border-radius: 12px;
                    background-color: {"#ff4c4c" if selected == square else ("#ffbaba" if any(m.to_square==square for m in valid_moves) else ("#ffcfcf" if is_light else "#700101"))};
                    box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
                    transition: all 0.3s ease;
                }}
                div.stButton > button[key="square_{square}"]:hover {{
                    background-color: #ff5959;
                    box-shadow: 0 0 15px #ff3c3c;
                    transform: scale(1.1);
                }}
                .piece-{piece_class} {{
                    animation-duration: 4s;
                    animation-iteration-count: infinite;
                    animation-timing-function: ease-in-out;
                }}
                .piece-king {{ animation-name: kingGlow; }}
                .piece-queen {{ animation-name: queenGlow; }}
                .piece-rook {{ animation-name: rookPulse; }}
                .piece-bishop {{ animation-name: bishopFloat; }}
                .piece-knight {{ animation-name: knightBounce; }}
                .piece-pawn {{ animation-name: pawnWave; }}

                @keyframes kingGlow {{
                    0%,100% {{ text-shadow: 0 0 7px #ff4c4c; }}
                    50% {{ text-shadow: 0 0 20px #ff0000; }}
                }}
                @keyframes queenGlow {{ 0%,100% {{opacity:1;}} 50% {{opacity:0.7;}} }}
                @keyframes rookPulse {{0%,100%{{transform:scale(1)}} 50%{{transform:scale(1.07)}}}}
                @keyframes bishopFloat {{0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-3px)}}}}
                @keyframes knightBounce {{0%,100%{{transform: translateY(0) rotate(0)}} 25%{{transform: translateY(-3px) rotate(2deg)}} 75%{{transform: translateY(-3px) rotate(-2deg)}}}}
                @keyframes pawnWave {{0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-1.7px)}}}}
                </style>
                ''', unsafe_allow_html=True)
    st.write("")


def save_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            state = {
                "fen": st.session_state.board.fen(),
                "move_history": st.session_state.move_history,
                "last_update": time.time()
            }
            filename = f"game_{st.session_state.room_code}.json"
            with open(filename, "w") as f:
                json.dump(state, f)
            return True
        except Exception as e:
            st.error(f"Error saving game state: {e}")
            return False
    return False


def load_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            filename = f"game_{st.session_state.room_code}.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    state = json.load(f)
                st.session_state.board = chess.Board(state["fen"])
                st.session_state.move_history = state["move_history"]
                return True
        except Exception:
            return False
    return False


def create_multiplayer_game():
    import string
    room = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    st.session_state.room_code = room
    st.session_state.game_mode = "multiplayer"
    st.session_state.waiting_for_opponent = True
    return room


def join_multiplayer_game(room_code):
    if room_code and len(room_code) == 6:
        st.session_state.room_code = room_code.upper()
        st.session_state.game_mode = "multiplayer"
        st.session_state.waiting_for_opponent = False
        load_game_state()
        return True
    return False


def get_game_status(board):
    if board.is_checkmate():
        return "checkmate", "💎 CHECKMATE! The game is over! 💎"
    if board.is_stalemate():
        return "stalemate", "⚖️ STALEMATE! The game is a draw! ⚖️"
    if board.is_insufficient_material():
        return "stalemate", "⚖️ Draw due to insufficient material! ⚖️"
    if board.is_check():
        return "check", "⚡ CHECK! Your king is in danger! ⚡"
    return "normal", "💎 Game in progress 💎"


def main():
    init_chess_game()
    if st.session_state.game_mode == "multiplayer":
        load_game_state()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS (Red Luxury) 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear red interface</p>', unsafe_allow_html=True)
    
    # Multiplayer Lobby/UI
    if st.session_state.game_mode == "multiplayer":
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🌐 Multiplayer Game")
        if st.session_state.room_code:
            st.markdown(f"**Room Code:** `{st.session_state.room_code}`")
            st.markdown(f"**Your Color:** {get_player_color().title()}")
            if st.session_state.waiting_for_opponent:
                st.markdown("⏳ **Waiting for opponent to join...** Share this room code!")
            else:
                if is_player_turn():
                    st.markdown("✅ **Your turn!**")
                else:
                    st.markdown("⏳ **Opponent's turn** - please wait")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔙 Back to Single Player"):
                st.session_state.game_mode = "single"
                st.session_state.room_code = None
                st.session_state.waiting_for_opponent = False
                st.experimental_rerun()
        with col2:
            if st.button("🔄 Refresh Multiplayer Game"):
                load_game_state()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Single player mode multiplayer controls
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🎮 Game Mode")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌐 Create Multiplayer Game"):
                room_code = create_multiplayer_game()
                st.success(f"Multiplayer Game Created! Room Code: {room_code}")
                st.experimental_rerun()
        with col2:
            room_code_input = st.text_input("Join Multiplayer Room Code", max_chars=6)
            if st.button("🎯 Join Multiplayer Game"):
                if join_multiplayer_game(room_code_input):
                    st.success("Joined Multiplayer Game!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid Room Code")
        st.markdown("</div>", unsafe_allow_html=True)

    display_board()

    status, message = get_game_status(st.session_state.board)
    st.markdown(f'<div class="status-message">{message}</div>', unsafe_allow_html=True)

    # Game controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💎 New Game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()
    with col2:
        if st.button("↩️ Undo Move"):
            if len(st.session_state.move_history) > 0:
                st.session_state.board.pop()
                st.session_state.move_history.pop()
                st.session_state.selected_square = None
                st.experimental_rerun()
    with col3:
        if st.button("🎲 Random Move"):
            moves = list(st.session_state.board.legal_moves)
            if moves:
                mv = random.choice(moves)
                make_move(mv.uci())
                st.experimental_rerun()
    with col4:
        if st.button("📋 Copy FEN"):
            st.code(st.session_state.board.fen())

    st.markdown("""
    <div class="drag-instructions">
        🎯 <strong>How to Play:</strong> Click on a piece, then click on destination square to move. Selected pieces glow red, valid destinations highlight pink.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
