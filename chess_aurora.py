# Glassy Chess – Streamlit + python-chess
# Run: pip install streamlit python-chess
# Start: streamlit run app.py

import streamlit as st
import chess
from dataclasses import dataclass

st.set_page_config(page_title="Glassy Chess", layout="wide")

# ---------- Styles (Glassy Blue Theme) ----------
GLASSY_CSS = """
<style>
/* Page background */
[data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 800px at 15% 10%, rgba(20,60,120,0.45), rgba(10,20,40,0.85)),
              linear-gradient(135deg, #0a1931 0%, #0f3057 50%, #1a508b 100%);
}

/***** Board container as frosted glass *****/
.chess-wrap {
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.14);
  box-shadow: 0 10px 40px rgba(0,0,0,0.35), inset 0 0 40px rgba(90,150,255,0.08);
  border-radius: 24px;
  padding: 14px 14px 8px 14px;
}

/***** Global button styling to mimic glass squares *****/
.stButton > button {
  width: 100% !important;
  aspect-ratio: 1 / 1;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(200,220,255,0.10), rgba(120,160,255,0.06));
  border: 1px solid rgba(180,200,255,0.25);
  box-shadow: inset 0 0 10px rgba(120,160,255,0.15), 0 6px 18px rgba(0,0,0,0.26);
  color: #d9e6ff;
  text-shadow: 0 0 10px rgba(120,180,255,0.6), 0 0 2px rgba(255,255,255,0.6);
  transition: transform 120ms ease, box-shadow 200ms ease, background 200ms ease;
  font-size: 28px;
  font-weight: 600;
}
.stButton > button:hover {
  transform: scale(1.03);
  box-shadow: inset 0 0 18px rgba(120,180,255,0.35), 0 10px 26px rgba(20,40,90,0.55);
}

/* Selected & valid-move pseudo-highlights via aria-label markers */
button[data-selected="true"] {
  outline: 2px solid rgba(120,200,255,0.95) !important;
  box-shadow: 0 0 20px rgba(120,200,255,0.75), inset 0 0 18px rgba(120,200,255,0.25) !important;
}
button[data-valid="true"] {
  outline: 2px solid rgba(0,230,255,0.85) !important;
  box-shadow: 0 0 28px rgba(0,230,255,0.55), inset 0 0 16px rgba(0,230,255,0.18) !important;
}

/* Header/info chips */
.info-chip {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.22);
  color: #d9e6ff;
  font-size: 12px;
  margin-right: 8px;
}

/* Tutor hint bubble (positioned near the board header) */
.hint-bubble {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 14px;
  background: rgba(0, 225, 255, 0.12);
  border: 1px solid rgba(0, 225, 255, 0.35);
  color: #bfefff;
  animation: floaty 3s ease-in-out infinite;
}
@keyframes floaty {
  0%,100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

/* Board rank/file labels */
.coord {
  color: rgba(210,230,255,0.75);
  font-size: 13px; font-weight: 600; text-align: center;
  text-shadow: 0 0 6px rgba(120,160,255,0.55);
}
</style>
"""

st.markdown(GLASSY_CSS, unsafe_allow_html=True)

# ---------- Session State ----------
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "selected" not in st.session_state:
    st.session_state.selected = None  # chess.SQUARE or None
if "valid_targets" not in st.session_state:
    st.session_state.valid_targets = set()
if "history" not in st.session_state:
    st.session_state.history = []  # list[chess.Move]
if "orientation_white" not in st.session_state:
    st.session_state.orientation_white = True
if "tutor" not in st.session_state:
    st.session_state.tutor = False

# ---------- Utility ----------
PIECE_UNICODE = {
    chess.PAWN: {True: "♙", False: "♟"},
    chess.KNIGHT: {True: "♘", False: "♞"},
    chess.BISHOP: {True: "♗", False: "♝"},
    chess.ROOK: {True: "♖", False: "♜"},
    chess.QUEEN: {True: "♕", False: "♛"},
    chess.KING: {True: "♔", False: "♚"},
}

