# Glassy Chess – Streamlit Multiplayer (Room Codes) + python-chess
# Run: pip install streamlit python-chess
# Start: streamlit run app.py
# Notes:
# - Multiplayer works by saving room state to files under ./rooms on the server.
#   Anyone who opens the same deployed app and enters the same ROOM CODE will join the same game.
# - Creator becomes White; next joiner becomes Black; others are spectators.
# - Optional Auto‑Sync re-runs the app every 2 seconds for near real-time play.

import os, json, time, secrets, string
from dataclasses import dataclass
from typing import Optional

import streamlit as st
import chess
import chess.pgn

st.set_page_config(page_title="Glassy Chess – Obsidian Blue", layout="wide")

ROOMS_DIR = "rooms"
os.makedirs(ROOMS_DIR, exist_ok=True)

# ---------- Styles (Obsidian Blue Luxury Theme) ----------
GLASSY_CSS = """
<style>
/* Deep obsidian blue aurora background */
[data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 750px at 15% 10%, rgba(17,36,80,0.55), rgba(8,16,32,0.95)),
              conic-gradient(from 210deg at 75% 20%, rgba(0,180,255,0.12), rgba(0,0,0,0) 20%),
              linear-gradient(135deg, #050B16 0%, #081122 45%, #0B1C37 100%);
}

/***** Board container as frosted glass *****/
.chess-wrap {
  backdrop-filter: blur(18px) saturate(120%);
  -webkit-backdrop-filter: blur(18px) saturate(120%);
  background: rgba(12, 24, 48, 0.45);
  border: 1px solid rgba(180, 220, 255, 0.15);
  box-shadow: 0 18px 60px rgba(0,0,0,0.45), inset 0 0 60px rgba(120,180,255,0.07);
  border-radius: 28px;
  padding: 16px 16px 10px 16px;
}

/* Headline */
.h1 {font-size: 34px; font-weight: 800; letter-spacing: 0.3px; color: #E9F3FF;
  text-shadow: 0 0 24px rgba(0,220,255,0.35);
}
.subtle { color: rgba(220,235,255,0.8); }

/* Neumorphic luxe buttons (squares) */
.stButton > button {
  width: 100% !important; aspect-ratio: 1 / 1; border-radius: 16px;
  background: linear-gradient(180deg, rgba(200,230,255,0.10), rgba(110,160,255,0.06));
  border: 1px solid rgba(170,210,255,0.22);
  box-shadow: inset 0 0 18px rgba(120,170,255,0.18), 0 10px 26px rgba(4,10,22,0.55);
  color: #E4F0FF; font-size: 30px; font-weight: 700;
  text-shadow: 0 0 14px rgba(120,200,255,0.65), 0 0 2px rgba(255,255,255,0.7);
  transition: transform 120ms ease, box-shadow 220ms ease, background 220ms ease, filter 220ms ease;
}
.stButton > button:hover { transform: scale(1.035);
  filter: drop-shadow(0 0 18px rgba(0,220,255,0.25)); }

/* Selection & valid move halos */
button[data-selected="true"], .sq-selected button {
  outline: 2px solid rgba(120,220,255,0.95) !important;
  box-shadow: 0 0 26px rgba(120,220,255,0.75), inset 0 0 20px rgba(120,220,255,0.25) !important;
}
button[data-valid="true"], .sq-valid button {
  outline: 2px solid rgba(0,240,255,0.85) !important;
  box-shadow: 0 0 34px rgba(0,240,255,0.55), inset 0 0 18px rgba(0,240,255,0.18) !important;
}

/* Chips & hint bubble */
.info-chip {display:inline-block;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.22);color:#d9e6ff;font-size:12px;margin-right:8px}
.hint-bubble{display:inline-block;padding:9px 12px;border-radius:14px;background:rgba(0,225,255,0.10);
  border:1px solid rgba(0,225,255,0.35);color:#bfefff;animation:floaty 3s ease-in-out infinite}
@keyframes floaty {0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)}}
.coord { color: rgba(210,230,255,0.82); font-size: 13px; font-weight: 700; text-align:center;
  text-shadow: 0 0 6px rgba(120,160,255,0.55); }
</style>
"""

st.markdown(GLASSY_CSS, unsafe_allow_html=True)

# ---------- Session ----------
if "client_id" not in st.session_state:
    st.session_state.client_id = secrets.token_hex(8)
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "selected" not in st.session_state:
    st.session_state.selected = None
