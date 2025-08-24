import streamlit as st
import chess
import chess.svg
import base64
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

# -- CSS styles from your original code plus new multiplayer styles --
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');
  /* (Your full provided CSS goes here, unchanged; trimmed for brevity) */
  /* Added custom piece styles example */
  .piece-archbishop {
      color: gold;
      animation: archbishopGlow 3s ease-in-out infinite;
  }
  @keyframes archbishopGlow {
      0%, 100% { text-shadow: 0 0 8px gold; }
      50% { text-shadow: 0 0 20px orange; }
  }
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    """Initialize all necessary session state variables."""
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'selected_piece' not in st.session_state:
        st.session_state.selected_piece = None
    if 'promotion_piece' not in st.session_state:
        st.session_state.promotion_piece = chess.QUEEN
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = "single"
    if 'room_code' not in st.session_state:
        st.session_state.room_code = None
    if 'player_name' not in st.session_state:
        st.session_state.player_name = None
    if 'waiting_for_opponent' not in st.session_state:
        st.session_state.waiting_for_opponent = False
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'valid_moves' not in st.session_state:
        st.session_state.valid_moves = []
    if 'last_click_time' not in st.session_state:
        st.session_state.last_click_time = 0
    if 'tutor_mode' not in st.session_state:
        st.session_state.tutor_mode = True
    if 'tutor_hints' not in st.session_state:
        st.session_state.tutor_hints = {}
    if 'last_move_quality' not in st.session_state:
        st.session_state.last_move_quality = None
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "intermediate"
    if 'ai_thinking_time' not in st.session_state:
        st.session_state.ai_thinking_time = 2
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = True
    if 'move_quality_threshold' not in st.session_state:
        st.session_state.move_quality_threshold = 0.7

def get_player_color():
    """First player to create room is white, second is black."""
    if st.session_state.room_code:
        return "white" if st.session_state.waiting_for_opponent else "black"
    return "white"

def is_player_turn():
    """Check if it is current player's turn."""
    if st.session_state.game_mode == "single":
        return True
    player_color = get_player_color()
    board_turn = "white" if st.session_state.board.turn else "black"
    return player_color == board_turn

def generate_room_code():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))

def create_multiplayer_game():
    room_code = generate_room_code()
    st.session_state.room_code = room_code
    st.session_state.game_mode = "multiplayer"
    st.session_state.waiting_for_opponent = True
    st.session_state.board = chess.Board()
    st.session_state.move_history = []
    save_game_state()
    return room_code

def join_multiplayer_game(room_code):
    if room_code and len(room_code) == 6:
        st.session_state.room_code = room_code.upper()
        st.session_state.game_mode = "multiplayer"
        st.session_state.waiting_for_opponent = False
        load_game_state()
        return True
    return False

def save_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            game_state = {
                'fen': st.session_state.board.fen(),
                'move_history': st.session_state.move_history,
                'last_updated': time.time()
            }
            filename = f"game_{st.session_state.room_code}.json"
            with open(filename, 'w') as f:
                json.dump(game_state, f)
            return True
        except:
            return False
    return False

def load_game_state():
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            filename = f"game_{st.session_state.room_code}.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    game_state = json.load(f)
                st.session_state.board = chess.Board(game_state['fen'])
                st.session_state.move_history = game_state['move_history']
                return True
        except:
            pass
    return False

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
            st.error("💎 Invalid move! Try again!")
            return False
    except ValueError:
        st.error("💎 Invalid move format! Use UCI notation (e.g., 'e2e4')")
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
        if move in st.session_state.board.legal_moves:
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color and to_sq >= 56) or (not piece.color and to_sq <= 7):
                    move = chess.Move(from_sq, to_sq, chess.QUEEN)
            if make_move(str(move)):
                st.experimental_rerun()
        else:
            select_square(square)
    else:
        select_square(square)

