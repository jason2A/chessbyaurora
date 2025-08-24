import streamlit as st
import chess
import time
import random
import json
import os

st.set_page_config(
    page_title="💎 Glass Chess 3D - Luxurious Red",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;700&display=swap');

body, .stApp {
    margin:0; padding:0; overflow-x:hidden;
    background: linear-gradient(135deg, #1e0a09, #450909, #861414);
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #f2dede;
}

/* Container */
.glass-container {
    max-width: 960px;
    margin: 2rem auto;
    background: rgba(255, 220, 218, 0.15);
    border-radius: 32px;
    backdrop-filter: blur(28px);
    border: 1px solid rgba(255, 120, 110, 0.3);
    box-shadow:
        0 0 25px 8px rgba(255, 90, 80, 0.4),
        inset 0 0 4px 2px rgba(255, 100, 80, 0.15);
    padding: 2rem;
    position: relative;
    perspective: 1400px;
    animation: floatContainer 6s ease-in-out infinite;
}

@keyframes floatContainer {
    0%, 100% { transform: translateY(0);}
    50% { transform: translateY(-12px);}
}

/* Titles */
.glass-title {
    font-size: 4rem;
    font-weight: 700;
    color: #ff5e53;
    text-align: center;
    text-shadow:
      0 0 12px #ff5e53,
      0 0 40px #ff5e53;
    animation: titleGlow 3.5s ease-in-out alternate infinite;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}

@keyframes titleGlow {
    0% { text-shadow: 0 0 12px #ff5e53; }
    100% { text-shadow: 0 0 36px #ff9a8d;}
}

.glass-subtitle {
    text-align: center;
    font-weight: 400;
    font-size: 1.3rem;
    color: #ff9388;
    margin-bottom: 1.6rem;
    text-shadow: 0 0 6px #ff8575;
    letter-spacing: 0.02em;
    animation: subtitlePulse 5s ease-in-out infinite;
}

@keyframes subtitlePulse {
    0%, 100% { opacity: 0.9; }
    50% { opacity: 1; }
}

/* Chessboard container with 3D rotation */
.chessboard-3d {
    display: grid;
    grid-template-columns: repeat(8, 80px);
    grid-template-rows: repeat(8, 80px);
    margin: 0 auto;
    border-radius: 28px;
    box-shadow:
        0 0 40px #ff695c7f,
        inset 0 0 18px 6px #f75a4f88;
    transform-style: preserve-3d;
    animation: boardPulse 8s ease-in-out infinite;
    perspective: 1800px;
    cursor: pointer;
}

@keyframes boardPulse {
    0%, 100% { transform: rotateX(0deg) rotateY(0deg) translateZ(0); }
    50% { transform: rotateX(4deg) rotateY(8deg) translateZ(10px);}
}

/* Squares */
.square {
    width: 80px; height: 80px;
    user-select:none;
    border-radius: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    transform-origin: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    transition: background-color 0.3s cubic-bezier(0.4,0,0.2,1), box-shadow 0.3s ease;
    filter: drop-shadow(0 0 1.5px rgba(255,90,80,0.6));
    position: relative;
}

.square.light {
    background: #ffdedbcc;
    filter: drop-shadow(0 0 2px rgba(255,110,95,0.7));
}

.square.dark {
    background: #922a262c;
    filter: drop-shadow(0 0 2.5px rgba(255,65,65,0.9));
}

.square.selected {
    background: #ff5a4ddd !important;
    box-shadow: 0 0 18px 7px #ff7d71cc !important;
    transform: scale(1.05) !important;
}

.square.move {
    background: #fab7b1cc !important;
    box-shadow: 0 0 14px 5px #ff7d6e99 !important;
}

/* Hover Effect */
.square:not(.selected):hover {
    filter: drop-shadow(0 0 6px rgba(255, 120, 110,0.9));
    transform: translateZ(16px) scale(1.08);
    box-shadow: 0 0 24px 8px #ff6a5fbb;
    z-index: 1000;
    transition: transform 0.2s ease;
}

/* Chess pieces with 3D floating animations */
.piece {
    font-size: 3.7rem;
    font-weight: 900;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    text-shadow:
      0 0 4px rgba(245,85,80,0.85),
      0 0 11px rgba(250,137,129,0.9);
    user-select:none;
}

.piece-king { animation-name: kingFloat; color:#ff3f33;}
.piece-queen { animation-name: queenPulse; color:#ff5a4e;}
.piece-rook { animation-name: rookBounce; color:#ff4227;}
.piece-bishop { animation-name: bishopWave; color:#ff4f3d;}
.piece-knight { animation-name: knightShine; color:#ff4838;}
.piece-pawn { animation-name: pawnFloat; color:#ff665b;}

@keyframes kingFloat {
    0%, 100% { transform: translateY(1px) translateZ(10px) scale(1); }
    50% { transform: translateY(-6px) translateZ(20px) scale(1.09);}
}

@keyframes queenPulse {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
}

@keyframes rookBounce {
    0%, 100% { transform: translateY(0) translateZ(10px);}
    50% { transform: translateY(-3px) translateZ(18px);}
}

@keyframes bishopWave {
    0%, 100% { transform: translateY(1px) translateZ(15px);}
    50% { transform: translateY(-4px) translateZ(22px);}
}

@keyframes knightShine {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes pawnFloat {
    0%, 100% { transform: translateY(0) translateZ(10px);}
    50% { transform: translateY(-5px) translateZ(13px);}
}

/* Info Panels */
.glass-info {
    margin-top: 20px;
    background: rgba(255, 200, 190,0.18);
    box-shadow: 0 0 20px #ff6a5e80;
    border-radius: 24px;
    padding: 20px 30px;
    font-weight: 700;
    color: #ff3f34;
    min-height: 70px;
    user-select: none;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 90, 80, 0.3);
    text-align: center;
}

.status-message {
    margin-top: 15px;
    font-size: 1.25rem;
    color: #ff3b2e;
    text-shadow: 0 0 5px #ff493fcc;
    font-weight: 900;
}

.drag-instructions {
    margin: 24px auto;
    padding: 14px 24px;
    max-width: 500px;
    border-radius: 22px;
    background: rgba(255, 145, 135, 0.22);
    box-shadow: 0 0 26px 6px rgba(255,88,80,0.38);
    color: #ff5649;
    font-weight: 600;
    text-align: center;
}

/* Buttons*/
.stButton > button {
    background: linear-gradient(135deg, #ff503fdd, #d3212bbd);
    border: none !important;
    border-radius: 26px !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 14px 28px !important;
    color: #ffe2db !important;
    box-shadow: 0 0 28px 6px #ff493fcc;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ff725bdd, #e43d3dbd);
    box-shadow: 0 0 38px 12px #ff5a48ed !important;
    transform: translateY(-3px) scale(1.1);
}

/* Scrollbars on history */
.move-history {
    max-height: 320px;
    overflow-y: auto;
    background: rgba(255, 180, 170, 0.15);
    border-radius: 20px;
    border: 1px solid #ff675f66;
    box-shadow: 0 0 22px 6px #ff5b5544 inset;
    padding: 15px 25px;
    font-weight: 600;
    color: #ff5a48cc;
    user-select:none;
}

.move-history::-webkit-scrollbar {
    width: 8px;
}
.move-history::-webkit-scrollbar-track {
    border-radius: 20px;
    background: rgba(255, 88, 80, 0.2);
}
.move-history::-webkit-scrollbar-thumb {
    background: rgba(255, 120, 110, 0.7);
    border-radius: 20px;
}
.move-history::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 160, 145, 0.85);
}

</style>
""", unsafe_allow_html=True)


def init_game():
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
    if "waiting" not in st.session_state:
        st.session_state.waiting = False
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "intermediate"
    if "show_hints" not in st.session_state:
        st.session_state.show_hints = True
    if "ai_thinking" not in st.session_state:
        st.session_state.ai_thinking = False


def get_player_color():
    if st.session_state.room_code:
        return "white" if st.session_state.waiting else "black"
    return "white"


def is_player_turn():
    if st.session_state.game_mode == "single":
        return True
    return get_player_color() == ("white" if st.session_state.board.turn else "black")


def make_move(move):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in st.session_state.board.legal_moves:
            st.session_state.board.push(chess_move)
            st.experimental_rerun()
            return True
        else:
            st.error("Invalid move")
            return False
    except:
        st.error("Invalid move format")
        return False


def save_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        state = {
            "fen": st.session_state.board.fen(),
            "history": st.session_state.move_history,
            "last_update": time.time()
        }
        fpath = f"game_{st.session_state.room_code}.json"
        with open(fpath, "w") as f:
            json.dump(state, f)


def load_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        fpath = f"game_{st.session_state.room_code}.json"
        if os.path.exists(fpath):
            with open(fpath, "r") as f:
                state = json.load(f)
            st.session_state.board = chess.Board(state["fen"])
            st.session_state.move_history = state.get("history", [])


def display_board():
    board = st.session_state.board
    selected = st.session_state.get("selected_square", None)
    valid_moves = st.session_state.get("valid_moves", [])

    cols = st.columns(8, gap="small")
    for r in range(7, -1, -1):
        for c in range(8):
            sq = chess.square(c, r)
            piece = board.piece_at(sq)
            is_light = (r + c) % 2 == 0
            classes = ["square", "light" if is_light else "dark"]
            if sq == selected:
                classes.append("selected")
            elif any(m.to_square == sq for m in valid_moves):
                classes.append("move")

            piece_unicode = ""
            piece_cls = ""
            if piece:
                unicode_map = {
                    'P': "♙", 'N': "♘", 'B': "♗", 'R': "♖", 'Q': "♕", 'K': "♔",
                    'p': "♟", 'n': "♞", 'b': "♝", 'r': "♜", 'q': "♛", 'k': "♚"
                }
                piece_unicode = unicode_map[piece.symbol()]
                piece_cls = "piece-" + piece.symbol().lower()

            with st.container():
                btn_pressed = st.button(piece_unicode or " ", key=f"square_{sq}")
                if btn_pressed:
                    handle_click(sq)
                st.markdown(
                    f"""
                    <style>
                    div.stButton > button[key="square_{sq}"] {{
                        width: 80px; height: 80px;
                        font-size: 3.8rem; line-height: 75px;
                        text-align: center;
                        color: {'#ff4a40' if piece else '#801a1a'};
                        border-radius: 16px;
                        background-color: {'#ff5c58dd' if sq == selected else '#ffe4e3dd' if is_light else '#5a1511cc'};
                        user-select: none;
                        transition: all 0.2s ease;
                        box-shadow: 0 0 10px #ff4a4080;
                    }}
                    div.stButton > button[key="square_{sq}"]:hover {{
                        box-shadow: 0 0 24px 10px #ff5c5800;
                        transform: scale(1.1) translateZ(8px);
                    }}

                    .{piece_cls} {{
                        animation-duration: 4s;
                        animation-iteration-count: infinite;
                        animation-timing-function: ease-in-out;
                    }}
                    .piece-k{{ animation-name: kingFloat }}
                    .piece-q{{ animation-name: queenPulse }}
                    .piece-r{{ animation-name: rookBounce }}
                    .piece-b{{ animation-name: bishopWave }}
                    .piece-n{{ animation-name: knightShine }}
                    .piece-p{{ animation-name: pawnFloat }}

                    @keyframes kingFloat {{0%,100%{{transform:translateY(2px) translateZ(10px) scale(1)}} 50%{{transform:translateY(-6px) translateZ(20px) scale(1.08)}}}}
                    @keyframes queenPulse {{0%,100%{{opacity:0.85}} 50%{{opacity:1}}}}
                    @keyframes rookBounce {{0%,100%{{transform:translateY(0) translateZ(10px)}} 50%{{transform:translateY(-3px) translateZ(18px)}}}}
                    @keyframes bishopWave {{0%,100%{{transform:translateY(1px) translateZ(15px)}} 50%{{transform:translateY(-4px) translateZ(22px)}}}}
                    @keyframes knightShine {{0%,100%{{opacity:1}} 50%{{opacity:0.7}}}}
                    @keyframes pawnFloat {{0%,100%{{transform:translateY(0) translateZ(10px)}} 50%{{transform:translateY(-6px) translateZ(13px)}}}}
                    </style>
                    """, unsafe_allow_html=True
                )


def handle_click(square):
    if not is_player_turn():
        return
    if st.session_state.selected_square is None:
        piece = st.session_state.board.piece_at(square)
        if piece and piece.color == st.session_state.board.turn:
            st.session_state.selected_square = square
            st.session_state.valid_moves = [mv for mv in st.session_state.board.legal_moves if mv.from_square == square]
    else:
        move = chess.Move(st.session_state.selected_square, square)
        piece = st.session_state.board.piece_at(st.session_state.selected_square)
        if piece and piece.piece_type == chess.PAWN:
            rank = 7 if piece.color else 0
            if chess.square_rank(square) == rank:
                move = chess.Move(st.session_state.selected_square, square, promotion=chess.QUEEN)
        if move in st.session_state.board.legal_moves:
            if make_move(move.uci()):
                if st.session_state.game_mode == "multiplayer":
                    save_state()
                st.experimental_rerun()
        else:
            if piece and piece.color == st.session_state.board.turn:
                st.session_state.selected_square = square
                st.session_state.valid_moves = [mv for mv in st.session_state.board.legal_moves if mv.from_square == square]
            else:
                st.session_state.selected_square = None
                st.experimental_rerun()


def main():
    init_game()

    # Multiplayer state loading
    if st.session_state.game_mode == "multiplayer":
        load_state()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<div class="glass-title">💎 Glass Chess 3D - Luxurious Red</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-subtitle">Realistic, animated 3D virtual chess with multiplayer</div>', unsafe_allow_html=True)

    # Multiplayer lobby & info
    if st.session_state.game_mode == "multiplayer":
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown(f"**Room Code:** `{st.session_state.room_code}`")
        st.markdown(f"**You Are:** {get_player_color().title()}")
        if st.session_state.waiting:
            st.markdown("⏳ Waiting for opponent to join. Share the room code!")
        else:
            if is_player_turn():
                st.markdown("✅ Your turn")
            else:
                st.markdown("⏳ Opponent's turn, please wait...")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Single Player"):
                st.session_state.game_mode = "single"
                st.session_state.room_code = None
                st.session_state.waiting = False
                st.experimental_rerun()
        with col2:
            if st.button("Refresh Game"):
                load_state()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Multiplayer Game"):
                room_code = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 6)
                st.session_state.room_code = "".join(room_code)
                st.session_state.game_mode = "multiplayer"
                st.session_state.waiting = True
                st.experimental_rerun()
        with col2:
            code = st.text_input("Join Multiplayer Game via Room Code", max_chars=6)
            if st.button("Join Multiplayer Game"):
                if len(code) == 6:
                    st.session_state.room_code = code.upper()
                    st.session_state.game_mode = "multiplayer"
                    st.session_state.waiting = False
                    load_state()
                    st.experimental_rerun()
                else:
                    st.error("Invalid room code")
        st.markdown('</div>', unsafe_allow_html=True)

    display_board()

    status, msg = get_game_status(st.session_state.board)
    st.markdown(f'<div class="status-message">{msg}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("New Game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.selected_square = None
            st.session_state.valid_moves = []
            st.experimental_rerun()
    with col2:
        if st.button("Undo Move"):
            if len(st.session_state.board.move_stack) > 0:
                st.session_state.board.pop()
                if st.session_state.move_history:
                    st.session_state.move_history.pop()
                st.experimental_rerun()
    with col3:
        if st.button("Random Move"):
            moves = list(st.session_state.board.legal_moves)
            if moves:
                make_move(random.choice(moves).uci())
                st.experimental_rerun()
    with col4:
        if st.button("Copy FEN"):
            st.code(st.session_state.board.fen())

    st.markdown("""
    <div class="drag-instructions">
        Click the piece you want to move, then click the square to move it.
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__=="__main__":
    main()
