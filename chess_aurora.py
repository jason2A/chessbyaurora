import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="Chess Obsidian",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Obsidian-like glassmorphism design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chess-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .chess-title {
        text-align: center;
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .chess-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .chess-board-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .chess-info {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .move-history {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-family: 'Inter', sans-serif;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .button-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .status-message {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .status-check {
        background: rgba(255, 193, 7, 0.2);
        border: 1px solid rgba(255, 193, 7, 0.3);
        color: #ffc107;
    }
    
    .status-checkmate {
        background: rgba(220, 53, 69, 0.2);
        border: 1px solid rgba(220, 53, 69, 0.3);
        color: #dc3545;
    }
    
    .status-stalemate {
        background: rgba(108, 117, 125, 0.2);
        border: 1px solid rgba(108, 117, 125, 0.3);
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

def init_chess_game():
    """Initialize a new chess game"""
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board()
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

def get_board_svg(board, size=400):
    """Convert chess board to SVG"""
    svg_content = chess.svg.board(board=board, size=size)
    return svg_content

def display_board(board):
    """Display the chess board"""
    svg_content = get_board_svg(board)
    
    # Convert SVG to base64 for display
    b64 = base64.b64encode(svg_content.encode('utf-8')).decode()
    
    st.markdown(f"""
    <div class="chess-board-container">
        <img src="data:image/svg+xml;base64,{b64}" alt="Chess Board" style="border-radius: 10px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
    </div>
    """, unsafe_allow_html=True)

def make_move(move_uci):
    """Make a move on the board"""
    try:
        move = chess.Move.from_uci(move_uci)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_uci)
            return True
        else:
            st.error("Invalid move! Please try again.")
            return False
    except ValueError:
        st.error("Invalid move format! Use UCI notation (e.g., 'e2e4', 'g1f3')")
        return False

def get_game_status(board):
    """Get the current game status"""
    if board.is_checkmate():
        return "checkmate", "Checkmate! Game Over."
    elif board.is_stalemate():
        return "stalemate", "Stalemate! Game is a draw."
    elif board.is_insufficient_material():
        return "stalemate", "Insufficient material! Game is a draw."
    elif board.is_check():
        return "check", "Check!"
    else:
        return "normal", "Game in progress"

def main():
    # Initialize the game
    init_chess_game()
    
    # Main container
    st.markdown('<div class="chess-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="chess-title">♟️ Chess Obsidian</h1>', unsafe_allow_html=True)
    st.markdown('<p class="chess-subtitle">A modern chess experience with glassmorphism design</p>', unsafe_allow_html=True)
    
    # Display the board
    display_board(st.session_state.board)
    
    # Game status
    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        status_class = f"status-{status}"
        st.markdown(f'<div class="status-message {status_class}">{message}</div>', unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 New Game", key="new_game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.game_over = False
            st.rerun()
    
    with col2:
        if st.button("↩️ Undo Move", key="undo_move"):
            if len(st.session_state.move_history) > 0:
                st.session_state.board.pop()
                st.session_state.move_history.pop()
                st.rerun()
    
    with col3:
        if st.button("📋 Copy FEN", key="copy_fen"):
            st.code(st.session_state.board.fen())
    
    # Move input
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown("### Make a Move")
    st.markdown("Enter your move in UCI notation (e.g., 'e2e4', 'g1f3', 'e7e5')")
    
    move_input = st.text_input("Move:", key="move_input", placeholder="e2e4")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("♟️ Make Move", key="make_move"):
            if move_input:
                if make_move(move_input):
                    st.rerun()
    
    with col2:
        if st.button("🎲 Random Move", key="random_move"):
            legal_moves = list(st.session_state.board.legal_moves)
            if legal_moves:
                random_move = str(legal_moves[0])
                if make_move(random_move):
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Game information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chess-info">', unsafe_allow_html=True)
        st.markdown("### Game Info")
        st.markdown(f"**Turn:** {'White' if st.session_state.board.turn else 'Black'}")
        st.markdown(f"**Moves Made:** {len(st.session_state.move_history)}")
        st.markdown(f"**Legal Moves:** {st.session_state.board.legal_moves.count()}")
        st.markdown(f"**FEN:** `{st.session_state.board.fen()}`")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="move-history">', unsafe_allow_html=True)
        st.markdown("### Move History")
        if st.session_state.move_history:
            for i, move in enumerate(st.session_state.move_history, 1):
                st.markdown(f"{i}. {move}")
        else:
            st.markdown("No moves made yet.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