def get_board_svg(board, size=500, selected_square=None, valid_moves=None):
    style = """
        .square.light { fill: #f8f9fa; }
        .square.dark { fill: #6c757d; }
        .square.light:hover { fill: #e9ecef; cursor: pointer; }
        .square.dark:hover { fill: #5a6268; cursor: pointer; }
        .square.selected { fill: #409cff; }
        .square.move { fill: #28a745; }
        .square.check { fill: #ff453a; }
    """
    if selected_square is not None:
        style += f".square-{selected_square} {{ fill: #409cff !important; }}"
    if valid_moves:
        for move in valid_moves:
            style += f".square-{move.to_square} {{ fill: #28a745 !important; }}"
    return chess.svg.board(board=board, size=size, style=style)

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
                'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
                'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
                # Add custom pieces here if needed like 'a': '⯈', 'A': '⯈'
            }
            piece_symbol = piece_symbols.get(piece.symbol(), "") if piece else ""
            piece_class = ""
            if piece:
                pt = piece.symbol().lower()
                piece_class_map = {
                    'k': "piece-king",
                    'q': "piece-queen",
                    'r': "piece-rook",
                    'b': "piece-bishop",
                    'n': "piece-knight",
                    'p': "piece-pawn",
                    # Add custom piece class mapping if added
                }
                piece_class = piece_class_map.get(pt, "")
            tutor_hint = ""
            if st.session_state.get('tutor_mode', False) and st.session_state.get('show_hints', True):
                from functions import get_tutor_hint  # Use if defined elsewhere or inline
                hint_result = get_tutor_hint(board, selected_square)
                if hint_result and selected_square == square:
                    hint_text, _ = hint_result
                    tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'
            button_classes = ["chess-square-button", piece_class]
            if st.session_state.get('tutor_mode', False):
                button_classes.append("tutor-mode-active")
            bg_color = 'rgba(64, 156, 255, 0.8)' if square == selected_square else \
                'rgba(40, 167, 69, 0.8)' if any(move.to_square == square for move in valid_moves) else \
                'rgba(248, 249, 250, 0.9)' if (rank + file) % 2 == 0 else 'rgba(108, 117, 125, 0.9)'
            color = 'white' if square == selected_square or any(move.to_square == square for move in valid_moves) or (rank + file) % 2 != 0 else 'black'
            with cols[file]:
                st.markdown(f"""
                <div style="position: relative;">
                <button
                  class="{' '.join(button_classes)}"
                  onclick="handleChessClick({square})"
                  style="background: {bg_color}; color: {color}; width: 100%; height: 70px; 
                         border: 3px solid rgba(64, 156, 255, 0.3); border-radius: 12px; 
                         font-family: 'SF Mono', 'Monaco', 'Menlo', monospace; font-weight: 700;
                         font-size: 2.5rem; cursor: pointer; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                         display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;"
                  title="Square {chr(97 + file)}{rank + 1}"
                >{piece_symbol}</button>
                {tutor_hint}
                </div>""", unsafe_allow_html=True)
    st.markdown("""
    <script>
    function handleChessClick(square) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        const existing = document.getElementById('chess-click-input');
        if (existing) existing.remove();
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Include other functions as in your original code e.g. evaluate_position, get_best_moves, get_ai_move, etc.

def main():
    init_chess_game()
    # Listen for JS square clicks
    if 'chess_square_click' in st.experimental_get_query_params():
        try:
            clicked_square = int(st.experimental_get_query_params()['chess_square_click'][0])
            handle_square_click(clicked_square)
            st.experimental_set_query_params()
        except Exception:
            pass

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)

    display_board(st.session_state.board)

    status, msg = get_game_status(st.session_state.board)
    if status != 'normal':
        st.markdown(f'<div class="status-message status-{status}">{msg}</div>', unsafe_allow_html=True)

    if st.session_state.game_mode == 'multiplayer':
        load_game_state()
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🌐 Multiplayer Game")
        st.markdown(f"**Room Code:** `{st.session_state.room_code}`")
        st.markdown(f"**Your Color:** {get_player_color().title()}")

        if st.session_state.waiting_for_opponent:
            st.markdown("⏳ **Waiting for opponent to join...** Share the room code with your friend!")
        else:
            if is_player_turn():
                st.markdown("✅ **Your turn!**")
            else:
                st.markdown("⏳ **Opponent's turn**")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔙 Back to Single Player"):
                st.session_state.game_mode = 'single'
                st.session_state.room_code = None
                st.session_state.waiting_for_opponent = False
                st.experimental_rerun()
        with col2:
            if st.button("🔄 Refresh Game"):
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🎮 Game Mode")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🌐 Create Multiplayer Game"):
                code = create_multiplayer_game()
                st.success(f"Multiplayer game created! Room code: {code}")
                st.experimental_rerun()
        with col2:
            room_input = st.text_input("Join Room Code:")
            if st.button("🎯 Join Game"):
                if join_multiplayer_game(room_input):
                    st.success("Joined multiplayer game!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid room code!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Difficulty and tutor controls, game controls, stats, AI move button etc. go here (keep your original implementations)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