def piece_symbol(piece: chess.Piece | None) -> str:
    if not piece:
        return ""
    return PIECE_UNICODE[piece.piece_type][piece.color]

# Simple static evaluation (material + mobility + center control)
VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
CENTER = {chess.D4, chess.E4, chess.D5, chess.E5}

def evaluate(board: chess.Board) -> int:
    score = 0
    # Material
    for pt, val in VALUES.items():
        score += len(board.pieces(pt, chess.WHITE)) * val
        score -= len(board.pieces(pt, chess.BLACK)) * val
    # Mobility (legal moves count)
    score += (len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves))) * 2
    # Center control
    for sq in CENTER:
        attackers_w = board.attackers(chess.WHITE, sq)
        attackers_b = board.attackers(chess.BLACK, sq)
        score += (len(attackers_w) - len(attackers_b)) * 5
    # King safety (very rough: prefer castling rights)
    if board.has_kingside_castling_rights(chess.WHITE): score += 10
    if board.has_queenside_castling_rights(chess.WHITE): score += 10
    if board.has_kingside_castling_rights(chess.BLACK): score -= 10
    if board.has_queenside_castling_rights(chess.BLACK): score -= 10
    return score

@dataclass
class TutorSuggestion:
    move: chess.Move | None
    score: int | None


def suggest_move(board: chess.Board) -> TutorSuggestion:
    best_move = None
    best_score = -10**9 if board.turn == chess.WHITE else 10**9
    for mv in board.legal_moves:
        board.push(mv)
        sc = evaluate(board)
        board.pop()
        if board.turn == chess.BLACK:  # We just made a White move
            if sc > best_score:
                best_score = sc
                best_move = mv
        else:  # We just made a Black move
            if sc < best_score:
                best_score = sc
                best_move = mv
    return TutorSuggestion(best_move, best_score if best_move else None)

# Compute valid targets for selected square

def recompute_valid_targets():
    st.session_state.valid_targets = set()
    if st.session_state.selected is None:
        return
    for mv in st.session_state.board.legal_moves:
        if mv.from_square == st.session_state.selected:
            st.session_state.valid_targets.add(mv.to_square)

# Handle square click

def on_square_clicked(sq: chess.Square):
    b = st.session_state.board
    sel = st.session_state.selected
    if sel is None:
        # Select your own color piece only
        pc = b.piece_at(sq)
        if pc and pc.color == b.turn:
            st.session_state.selected = sq
            recompute_valid_targets()
        else:
            # ignore clicks on empty or opponent pieces as first click
            return
    else:
        # If clicking same color piece -> reselect
        pc = b.piece_at(sq)
        if pc and pc.color == b.turn and sq != sel:
            st.session_state.selected = sq
            recompute_valid_targets()
            return
        # Try to move if it's a valid target
        if sq in st.session_state.valid_targets:
            mv = chess.Move(sel, sq)
            # Promote automatically to queen on last rank (quick UX)
            if chess.square_rank(sq) in (7, 0) and b.piece_at(sel) and b.piece_at(sel).piece_type == chess.PAWN:
                mv = chess.Move.from_uci(chess.Move(sel, sq).uci() + 'q')
            if mv in b.legal_moves:
                st.session_state.history.append(mv)
                b.push(mv)
            # clear selection
            st.session_state.selected = None
            st.session_state.valid_targets = set()
        else:
            # clicked somewhere else -> clear selection
            st.session_state.selected = None
            st.session_state.valid_targets = set()

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.markdown("## ♟️ Controls")
    if st.button("♻️ New Game"):
        st.session_state.board = chess.Board()
        st.session_state.history = []
        st.session_state.selected = None
        st.session_state.valid_targets = set()
    if st.button("↩️ Undo"):
        if st.session_state.board.move_stack:
            st.session_state.board.pop()
            if st.session_state.history:
                st.session_state.history.pop()
        st.session_state.selected = None
        st.session_state.valid_targets = set()

    st.session_state.orientation_white = st.toggle("White at bottom", value=st.session_state.orientation_white)
    st.session_state.tutor = st.toggle("Tutor mode (heuristic)", value=st.session_state.tutor)
    show_coords = st.toggle("Show coordinates", value=True)