if "valid_targets" not in st.session_state:
    st.session_state.valid_targets = set()
if "history" not in st.session_state:
    st.session_state.history = []
if "orientation_white" not in st.session_state:
    st.session_state.orientation_white = True
if "tutor" not in st.session_state:
    st.session_state.tutor = False
if "room_code" not in st.session_state:
    st.session_state.room_code = ""
if "role" not in st.session_state:
    st.session_state.role = "solo"  # "white" | "black" | "spectator" | "solo"
if "auto_sync" not in st.session_state:
    st.session_state.auto_sync = False

# ---------- Room Storage Helpers ----------

def _room_path(code: str) -> str:
    return os.path.join(ROOMS_DIR, f"{code}.json")

@dataclass
class Room:
    code: str
    fen: str
    history_uci: list
    white_id: Optional[str]
    black_id: Optional[str]
    updated_at: float

    def save(self):
        with open(_room_path(self.code), "w", encoding="utf-8") as f:
            json.dump({
                "fen": self.fen,
                "history": self.history_uci,
                "white_id": self.white_id,
                "black_id": self.black_id,
                "updated_at": time.time(),
            }, f)


def room_load(code: str) -> Optional[Room]:
    try:
        with open(_room_path(code), "r", encoding="utf-8") as f:
            data = json.load(f)
        return Room(code, data["fen"], data.get("history", []), data.get("white_id"), data.get("black_id"), data.get("updated_at", time.time()))
    except FileNotFoundError:
        return None


def room_create() -> Room:
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(6))
        if not os.path.exists(_room_path(code)):
            break
    b = chess.Board()
    r = Room(code, b.fen(), [], st.session_state.client_id, None, time.time())
    r.save()
    return r


def room_join(code: str) -> Optional[Room]:
    r = room_load(code)
    if not r:
        return None
    # Assign roles if free
    if r.white_id is None:
        r.white_id = st.session_state.client_id
        r.save()
    elif r.black_id is None and r.white_id != st.session_state.client_id:
        r.black_id = st.session_state.client_id
        r.save()
    return r


def room_push_move(r: Room, mv: chess.Move):
    b = chess.Board(r.fen)
    if mv in b.legal_moves:
        b.push(mv)
        r.fen = b.fen()
        r.history_uci.append(mv.uci())
        r.save()

# ---------- Chess Helpers ----------
PIECE_UNICODE = {
    chess.PAWN: {True: "♙", False: "♟"},
    chess.KNIGHT: {True: "♘", False: "♞"},
    chess.BISHOP: {True: "♗", False: "♝"},
    chess.ROOK: {True: "♖", False: "♜"},
    chess.QUEEN: {True: "♕", False: "♛"},
    chess.KING: {True: "♔", False: "♚"},
}

VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
CENTER = {chess.D4, chess.E4, chess.D5, chess.E5}

def piece_symbol(piece: chess.Piece | None) -> str:
    if not piece:
        return ""
    return PIECE_UNICODE[piece.piece_type][piece.color]


def evaluate(board: chess.Board) -> int:
    score = 0
    for pt, val in VALUES.items():
        score += len(board.pieces(pt, chess.WHITE)) * val
        score -= len(board.pieces(pt, chess.BLACK)) * val
    score += (len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves))) * 2
    for sq in CENTER:
        attackers_w = board.attackers(chess.WHITE, sq)
        attackers_b = board.attackers(chess.BLACK, sq)
        score += (len(attackers_w) - len(attackers_b)) * 5
    if board.has_kingside_castling_rights(chess.WHITE): score += 10
    if board.has_queenside_castling_rights(chess.WHITE): score += 10
    if board.has_kingside_castling_rights(chess.BLACK): score -= 10
    if board.has_queenside_castling_rights(chess.BLACK): score -= 10
    return score

@dataclass
class TutorSuggestion:
    move: Optional[chess.Move]
    score: Optional[int]


def suggest_move(board: chess.Board) -> TutorSuggestion:
    if board.is_game_over():
        return TutorSuggestion(None, None)
    best_move = None
    best_score = -10**9 if board.turn == chess.WHITE else 10**9
    for mv in board.legal_moves:
        board.push(mv)
        sc = evaluate(board)
        board.pop()
        if board.turn == chess.BLACK:  # white just moved
            if sc > best_score:
                best_score = sc; best_move = mv
        else:
            if sc < best_score:
                best_score = sc; best_move = mv
    return TutorSuggestion(best_move, best_score if best_move else None)


