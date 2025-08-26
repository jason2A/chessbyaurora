import streamlit as st
import chess
import random
import time
import json
import os

# Page setup
st.set_page_config(page_title="💎 Glass Chess Velvet Multiplayer", layout="wide", page_icon="💎")

# Modern glass velvet style CSS with blue highlights and glowing pieces
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display&family=SF+Mono&display=swap');
:root {
  --blue-light: #409CFF;
  --blue-velvet: #162A58;
  --gold-highlight: #FFD700;
  --red-highlight: #FF453A;
}

body, .stApp, .main {
  background: linear-gradient(135deg, var(--blue-velvet), #101F4A);
  background-size: 400% 400%;
  animation: velvetGradient 20s ease infinite;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
  color: #ddd;
}

@keyframes velvetGradient {
  0%, 100% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
}

.glass-container {
  background: rgba(16, 25, 74, 0.85);
  border-radius: 32px;
  border: 1px solid rgba(50, 65, 120, 0.8);
  box-shadow: 0 15px 30px rgba(16, 25, 74, 0.85);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  padding: 2.5rem;
  max-width: 1100px;
  margin: 2rem auto;
  animation: floatPane 8s ease-in-out infinite;
}

@keyframes floatPane {
  0%, 100% {transform: translateY(0);}
  50% {transform: translateY(-6px);}
}

h1, h2 {
  text-align: center;
  color: white;
  font-weight: 800;
  filter: drop-shadow(0 0 3px var(--blue-light));
  letter-spacing: -0.03em;
  margin-bottom: 0.1rem;
}

h1 {
  font-size: 3.8rem;
  text-shadow: 0 0 15px var(--blue-light), 0 0 25px var(--gold-highlight), 0 0 35px var(--red-highlight);
  animation: titleGlow 10s ease-in-out infinite alternate;
}

@keyframes titleGlow {
  0%{ text-shadow: 0 0 8px var(--blue-light), 0 0 18px var(--gold-highlight); }
  100%{ text-shadow: 0 0 21px var(--blue-light), 0 0 41px var(--gold-highlight), 0 0 51px var(--red-highlight);}
}

h2.subtitle {
  font-weight: 400;
  color: #cdd6f4cc;
  margin-top: -12px;
  margin-bottom: 2rem;
  font-size: 1.3rem;
  letter-spacing: 0.02em;
  filter: drop-shadow(0 0 2px var(--blue-light));
  animation: subtGlow 10s ease-in-out infinite alternate;
}

@keyframes subtGlow {
  0%, 100% {opacity: 0.7;}
  50% {opacity: 1;}
}

.chessboard {
  display: grid;
  grid-template-columns: repeat(8, minmax(64px, 1fr));
  grid-template-rows: repeat(8, 64px);
  gap: 2px;
  max-width: 512px;
  margin: auto;
  border-radius: 14px;
  box-shadow: inset 0 0 12px var(--blue-light), 0 0 16px var(--blue-light);
  background: linear-gradient(135deg, #14284a, #203e7a);
  user-select: none;
  overflow: hidden;
  animation: boardGlow 8s ease-in-out infinite alternate;
}

@keyframes boardGlow {
  0%, 100% {box-shadow: inset 0 0 12px var(--blue-light), 0 0 18px var(--blue-light);}
  50% {box-shadow: inset 0 0 22px var(--blue-light), 0 0 28px var(--gold-highlight);}
}

.square {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  cursor: pointer;
  font-weight: 900;
  font-family: 'SF Mono', monospace;
  border-radius: 10px;
  transition: background 0.3s ease, box-shadow 0.4s ease;
  color: rgba(220, 220, 255, 0.95);
}

.square.light {
  background: rgba(10, 25, 50, 0.4);
  box-shadow: inset 0 0 8px rgba(40, 70, 110, 0.7);
}

.square.dark {
  background: rgba(20, 35, 70, 0.7);
  box-shadow: inset 0 0 9px rgba(20, 40, 75, 0.8);
}

.square.selected {
  background: rgba(64, 156, 255, 0.8) !important;
  box-shadow: 0 0 10px var(--blue-light) !important;
  color: white !important;
}

.square.valid {
  background: rgba(255, 215, 0, 0.7) !important;
  box-shadow: 0 0 12px var(--gold-highlight) !important;
  color: #201800 !important;
}

.square:hover {
  filter: brightness(1.2);
  box-shadow: 0 0 12px var(--blue-light);
}

.piece {
  animation: pieceGlow 8s ease-in-out infinite alternate;
  user-select: none;
}

@keyframes pieceGlow {
  0% {text-shadow: 0 0 8px var(--blue-light);}
  100% {text-shadow: 0 0 20px var(--gold-highlight);}
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init():
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

# Returns Unicode symbols for chess pieces with classes for animations
def piece_unicode(piece):
    if not piece:
        return ""
    unicode_pieces = {
        "P":"♙",
        "N":"♘",
        "B":"♗",
        "R":"♖",
        "Q":"♕",
        "K":"♔",
        "p":"♟",
        "n":"♞",
        "b":"♝",
        "r":"♜",
        "q":"♛",
        "k":"♚"
    }
    return f'<span class="piece piece-{piece.symbol().lower()}">{unicode_pieces[piece.symbol()]}</span>'

# Draw the board with clickable squares
def draw_board():
    board = st.session_state.board
    selected = st.session_state.selected_square
    valid_moves = st.session_state.valid_moves

    letters = "abcdefgh"

    # Build grid squares as buttons
    cols = st.columns(8)

    html = '<div class="chessboard">'
    for rank in range(7, -1, -1):
        for file in range(8):
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            color = 'light' if (rank + file) % 2 == 0 else 'dark'

            classes = f"square {color}"
            if sq == selected:
                classes += " selected"
            elif any(move.to_square == sq for move in valid_moves):
                classes += " valid"

            piece_html = piece_unicode(piece)

            html += (f'<button class="{classes}" id="square-{sq}" title="{letters[file]}{rank+1}" '
                     f'onclick="sendClick({sq})">{piece_html}</button>')
    html += "</div>"

    # Inject JS function for click handling to Streamlit input widget hack
    js = """
    <script>
    const sendClick = (sq) => {
        let inputEl = window.parent.document.querySelector('input[id="square-click"]');
        if (!inputEl) {
            inputEl = window.parent.document.createElement('input');
            inputEl.type = 'hidden';
            inputEl.id = 'square-click';
            inputEl.name = 'square-click';
            window.parent.document.body.appendChild(inputEl);
        }
        inputEl.value = sq;
        inputEl.dispatchEvent(new Event('change'));
    }
    </script>
    """

    st.markdown(html + js, unsafe_allow_html=True)

def update_state():
    # Check if clicked square input exists
    clicked = st.experimental_get_query_params().get("square-click")
    if not clicked:
        # Old-style form workaround
        if "square-click" in st.session_state:
            clicked = [str(st.session_state["square-click"])]
    if clicked:
        sq = int(clicked[0])
        board = st.session_state.board
        # Handle selection and moves
        if st.session_state.selected_square is None:
            # Select the piece only if it is player's turn piece color
            piece = board.piece_at(sq)
            if piece and piece.color == board.turn:
                st.session_state.selected_square = sq
                st.session_state.valid_moves = [m for m in board.legal_moves if m.from_square == sq]
        else:
            move = chess.Move(st.session_state.selected_square, sq)
            # Auto promote pawn to queen
            piece = board.piece_at(st.session_state.selected_square)
            if piece is not None and piece.piece_type == chess.PAWN:
                if (piece.color and sq >= 56) or (not piece.color and sq <= 7):
                    move = chess.Move(st.session_state.selected_square, sq, promotion=chess.QUEEN)
            if move in board.legal_moves:
                board.push(move)
                st.session_state.move_history.append(move.uci())
                st.session_state.selected_square = None
                st.session_state.valid_moves = []
                # Save multiplayer state if needed
                if st.session_state.game_mode == "multiplayer":
                    save_game_state()
            else:
                # If clicked invalid square, select new square if allowed
                piece = board.piece_at(sq)
                if piece and piece.color == board.turn:
                    st.session_state.selected_square = sq
                    st.session_state.valid_moves = [m for m in board.legal_moves if m.from_square == sq]
                else:
                    st.session_state.selected_square = None
                    st.session_state.valid_moves = []
            # Clear the input
            st.experimental_set_query_params(**{"square-click": None})

def save_game_state():
    try:
        state = {
            "fen": st.session_state.board.fen(),
            "move_history": st.session_state.move_history,
            "last_updated": time.time()
        }
        filename = f"game_{st.session_state.room_code}.json"
        with open(filename, "w") as f:
            json.dump(state, f)
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False

def load_game_state():
    try:
        filename = f"game_{st.session_state.room_code}.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                state = json.load(f)
            st.session_state.board.set_fen(state["fen"])
            st.session_state.move_history = state["move_history"]
            return True
    except Exception as e:
        print(f"Error loading state: {e}")
    return False

def is_player_turn():
    # Simple player color assignment: first player (who created room) = white, else black
    if st.session_state.game_mode == "single":
        return True
    if not st.session_state.room_code:
        return False
    color = "white" if st.session_state.waiting else "black"
    turn = "white" if st.session_state.board.turn else "black"
    return color == turn

def main():
    init()
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.title("💎 Glass Chess Velvet Multiplayer")
    st.markdown('<h2 class="subtitle">Crystal Clear Transparent Velvet with Blue Lighting</h2>', unsafe_allow_html=True)

    # Multiplayer controls & join/create room
    if st.session_state.game_mode == "single":
        if st.button("Create Multiplayer Room"):
            code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
            st.session_state.room_code = code
            st.session_state.waiting = True
            st.session_state.game_mode = "multiplayer"
            st.experimental_rerun()
        room_to_join = st.text_input("Or enter Multiplayer Room Code:")
        if st.button("Join Room"):
            if room_to_join.strip().upper() == st.session_state.room_code:
                st.session_state.waiting = False
                st.experimental_rerun()
            else:
                st.error("Invalid Room Code")
    else:
        st.info(f"Multiplayer Room: {st.session_state.room_code}")
        if st.session_state.waiting:
            st.info("Waiting for opponent to join. Share your room code.")
            room_to_join = st.text_input("Enter Room Code to Join")
            if st.button("Join Room"):
                if room_to_join.strip().upper() == st.session_state.room_code:
                    st.session_state.waiting = False
                    st.experimental_rerun()
                else:
                    st.error("Invalid Room Code")
        else:
            my_color = "White" if st.session_state.waiting else "Black"
            st.success(f"You are playing as {my_color}")
            turn_status = "Your turn" if is_player_turn() else "Opponent's turn"
            if is_player_turn():
                st.info("Your turn - Make your move")
            else:
                st.warning("Waiting for opponent's move")

            # Refresh button for manual refresh (simulate live updates)
            if st.button("Refresh Game State"):
                load_game_state()
                st.experimental_rerun()

            # Load latest state regularly - you can add st.experimental_rerun() with timer if needed

    draw_board()
    update_state()

    # Game controls
    cols = st.columns(5)
    if cols[0].button("New Game"):
        st.session_state.board.reset()
        st.session_state.move_history = []
        st.session_state.selected_square = None
        st.session_state.valid_moves = []

        if st.session_state.game_mode == "multiplayer":
            save_game_state()
        st.experimental_rerun()

    if cols[1].button("Undo Move") and len(st.session_state.board.move_stack) > 0:
        st.session_state.board.pop()
        if st.session_state.move_history:
            st.session_state.move_history.pop()
        st.session_state.selected_square = None
        st.session_state.valid_moves = []
        if st.session_state.game_mode == "multiplayer":
            save_game_state()
        st.experimental_rerun()

    if cols[2].button("Flip Board"):
        st.session_state.flip_board = not st.session_state.get("flip_board", False)
        st.experimental_rerun()

    if cols[3].button("Save Game"):
        if st.session_state.game_mode == "multiplayer":
            saved = save_game_state()
            if saved:
                st.success("Game saved successfully!")
            else:
                st.error("Failed to save game.")

    # Show game info & move count
    st.markdown(f"**Move count:** {len(st.session_state.move_history)}")
    status, msg = get_game_status(st.session_state.board)
    if status != "normal":
        st.markdown(f"<div class='status-message status-{status}'>{msg}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
