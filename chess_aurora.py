import streamlit as st
import chess

st.set_page_config(page_title="💎 Glass Chess Improved", page_icon="💎", layout="wide")

# Glassy blue CSS for board, squares, and pieces
st.markdown("""
<style>
body, .stApp {
  background: linear-gradient(135deg, #0a1227 0%, #152a70 50%, #0a1b5e 100%);
  color: #e0eaff;
  font-family: 'SF Mono', monospace;
  user-select: none;
}
.glass-container {
  max-width: 850px;
  margin: 2rem auto;
  padding: 36px 24px;
  background: rgba(20,40,80,0.17);
  border-radius: 32px;
  box-shadow: 0 8px 40px rgba(0,90,255,0.5);
  backdrop-filter: blur(34px);
  -webkit-backdrop-filter: blur(34px);
}
.glass-title {
  text-align: center;
  font-size: 3rem;
  font-weight: 900;
  color: #a0d8ff;
  text-shadow: 0 0 20px rgba(64, 160, 255, 0.8);
  margin-bottom: 14px;
}
.glass-subtitle {
  text-align: center;
  font-size: 1.15rem;
  font-weight: 500;
  margin-bottom: 36px;
  color: #cce7ff;
  text-shadow: 0 0 10px rgba(64, 160, 255, 0.4);
}
.chess-board-container {
  display: grid;
  grid-template-columns: repeat(8, 68px);
  grid-template-rows: repeat(8, 68px);
  gap: 7px;
  justify-content: center;
  user-select: none;
}
.chess-square-button {
  border-radius: 14px;
  border: 2px solid rgba(64,160,255,0.22);
  background: rgba(64,156,255,0.10);
  color: rgba(230,245,255,0.85);
  font-size: 2.8rem;
  font-weight: 900;
  font-family: 'SF Mono', monospace;
  box-shadow:
    inset 0 0 12px rgba(64,180,255,0.22),
    0 0 12px rgba(64,160,255,0.30);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  text-shadow: 0 0 6px rgba(64,200,255,0.7);
  user-select: none;
  transition: all 0.16s cubic-bezier(0.4, 0, 0.2, 1);
}
.chess-square-button:hover {
  color: #bbe7ff;
  box-shadow:
    inset 0 0 20px rgba(64,210,255,0.28),
    0 0 25px rgba(64,210,255,0.7);
  transform: scale(1.10);
  z-index: 10;
}
/* highlight selected piece */
.chess-square-button.selected {
  background: rgba(0,145,255,0.33) !important;
  box-shadow:
    0 0 30px rgba(0,145,255,0.6),
    inset 0 0 22px rgba(64,200,255,0.27);
  color: #ddf7ff !important;
}
/* highlight valid moves */
.chess-square-button.valid-move {
  background: rgba(0,185,255,0.28) !important;
  box-shadow: 0 0 20px rgba(0,185,255,0.39);
  color: #ffffff !important;
}
.chess-square-button.capture-move {
  background: rgba(0,155,255,0.20) !important;
  border: 2px solid #ff2345 !important;
  box-shadow: 0 0 23px rgba(255, 61, 77, 0.29);
  color: #ffdee0 !important;
}
.chess-square-button.last-move {
  border: 2px solid #fff688 !important;
}
.chess-square-button.promotion-move {
  border: 2px dashed #a0eaff !important;
}
.tutor-hint {
  position: absolute;
  top: -28px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(64,156,255,0.9);
  color: #00152d;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 700;
  white-space: nowrap;
  pointer-events: none;
  box-shadow: 0 0 20px rgba(64, 156, 255, 0.8);
  user-select: none;
  animation: hintFloat 2.5s ease-in-out infinite;
  z-index: 99;
}
@keyframes hintFloat {
  0%,100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(-6px); }
}
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    # Add support for storing last move for highlighting
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'last_move' not in st.session_state:
        st.session_state.last_move = None
    if 'promotion_piece' not in st.session_state:
        st.session_state.promotion_piece = chess.QUEEN

def get_tutor_hint(board, selected_square):
    if selected_square is None:
        return None
    piece = board.piece_at(selected_square)
    if not piece or piece.color != board.turn:
        return None
    moves = [m for m in board.legal_moves if m.from_square == selected_square]
    if not moves:
        return None
    return f"Best move: {board.san(moves[0])}"

def display_board(board):
    selected_square = st.session_state.get('selected_square')
    valid_moves = st.session_state.get('valid_moves', [])
    last_move = st.session_state.get('last_move')

    symbols = {
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
    }

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)
    for rank in range(7, -1, -1):
        for file in range(8):
            square = rank * 8 + file
            piece = board.piece_at(square)
            symbol = symbols.get(piece.symbol(), "") if piece else ""
            classes = ["chess-square-button"]

            if square == selected_square:
                classes.append("selected")
            # Highlight valid moves including promotions/captures
            elif any(move.to_square == square for move in valid_moves):
                move_obj = next((move for move in valid_moves if move.to_square == square), None)
                if move_obj:
                    # Promotion (last rank for pawn)
                    if move_obj.promotion:
                        classes.append("promotion-move")
                    # Capture
                    elif board.is_capture(move_obj):
                        classes.append("capture-move")
                    else:
                        classes.append("valid-move")
                else:
                    classes.append("valid-move")
            # Last moved squares (source and destination)
            if last_move:
                if square == last_move.from_square or square == last_move.to_square:
                    classes.append("last-move")

            # Tutor hint only for selected piece
            tutor_hint = ""
            if selected_square == square:
                hint = get_tutor_hint(board, selected_square)
                if hint:
                    tutor_hint = f'<div class="tutor-hint">{hint}</div>'

            st.markdown(f"""
            <div style="position: relative;">
                <button class="{' '.join(classes)}"
                  onclick="handleChessClick({square})"
                  title="{chr(97+file)}{rank+1}" aria-label="Square {chr(97+file)}{rank+1}">
                  {symbol or "&nbsp;"}
                </button>
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
        const event = new CustomEvent('chessSquareClick', {detail: {square:square}});
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def select_square(square):
    piece = st.session_state.board.piece_at(square)
    if piece and piece.color == st.session_state.board.turn:
        # Show only legal moves for that piece
        valid_moves = [m for m in st.session_state.board.legal_moves if m.from_square == square]
        st.session_state.selected_square = square
        st.session_state.valid_moves = valid_moves
    else:
        st.session_state.selected_square = None
        st.session_state.valid_moves = []

def make_move(from_sq, to_sq, promotion_piece=None):
    legal_moves = list(st.session_state.board.legal_moves)
    move = None
    # Promotion: detect moving pawn to last rank
    for candidate in legal_moves:
        if candidate.from_square == from_sq and candidate.to_square == to_sq:
            move = candidate
            break
    if move:
        # Handle promotion by default to Queen (can add UI popup for choice)
        if move.promotion is not None and promotion_piece is not None:
            move = chess.Move(from_sq, to_sq, promotion=promotion_piece)
        st.session_state.board.push(move)
        st.session_state.selected_square = None
        st.session_state.valid_moves = []
        st.session_state.last_move = move
        return True
    return False

def handle_click():
    param = st.experimental_get_query_params()
    if "chess_square_click" in param:
        try:
            clicked = int(param["chess_square_click"][0])
            selected = st.session_state.get('selected_square')
            # If a piece is not selected, select one if possible
            if selected is None:
                select_square(clicked)
            else:
                piece = st.session_state.board.piece_at(selected)
                is_pawn_promotion = piece and piece.piece_type == chess.PAWN and ((piece.color and clicked // 8 == 7) or (not piece.color and clicked // 8 == 0))
                if is_pawn_promotion:
                    promoted = chess.QUEEN  # Default; UI for choosing can be added
                else:
                    promoted = None
                if make_move(selected, clicked, promoted):
                    st.experimental_rerun()
                else:
                    select_square(clicked)
        except Exception:
            pass

def main():
    init_chess_game()
    handle_click()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 Glass Chess Improved 💎</h1>', unsafe_allow_html=True)
    st.markdown('<div class="glass-subtitle">Click a piece to select, then a destination to move. Valid moves glow. Tutor hint shown for selection.</div>', unsafe_allow_html=True)
    display_board(st.session_state.board)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