def recompute_valid_targets(board: chess.Board, selected: Optional[int]):
    targets = set()
    if selected is None:
        return targets
    for mv in board.legal_moves:
        if mv.from_square == selected:
            targets.add(mv.to_square)
    return targets

# ---------- Sidebar: Multiplayer Controls ----------
with st.sidebar:
    st.markdown("<div class='h1'>♟️ Glassy Chess</div>", unsafe_allow_html=True)
    st.caption("Obsidian‑blue, luxurious UI • Multiplayer via room codes • Tutor suggestions")

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("✨ Create Room"):
            r = room_create()
            st.session_state.room_code = r.code
            st.session_state.role = "white"
            st.success(f"Room created: {r.code}. You are White. Share this code to invite.")
    with colB:
        code_in = st.text_input("Join Room (code)", placeholder="e.g. 7K3Q2", value=st.session_state.room_code)
        if st.button("🔗 Join") and code_in:
            r = room_join(code_in.strip().upper())
            if r:
                st.session_state.room_code = r.code
                # decide role
                if r.white_id == st.session_state.client_id:
                    st.session_state.role = "white"
                elif r.black_id == st.session_state.client_id:
                    st.session_state.role = "black"
                elif r.black_id is None:
                    # this branch will not happen because room_join assigns automatically, but keep for safety
                    st.session_state.role = "black"
                else:
                    st.session_state.role = "spectator"
                st.success(f"Joined room {r.code} as {st.session_state.role}.")
            else:
                st.error("Room not found. Check the code.")

    st.session_state.orientation_white = st.toggle("White at bottom", value=st.session_state.orientation_white)
    st.session_state.tutor = st.toggle("Tutor mode (heuristic)", value=st.session_state.tutor)
    st.session_state.auto_sync = st.toggle("Auto‑Sync every 2s", value=st.session_state.auto_sync)

    if st.button("♻️ New Game"):
        if st.session_state.room_code:
            # reset shared room
            r = room_load(st.session_state.room_code)
            if r:
                b = chess.Board()
                r.fen = b.fen()
                r.history_uci = []
                r.save()
        else:
            # local
            st.session_state.board = chess.Board()
            st.session_state.history = []
            st.session_state.selected = None
            st.session_state.valid_targets = set()

    if st.button("↩️ Undo"):
        if st.session_state.room_code:
            r = room_load(st.session_state.room_code)
            if r and r.history_uci:
                b = chess.Board()
                for u in r.history_uci[:-1]:
                    b.push_uci(u)
                r.fen = b.fen()
                r.history_uci = r.history_uci[:-1]
                r.save()
        else:
            b = st.session_state.board
            if b.move_stack:
                b.pop()
                if st.session_state.history:
                    st.session_state.history.pop()
            st.session_state.selected = None
            st.session_state.valid_targets = set()

# ---------- Top Info Bar ----------
if st.session_state.room_code:
    r = room_load(st.session_state.room_code)
    if not r:
        st.error("Room not found (maybe deleted).")
        st.stop()
    # hydrate local board from room
    st.session_state.board = chess.Board(r.fen)
    st.session_state.history = [chess.Move.from_uci(u) for u in r.history_uci]

turn_text = "White to move" if st.session_state.board.turn else "Black to move"
role = st.session_state.role
left, right = st.columns([2,3])
with left:
    st.markdown(f"<span class='info-chip'>⏳ {turn_text}</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='info-chip'>Moves: {len(st.session_state.history)}</span>", unsafe_allow_html=True)
    if st.session_state.room_code:
        st.markdown(f"<span class='info-chip'>Room: <b>{st.session_state.room_code}</b></span>", unsafe_allow_html=True)
        st.markdown(f"<span class='info-chip'>You are: <b>{role}</b></span>", unsafe_allow_html=True)
with right:
    if st.session_state.tutor and not st.session_state.board.is_game_over():
        sug = suggest_move(st.session_state.board)
        san = st.session_state.board.san(sug.move) if sug.move else ""
        st.markdown(f"<span class='hint-bubble'>💡 Tutor suggests: <b>{san}</b></span>", unsafe_allow_html=True)

st.markdown("<div class='chess-wrap'>", unsafe_allow_html=True)

