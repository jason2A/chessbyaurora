import streamlit as st
import chess

st.set_page_config(
    page_title="💎 Glass Chess Advanced",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for glassy blue transparent chessboard and pieces with animations
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=SF+Mono&display=swap');

  body, .stApp {
      background: linear-gradient(135deg, #0a1227 0%, #152a70 50%, #0a1b5e 100%);
      color: #e0eaff;
      font-family: 'SF Mono', monospace;
      user-select: none;
      margin: 0; padding: 0;
  }

  .glass-container {
      max-width: 820px; margin: 2rem auto;
      padding: 30px;
      background: rgba(20, 40, 80, 0.15);
      border-radius: 32px;
      box-shadow: 0 8px 40px rgba(0, 90, 255, 0.5);
      backdrop-filter: blur(34px);
      -webkit-backdrop-filter: blur(34px);
  }

  .glass-title {
      text-align: center;
      font-size: 3rem;
      font-weight: 900;
      color: #a0d8ff;
      text-shadow: 0 0 20px rgba(64, 160, 255, 0.75);
      margin-bottom: 20px;
  }

  .glass-subtitle {
      text-align: center;
      font-size: 1.2rem;
      font-weight: 500;
      margin-bottom: 40px;
      color: #cce7ff;
      text-shadow: 0 0 8px rgba(64, 160, 255, 0.5);
  }

  .chess-board-container {
      display: grid;
      grid-template-columns: repeat(8, 70px);
      grid-template-rows: repeat(8, 70px);
      gap: 6px;
      justify-content: center;
  }

  .chess-square-button {
      border-radius: 14px;
      border: 3px solid rgba(64, 160, 255, 0.3);
      background: rgba(64, 156, 255, 0.12);
      color: rgba(230, 245, 255, 0.8);
      font-size: 2.8rem;
      font-weight: 900;
      font-family: 'SF Mono', monospace;
      box-shadow:
          inset 0 0 18px rgba(64, 180, 255, 0.4),
          0 0 14px rgba(64, 160, 255, 0.55);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      text-shadow: 0 0 6px rgba(64, 200, 255, 0.7);
      user-select: none;
      -webkit-user-select: none;
  }

  .chess-square-button:hover {
      color: #ccecff;
      box-shadow:
          inset 0 0 25px rgba(64, 210, 255, 0.7),
          0 0 30px rgba(64, 210, 255, 1);
      transform: scale(1.13);
      z-index: 10;
  }

  .chess-square-button.selected {
      background: rgba(0, 140, 255, 0.5) !important;
      box-shadow:
          0 0 32px rgba(0, 140, 255, 1),
          inset 0 0 24px rgba(64, 200, 255, 0.85);
      color: #e0f7ff !important;
  }

  .chess-square-button.valid-move {
      background: rgba(0, 175, 255, 0.35) !important;
      box-shadow:
          0 0 22px rgba(0, 180, 255, 0.8);
      color: white !important;
  }

  .tutor-hint {
      position: absolute;
      top: -28px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(64, 156, 255, 0.9);
      color: #00152d;
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 0 20px rgba(64, 156, 255, 0.8);
      user-select: none;
      animation: hintFloat 2.5s ease-in-out infinite;
      z-index: 99;
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
    return f"Best move: {board.san(moves[0])}", 0.85


def display_board(board):
    selected_square = st.session_state.get('selected_square')
    valid_moves = st.session_state.get('valid_moves', [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)

    symbols = {
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
    }

    for rank in range(7, -1, -1):
        for file in range(8):
            square = rank*8 + file
            piece = board.piece_at(square)
            symbol = symbols.get(piece.symbol(), "") if piece else ""

            tutor_hint = ""
            if st.session_state.tutor_mode and st.session_state.show_hints:
                hint = get_tutor_hint(board, selected_square)
                if hint and selected_square == square:
                    hint_text, _ = hint
                    tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'

            classes = ["chess-square-button"]
            if square == selected_square:
                classes.append("selected")
            elif any(move.to_square == square for move in valid_moves):
                classes.append("valid-move")

            st.markdown(f"""
                <div style="position: relative;">
                    <button class="{' '.join(classes)}"
                        onclick="handleChessClick({square})"
                        title="{chr(97+file)}{rank+1}"
                        aria-label="Square {chr(97+file)}{rank+1}">
                        {symbol}
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


def handle_click():
    param = st.experimental_get_query_params()
    if "chess_square_click" in param:
        try:
            clicked = int(param["chess_square_click"][0])
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
    handle_click()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 Glass Chess Advanced 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Interactive transparent glassy blue pieces with smooth animations</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