# ---------- Top Info Bar ----------
turn_text = "White to move" if st.session_state.board.turn else "Black to move"
colL, colM = st.columns([1,3])
with colL:
    st.markdown(f"<span class='info-chip'>⏳ {turn_text}</span>" , unsafe_allow_html=True)
    st.markdown(f"<span class='info-chip'>Moves: {len(st.session_state.history)}</span>", unsafe_allow_html=True)

with colM:
    if st.session_state.tutor and not st.session_state.board.is_game_over():
        sug = suggest_move(st.session_state.board)
        san = st.session_state.board.san(sug.move) if sug.move else ""
        st.markdown(f"<span class='hint-bubble'>💡 Tutor suggests: <b>{san}</b></span>", unsafe_allow_html=True)

st.markdown("<div class='chess-wrap'>", unsafe_allow_html=True)

# ---------- Board Rendering ----------
files = range(8)
ranks = range(8)

# Orientation
if st.session_state.orientation_white:
    ranks_iter = reversed(ranks)  # 7..0 displayed top->bottom as 8..1
    files_iter = files            # 0..7 (a..h) left->right
else:
    ranks_iter = ranks
    files_iter = reversed(files)

# Coordinates row (files)
if show_coords:
    cols = st.columns(9, gap="small")
    cols[0].markdown("&nbsp;")
    for i, f in enumerate(files_iter):
        file_char = chr(ord('a') + (f if st.session_state.orientation_white else 7 - f))
        cols[i+1].markdown(f"<div class='coord'>{file_char}</div>", unsafe_allow_html=True)

# 8x8 grid
for r in ranks_iter:
    cols = st.columns(9, gap="small") if show_coords else st.columns(8, gap="small")
    # Rank label
    if show_coords:
        rank_char = str(r+1) if st.session_state.orientation_white else str(8 - r)
        cols[0].markdown(f"<div class='coord'>{rank_char}</div>", unsafe_allow_html=True)
    for i, f in enumerate(files_iter):
        # Map to python-chess square index
        # chess.square(file, rank) expects 0-based a-file and 0-based rank (a1 -> (0,0))
        sq = chess.square(f, r)
        piece = st.session_state.board.piece_at(sq)
        label = piece_symbol(piece) if piece else ""

        selected = (st.session_state.selected == sq)
        valid = (sq in st.session_state.valid_targets)

        # Using empty markdown to inject attributes on next button by JS is complex in Streamlit.
        # Instead, we hint selection/validity by appending subtle markers to the label.
        mark = ""
        if selected:
            mark = " ⦿"
        elif valid:
            mark = " ·"

        # Render each square as a button
        with cols[(i+1) if show_coords else i]:
            clicked = st.button(label + mark, key=f"sq_{sq}")
            if clicked:
                on_square_clicked(sq)

# Game state message
if st.session_state.board.is_game_over():
    res = st.session_state.board.result()
    msg = "Draw"
    if res == "1-0":
        msg = "White wins"
    elif res == "0-1":
        msg = "Black wins"
    st.success(f"Game over – {msg} ({res})")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FEN / PGN Export ----------
col1, col2 = st.columns(2)
with col1:
    st.text_input("FEN", value=st.session_state.board.fen(), key="fen_field")
with col2:
    import chess.pgn
    game = chess.pgn.Game()
    node = game
    btemp = chess.Board()
    for mv in st.session_state.history:
        node = node.add_variation(mv)
        btemp.push(mv)
    pgn_str = str(game)
    st.text_area("PGN", value=pgn_str, height=120)

# ---------- Notes ----------
st.caption(
    "Tips: Click a piece to highlight valid moves (marked with ·). Click a highlighted square to move. "
    "Toggle Tutor mode in the sidebar for heuristic suggestions. Use Undo or start a New Game anytime."
)