# ---------- Board Rendering ----------
files = range(8); ranks = range(8)
if st.session_state.orientation_white:
    ranks_iter = reversed(ranks); files_iter = files
else:
    ranks_iter = ranks; files_iter = reversed(files)

show_coords = True
if show_coords:
    cols = st.columns(9, gap="small"); cols[0].markdown("&nbsp;")
    for i, f in enumerate(files_iter):
        file_char = chr(ord('a') + (f if st.session_state.orientation_white else 7 - f))
        cols[i+1].markdown(f"<div class='coord'>{file_char}</div>", unsafe_allow_html=True)

# Permissions: who can move?
can_move = True
if st.session_state.room_code:
    # Only the side to move with matching role can act
    to_move_is_white = st.session_state.board.turn
    if role == "white":
        can_move = to_move_is_white
    elif role == "black":
        can_move = not to_move_is_white
    else:
        can_move = False

selected = st.session_state.selected
valid_targets = recompute_valid_targets(st.session_state.board, selected)

for r in ranks_iter:
    cols = st.columns(9, gap="small") if show_coords else st.columns(8, gap="small")
    if show_coords:
        rank_char = str(r+1) if st.session_state.orientation_white else str(8 - r)
        cols[0].markdown(f"<div class='coord'>{rank_char}</div>", unsafe_allow_html=True)
    for i, f in enumerate(files_iter):
        sq = chess.square(f, r)
        piece = st.session_state.board.piece_at(sq)
        label = piece_symbol(piece) if piece else ""
        is_sel = (selected == sq)
        is_valid = (sq in valid_targets)
        mark = " ⦿" if is_sel else (" ·" if is_valid else "")
        with cols[(i+1) if show_coords else i]:
            clicked = st.button(label + mark, key=f"sq_{sq}")
            if clicked and can_move:
                # selection logic
                b = st.session_state.board
                if selected is None:
                    pc = b.piece_at(sq)
                    if pc and pc.color == b.turn:
                        st.session_state.selected = sq
                else:
                    pc = b.piece_at(sq)
                    if pc and pc.color == b.turn and sq != selected:
                        st.session_state.selected = sq
                    else:
                        mv = chess.Move(selected, sq)
                        # auto-queen promotion
                        if chess.square_rank(sq) in (7, 0) and b.piece_at(selected) and b.piece_at(selected).piece_type == chess.PAWN:
                            mv = chess.Move.from_uci(mv.uci() + 'q')
                        if mv in b.legal_moves:
                            if st.session_state.room_code:
                                rr = room_load(st.session_state.room_code)
                                if rr:
                                    room_push_move(rr, mv)
                                    # pull back synced state
                                    rr = room_load(st.session_state.room_code)
                                    st.session_state.board = chess.Board(rr.fen)
                                    st.session_state.history = [chess.Move.from_uci(u) for u in rr.history_uci]
                            else:
                                st.session_state.history.append(mv)
                                b.push(mv)
                        st.session_state.selected = None

# Game state message
if st.session_state.board.is_game_over():
    res = st.session_state.board.result()
    msg = "Draw"
    if res == "1-0": msg = "White wins"
    elif res == "0-1": msg = "Black wins"
    st.success(f"Game over – {msg} ({res})")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FEN / PGN Export ----------
col1, col2 = st.columns(2)
with col1:
    st.text_input("FEN", value=st.session_state.board.fen(), key="fen_field")
with col2:
    game = chess.pgn.Game(); node = game; btemp = chess.Board()
    for mv in st.session_state.history:
        node = node.add_variation(mv); btemp.push(mv)
    st.text_area("PGN", value=str(game), height=120)

# ---------- Sync Controls ----------
colx, coly = st.columns([1,1])
with colx:
    if st.button("🔄 Manual Sync"):
        if st.session_state.room_code:
            rr = room_load(st.session_state.room_code)
            if rr:
                st.session_state.board = chess.Board(rr.fen)
                st.session_state.history = [chess.Move.from_uci(u) for u in rr.history_uci]
        st.experimental_rerun()
with coly:
    if st.session_state.auto_sync and st.session_state.room_code:
        time.sleep(2)
        st.experimental_rerun()

# ---------- Footer Tips ----------
st.caption(
    "Create a room to get a 6‑char code. Share it. The creator is White, the next joiner is Black; others spectate. "
    "Only the side to move can act in multiplayer. Tutor gives quick heuristic hints."
)
