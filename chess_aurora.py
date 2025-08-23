import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import time
import random

# Page configuration
st.set_page_config(
    page_title="🔥 Fire Chess",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for FIRE theme with glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 25%, #ffd700 50%, #ff6b35 75%, #cc0000 100%);
        background-size: 400% 400%;
        animation: fireGradient 8s ease infinite;
        min-height: 100vh;
        padding: 0;
    }
    
    @keyframes fireGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 25%, #ffd700 50%, #ff6b35 75%, #cc0000 100%);
        background-size: 400% 400%;
        animation: fireGradient 8s ease infinite;
    }
    
    .fire-container {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 2px solid rgba(255, 107, 53, 0.5);
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow: 
            0 0 50px rgba(255, 107, 53, 0.3),
            0 0 100px rgba(255, 215, 0, 0.2),
            inset 0 0 50px rgba(255, 107, 53, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .fire-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 107, 53, 0.1) 50%, transparent 70%);
        animation: fireShimmer 3s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes fireShimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .fire-title {
        text-align: center;
        color: #ffd700;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 4rem;
        margin-bottom: 0.5rem;
        text-shadow: 
            0 0 10px #ff6b35,
            0 0 20px #ff6b35,
            0 0 30px #ff6b35,
            0 0 40px #ff6b35;
        animation: fireTitle 2s ease-in-out infinite alternate;
    }
    
    @keyframes fireTitle {
        0% { text-shadow: 0 0 10px #ff6b35, 0 0 20px #ff6b35, 0 0 30px #ff6b35; }
        100% { text-shadow: 0 0 15px #ffd700, 0 0 25px #ffd700, 0 0 35px #ffd700; }
    }
    
    .fire-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .chess-board-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        position: relative;
    }
    
    .chess-board-container img {
        border-radius: 15px;
        box-shadow: 
            0 0 30px rgba(255, 107, 53, 0.5),
            0 0 60px rgba(255, 215, 0, 0.3),
            inset 0 0 20px rgba(255, 107, 53, 0.2);
        transition: all 0.3s ease;
    }
    
    .chess-board-container img:hover {
        transform: scale(1.02);
        box-shadow: 
            0 0 40px rgba(255, 107, 53, 0.7),
            0 0 80px rgba(255, 215, 0, 0.5);
    }
    
    .fire-info {
        background: rgba(255, 107, 53, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 107, 53, 0.3);
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
    }
    
    .move-history {
        background: rgba(255, 215, 0, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-family: 'Inter', sans-serif;
        max-height: 300px;
        overflow-y: auto;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
    }
    
    .fire-button {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        border: none;
        border-radius: 15px;
        color: white;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .fire-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .fire-button:hover::before {
        left: 100%;
    }
    
    .fire-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6);
        background: linear-gradient(135deg, #f7931e, #ffd700);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6) !important;
        background: linear-gradient(135deg, #f7931e, #ffd700) !important;
    }
    
    .fire-input {
        background: rgba(255, 107, 53, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 2px solid rgba(255, 107, 53, 0.3);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid rgba(255, 107, 53, 0.5) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 500 !important;
        padding: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
    }
    
    .status-message {
        text-align: center;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.2rem;
        animation: statusPulse 2s ease-in-out infinite;
    }
    
    @keyframes statusPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .status-check {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.3), rgba(255, 215, 0, 0.3));
        border: 2px solid #ffc107;
        color: #ffd700;
        box-shadow: 0 0 20px rgba(255, 193, 7, 0.5);
    }
    
    .status-checkmate {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.3), rgba(255, 0, 0, 0.3));
        border: 2px solid #dc3545;
        color: #ff6b6b;
        box-shadow: 0 0 30px rgba(220, 53, 69, 0.7);
    }
    
    .status-stalemate {
        background: linear-gradient(135deg, rgba(108, 117, 125, 0.3), rgba(169, 169, 169, 0.3));
        border: 2px solid #6c757d;
        color: #b0b0b0;
        box-shadow: 0 0 20px rgba(108, 117, 125, 0.5);
    }
    
    .drag-instructions {
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffd700;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    
    .piece-selector {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .piece-option {
        background: rgba(255, 107, 53, 0.2);
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: white;
        font-family: 'Orbitron', monospace;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .piece-option:hover {
        background: rgba(255, 107, 53, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
    }
    
    .piece-option.selected {
        background: rgba(255, 215, 0, 0.3);
        border-color: #ffd700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
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
    if 'selected_piece' not in st.session_state:
        st.session_state.selected_piece = None
    if 'promotion_piece' not in st.session_state:
        st.session_state.promotion_piece = chess.QUEEN

def get_board_svg(board, size=500):
    """Convert chess board to SVG with fire theme"""
    # Custom SVG styling for fire theme
    svg_content = chess.svg.board(
        board=board, 
        size=size,
        style="""
        .square.light { fill: #f4d03f; }
        .square.dark { fill: #e67e22; }
        .square.light:hover { fill: #f39c12; }
        .square.dark:hover { fill: #d35400; }
        .square.selected { fill: #e74c3c; }
        .square.move { fill: #27ae60; }
        .square.check { fill: #e74c3c; }
        """
    )
    return svg_content

def display_board(board):
    """Display the chess board with fire effects"""
    svg_content = get_board_svg(board)
    
    # Convert SVG to base64 for display
    b64 = base64.b64encode(svg_content.encode('utf-8')).decode()
    
    st.markdown(f"""
    <div class="chess-board-container">
        <img src="data:image/svg+xml;base64,{b64}" alt="Fire Chess Board" style="max-width: 100%; height: auto;">
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
            st.error("🔥 Invalid move! Try again!")
            return False
    except ValueError:
        st.error("🔥 Invalid move format! Use UCI notation (e.g., 'e2e4', 'g1f3')")
        return False

def get_game_status(board):
    """Get the current game status"""
    if board.is_checkmate():
        return "checkmate", "🔥 CHECKMATE! The game is over! ��"
    elif board.is_stalemate():
        return "stalemate", "⚖️ STALEMATE! The game is a draw! ⚖️"
    elif board.is_insufficient_material():
        return "stalemate", "⚖️ Insufficient material! Draw! ⚖️"
    elif board.is_check():
        return "check", "⚡ CHECK! Your king is in danger! ⚡"
    else:
        return "normal", "🔥 Game in progress 🔥"

def get_best_moves(board, num_moves=3):
    """Get some suggested moves (simplified)"""
    legal_moves = list(board.legal_moves)
    if len(legal_moves) > 0:
        return random.sample(legal_moves, min(num_moves, len(legal_moves)))
    return []

def main():
    # Initialize the game
    init_chess_game()
    
    # Main container
    st.markdown('<div class="fire-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="fire-title">�� FIRE CHESS 🔥</h1>', unsafe_allow_html=True)
    st.markdown('<p class="fire-subtitle">Where every move burns with intensity!</p>', unsafe_allow_html=True)
    
    # Display the board
    display_board(st.session_state.board)
    
    # Game status
    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        status_class = f"status-{status}"
        st.markdown(f'<div class="status-message {status_class}">{message}</div>', unsafe_allow_html=True)
    
    # Drag instructions
    st.markdown("""
    <div class="drag-instructions">
        🎯 <strong>How to Play:</strong> Enter moves in UCI notation (e.g., 'e2e4', 'g1f3', 'e7e5')
    </div>
    """, unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🔥 NEW GAME", key="new_game"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.game_over = False
            st.rerun()
    
    with col2:
        if st.button("↩️ UNDO", key="undo_move"):
            if len(st.session_state.move_history) > 0:
                st.session_state.board.pop()
                st.session_state.move_history.pop()
                st.rerun()
    
    with col3:
        if st.button("🎲 RANDOM", key="random_move"):
            legal_moves = list(st.session_state.board.legal_moves)
            if legal_moves:
                random_move = str(legal_moves[0])
                if make_move(random_move):
                    st.rerun()
    
    with col4:
        if st.button("📋 FEN", key="copy_fen"):
            st.code(st.session_state.board.fen())
    
    # Move input with fire styling
    st.markdown('<div class="fire-input">', unsafe_allow_html=True)
    st.markdown("### 🔥 Make Your Move")
    
    move_input = st.text_input("Enter move (UCI):", key="move_input", placeholder="e2e4")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("♟️ MAKE MOVE", key="make_move"):
            if move_input:
                if make_move(move_input):
                    st.rerun()
    
    with col2:
        if st.button("🤖 AI MOVE", key="ai_move"):
            legal_moves = list(st.session_state.board.legal_moves)
            if legal_moves:
                # Simple AI: pick a random move
                ai_move = str(random.choice(legal_moves))
                if make_move(ai_move):
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Game information with fire theme
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="fire-info">', unsafe_allow_html=True)
        st.markdown("### 🔥 Game Info")
        st.markdown(f"**Turn:** {'⚪ White' if st.session_state.board.turn else '⚫ Black'}")
        st.markdown(f"**Moves Made:** {len(st.session_state.move_history)}")
        st.markdown(f"**Legal Moves:** {st.session_state.board.legal_moves.count()}")
        
        # Show some suggested moves
        best_moves = get_best_moves(st.session_state.board)
        if best_moves:
            st.markdown("**�� Suggested Moves:**")
            for i, move in enumerate(best_moves, 1):
                st.markdown(f"  {i}. `{move}`")
        
        st.markdown(f"**FEN:** `{st.session_state.board.fen()}`")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="move-history">', unsafe_allow_html=True)
        st.markdown("### 📜 Move History")
        if st.session_state.move_history:
            for i, move in enumerate(st.session_state.move_history, 1):
                st.markdown(f"**{i}.** `{move}`")
        else:
            st.markdown("No moves made yet. Start the fire! 🔥")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
