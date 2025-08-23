import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import time
import random
import requests
import re
import os

# Page configuration
st.set_page_config(
    page_title="💎 Glass Chess",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for iOS 26 Glassy theme with blue, gold, and red hues
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');
    
    /* Global animations */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
        min-height: 100vh;
        padding: 0;
    }
    
    @keyframes glassGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        animation: containerFloat 6s ease-in-out infinite;
    }
    
    @keyframes containerFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .glass-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(64, 156, 255, 0.05) 50%, transparent 70%);
        animation: glassShimmer 4s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes glassShimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .glass-title {
        text-align: center;
        color: #ffffff;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 
            0 0 20px rgba(64, 156, 255, 0.5),
            0 0 40px rgba(255, 215, 0, 0.3);
        animation: glassTitle 4s ease-in-out infinite alternate;
        letter-spacing: -0.02em;
        position: relative;
    }
    
    .glass-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #409cff, #ffd700, #ff453a);
        animation: titleUnderline 3s ease-in-out infinite;
    }
    
    @keyframes titleUnderline {
        0%, 100% { width: 0; opacity: 0; }
        50% { width: 200px; opacity: 1; }
    }
    
    @keyframes glassTitle {
        0% { 
            text-shadow: 0 0 20px rgba(64, 156, 255, 0.5), 0 0 40px rgba(255, 215, 0, 0.3);
            transform: scale(1) rotateY(0deg);
        }
        100% { 
            text-shadow: 0 0 30px rgba(255, 69, 58, 0.6), 0 0 50px rgba(255, 215, 0, 0.4);
            transform: scale(1.02) rotateY(2deg);
        }
    }
    
    .glass-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
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
        display: flex;
        justify-content: center;
        margin: 2.5rem 0;
        position: relative;
        animation: boardContainerPulse 8s ease-in-out infinite;
    }
    
    @keyframes boardContainerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.01); }
    }
    
    .chess-board-container img {
        border-radius: 24px;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: boardGlow 6s ease-in-out infinite;
    }
    
    @keyframes boardGlow {
        0%, 100% { 
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        50% { 
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1),
                0 0 30px rgba(64, 156, 255, 0.2);
        }
    }
    
    .chess-board-container img:hover {
        transform: scale(1.02) translateY(-4px) rotateY(2deg);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 40px rgba(255, 215, 0, 0.3);
    }
    
    .glass-info {
        background: rgba(64, 156, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(64, 156, 255, 0.15);
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        box-shadow: 
            0 8px 32px rgba(64, 156, 255, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        animation: infoPanelFloat 7s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .glass-info::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(64, 156, 255, 0.1), transparent);
        animation: infoShimmer 5s ease-in-out infinite;
    }
    
    @keyframes infoPanelFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }
    
    @keyframes infoShimmer {
        0%, 100% { left: -100%; }
        50% { left: 100%; }
    }
    
    .move-history {
        background: rgba(255, 215, 0, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 215, 0, 0.15);
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        max-height: 350px;
        overflow-y: auto;
        box-shadow: 
            0 8px 32px rgba(255, 215, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        animation: historyPanelFloat 8s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .move-history::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
        animation: historyShimmer 6s ease-in-out infinite;
    }
    
    @keyframes historyPanelFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-2px); }
    }
    
    @keyframes historyShimmer {
        0%, 100% { left: -100%; }
        50% { left: 100%; }
    }
    
    .glass-button {
        background: linear-gradient(135deg, rgba(64, 156, 255, 0.9), rgba(255, 69, 58, 0.9));
        border: none;
        border-radius: 20px;
        color: white;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 24px rgba(64, 156, 255, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.01em;
        animation: buttonPulse 4s ease-in-out infinite;
    }
    
    .glass-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-button:hover::before {
        left: 100%;
    }
    
    .glass-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 
            0 12px 32px rgba(64, 156, 255, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.15);
        background: linear-gradient(135deg, rgba(255, 69, 58, 0.9), rgba(255, 215, 0, 0.9));
        animation: buttonHover 0.3s ease-in-out;
    }
    
    @keyframes buttonPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes buttonHover {
        0% { transform: translateY(-2px) scale(1.05); }
        50% { transform: translateY(-4px) scale(1.08); }
        100% { transform: translateY(-2px) scale(1.05); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(64, 156, 255, 0.9), rgba(255, 69, 58, 0.9)) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 24px rgba(64, 156, 255, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 12px 32px rgba(64, 156, 255, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.15) !important;
        background: linear-gradient(135deg, rgba(255, 69, 58, 0.9), rgba(255, 215, 0, 0.9)) !important;
    }
    
    .glass-input {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        font-family: 'SF Mono', 'Monaco', 'Menlo', monospace !important;
        font-weight: 500 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(64, 156, 255, 0.8) !important;
        box-shadow: 
            0 0 0 4px rgba(64, 156, 255, 0.1),
            0 0 0 1px rgba(64, 156, 255, 0.8) !important;
        background: rgba(0, 0, 0, 0.3) !important;
    }
    
    .status-message {
        text-align: center;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        animation: statusPulse 3s ease-in-out infinite;
        letter-spacing: 0.01em;
    }
    
    @keyframes statusPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .status-check {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 193, 7, 0.15));
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #ffd700;
        box-shadow: 
            0 8px 32px rgba(255, 215, 0, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    
    .status-checkmate {
        background: linear-gradient(135deg, rgba(255, 69, 58, 0.15), rgba(220, 53, 69, 0.15));
        border: 1px solid rgba(255, 69, 58, 0.3);
        color: #ff6b6b;
        box-shadow: 
            0 8px 32px rgba(255, 69, 58, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    
    .status-stalemate {
        background: linear-gradient(135deg, rgba(108, 117, 125, 0.15), rgba(169, 169, 169, 0.15));
        border: 1px solid rgba(108, 117, 125, 0.3);
        color: #b0b0b0;
        box-shadow: 
            0 8px 32px rgba(108, 117, 125, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.05);
    }
    
    .drag-instructions {
        background: rgba(255, 215, 0, 0.08);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #ffd700;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 500;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(255, 215, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    
    .piece-selector {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .piece-option {
        background: rgba(64, 156, 255, 0.1);
        border: 1px solid rgba(64, 156, 255, 0.2);
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        color: white;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    .piece-option:hover {
        background: rgba(64, 156, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 
            0 8px 24px rgba(64, 156, 255, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    
    .piece-option.selected {
        background: rgba(255, 215, 0, 0.2);
        border-color: rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 8px 24px rgba(255, 215, 0, 0.2),
            0 0 0 1px rgba(255, 215, 0, 0.4);
    }
    
    /* Custom scrollbar for move history */
    .move-history::-webkit-scrollbar {
        width: 8px;
    }
    
    .move-history::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    .move-history::-webkit-scrollbar-thumb {
        background: rgba(255, 215, 0, 0.3);
        border-radius: 4px;
    }
    
    .move-history::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 215, 0, 0.5);
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
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = "single"
    if 'room_code' not in st.session_state:
        st.session_state.room_code = None
    if 'player_name' not in st.session_state:
        st.session_state.player_name = None
    if 'waiting_for_opponent' not in st.session_state:
        st.session_state.waiting_for_opponent = False

def get_board_svg(board, size=500):
    """Convert chess board to SVG with glass theme"""
    # Custom SVG styling for glass theme
    svg_content = chess.svg.board(
        board=board, 
        size=size,
        style="""
        .square.light { fill: #f8f9fa; }
        .square.dark { fill: #6c757d; }
        .square.light:hover { fill: #e9ecef; }
        .square.dark:hover { fill: #5a6268; }
        .square.selected { fill: #409cff; }
        .square.move { fill: #28a745; }
        .square.check { fill: #ff453a; }
        """
    )
    return svg_content

def display_board(board):
    """Display the chess board with glass effects"""
    svg_content = get_board_svg(board)
    
    # Convert SVG to base64 for display
    b64 = base64.b64encode(svg_content.encode('utf-8')).decode()
    
    st.markdown(f"""
    <div class="chess-board-container">
        <img src="data:image/svg+xml;base64,{b64}" alt="Glass Chess Board" style="max-width: 100%; height: auto;">
    </div>
    """, unsafe_allow_html=True)

def make_move(move_uci):
    """Make a move on the board"""
    try:
        move = chess.Move.from_uci(move_uci)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_uci)
            
            # Save game state for multiplayer
            if st.session_state.game_mode == "multiplayer":
                save_game_state()
            
            return True
        else:
            st.error("💎 Invalid move! Try again!")
            return False
    except ValueError:
        st.error("💎 Invalid move format! Use UCI notation (e.g., 'e2e4', 'g1f3')")
        return False

def get_game_status(board):
    """Get the current game status"""
    if board.is_checkmate():
        return "checkmate", "💎 CHECKMATE! The game is over! 💎"
    elif board.is_stalemate():
        return "stalemate", "⚖️ STALEMATE! The game is a draw! ⚖️"
    elif board.is_insufficient_material():
        return "stalemate", "⚖️ Insufficient material! Draw! ⚖️"
    elif board.is_check():
        return "check", "⚡ CHECK! Your king is in danger! ⚡"
    else:
        return "normal", "💎 Game in progress 💎"

def get_best_moves(board, num_moves=3):
    """Get some suggested moves (simplified)"""
    legal_moves = list(board.legal_moves)
    if len(legal_moves) > 0:
        return random.sample(legal_moves, min(num_moves, len(legal_moves)))
    return []

def analyze_position(board):
    """Analyze the current position using AI"""
    try:
        # Simple position evaluation
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        
        white_material = 0
        black_material = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color:
                    white_material += value
                else:
                    black_material += value
        
        evaluation = white_material - black_material
        
        if evaluation > 0:
            return f"White is ahead by {evaluation} pawns", "advantage"
        elif evaluation < 0:
            return f"Black is ahead by {abs(evaluation)} pawns", "disadvantage"
        else:
            return "Position is equal", "equal"
    except:
        return "Analysis unavailable", "unknown"

def get_move_analysis(move_uci, board):
    """Analyze a specific move"""
    try:
        # Create a copy of the board to test the move
        test_board = board.copy()
        move = chess.Move.from_uci(move_uci)
        
        if move in test_board.legal_moves:
            test_board.push(move)
            
            # Check if it's a check
            if test_board.is_check():
                return "This move gives check!", "check"
            
            # Check if it's a capture
            if board.is_capture(move):
                return "This is a capture move", "capture"
            
            # Check if it's a pawn move
            piece = board.piece_at(move.from_square)
            if piece and piece.piece_type == chess.PAWN:
                return "Pawn move - advancing position", "pawn"
            
            return "Standard developing move", "normal"
        else:
            return "Invalid move", "invalid"
    except:
        return "Move analysis unavailable", "unknown"

def generate_game_summary(move_history):
    """Generate a summary of the game"""
    if not move_history:
        return "Game has just begun. White to move."
    
    num_moves = len(move_history)
    opening_moves = move_history[:4] if len(move_history) >= 4 else move_history
    
    summary = f"Game in progress with {num_moves} moves played. "
    
    if num_moves <= 4:
        summary += "Still in the opening phase."
    elif num_moves <= 20:
        summary += "Middlegame position."
    else:
        summary += "Endgame approaching."
    
    return summary

def get_game_statistics(board, move_history):
    """Get detailed game statistics"""
    stats = {}
    
    # Count pieces
    piece_counts = {'white': {}, 'black': {}}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_name = piece.symbol().upper()
            color = 'white' if piece.color else 'black'
            piece_counts[color][piece_name] = piece_counts[color].get(piece_name, 0) + 1
    
    stats['piece_counts'] = piece_counts
    
    # Game phase
    total_pieces = sum(len(pieces) for pieces in piece_counts.values())
    if total_pieces > 20:
        stats['phase'] = "Opening"
    elif total_pieces > 10:
        stats['phase'] = "Middlegame"
    else:
        stats['phase'] = "Endgame"
    
    # Control of center
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    center_control = {'white': 0, 'black': 0}
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            color = 'white' if piece.color else 'black'
            center_control[color] += 1
    
    stats['center_control'] = center_control
    
    return stats

def export_pgn(board, move_history):
    """Export game to PGN format"""
    try:
        # Create a new board and replay moves
        game_board = chess.Board()
        pgn_moves = []
        
        for move_uci in move_history:
            move = chess.Move.from_uci(move_uci)
            pgn_moves.append(game_board.san(move))
            game_board.push(move)
        
        # Create PGN header
        pgn = f"""[Event "Glass Chess Game"]
[Site "Streamlit App"]
[Date "{time.strftime('%Y.%m.%d')}"]
[Round "1"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]

{' '.join(pgn_moves)} *"""
        
        return pgn
    except:
        return "PGN export failed"

def generate_room_code():
    """Generate a random room code"""
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_multiplayer_game():
    """Create a new multiplayer game"""
    room_code = generate_room_code()
    st.session_state.room_code = room_code
    st.session_state.game_mode = "multiplayer"
    st.session_state.waiting_for_opponent = True
    return room_code

def join_multiplayer_game(room_code):
    """Join an existing multiplayer game"""
    if room_code and len(room_code) == 6:
        st.session_state.room_code = room_code.upper()
        st.session_state.game_mode = "multiplayer"
        st.session_state.waiting_for_opponent = False
        return True
    return False

def get_player_color():
    """Get the current player's color based on room code"""
    if st.session_state.room_code:
        # Simple logic: first player (creator) is white, second player is black
        return "white" if st.session_state.waiting_for_opponent else "black"
    return "white"

def is_player_turn():
    """Check if it's the current player's turn"""
    if st.session_state.game_mode == "single":
        return True
    
    player_color = get_player_color()
    board_turn = "white" if st.session_state.board.turn else "black"
    return player_color == board_turn

def save_game_state():
    """Save the current game state for multiplayer"""
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            import json
            game_state = {
                'fen': st.session_state.board.fen(),
                'move_history': st.session_state.move_history,
                'last_updated': time.time()
            }
            
            # Save to a simple file (in a real app, you'd use a database)
            filename = f"game_{st.session_state.room_code}.json"
            with open(filename, 'w') as f:
                json.dump(game_state, f)
            return True
        except:
            return False
    return False

def load_game_state():
    """Load the game state for multiplayer"""
    if st.session_state.game_mode == "multiplayer" and st.session_state.room_code:
        try:
            import json
            filename = f"game_{st.session_state.room_code}.json"
            
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    game_state = json.load(f)
                
                # Update the board
                st.session_state.board = chess.Board(game_state['fen'])
                st.session_state.move_history = game_state['move_history']
                return True
        except:
            pass
    return False

def main():
    # Initialize the game
    init_chess_game()
    
    # Main container
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="glass-title">💎 GLASS CHESS 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="glass-subtitle">Where elegance meets strategy in a crystal-clear interface</p>', unsafe_allow_html=True)
    
    # Display the board
    display_board(st.session_state.board)
    
    # Game status
    status, message = get_game_status(st.session_state.board)
    if status != "normal":
        status_class = f"status-{status}"
        st.markdown(f'<div class="status-message {status_class}">{message}</div>', unsafe_allow_html=True)
    
    # Multiplayer section
    if st.session_state.game_mode == "multiplayer":
        # Auto-load game state for multiplayer
        load_game_state()
        
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🌐 Multiplayer Game")
        
        if st.session_state.room_code:
            st.markdown(f"**Room Code:** `{st.session_state.room_code}`")
            st.markdown(f"**Your Color:** {get_player_color().title()}")
            
            if st.session_state.waiting_for_opponent:
                st.markdown("⏳ **Waiting for opponent to join...**")
                st.markdown("Share the room code with your friend!")
            else:
                if is_player_turn():
                    st.markdown("✅ **Your turn!**")
                else:
                    st.markdown("⏳ **Opponent's turn**")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔙 Back to Single Player", key="back_to_single"):
                st.session_state.game_mode = "single"
                st.session_state.room_code = None
                st.session_state.waiting_for_opponent = False
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh Game", key="refresh_multiplayer"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Single player mode - show multiplayer options
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🎮 Game Mode")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🌐 Create Multiplayer Game", key="create_multiplayer"):
                room_code = create_multiplayer_game()
                st.success(f"Multiplayer game created! Room code: {room_code}")
                st.rerun()
        
        with col2:
            room_input = st.text_input("Join Room Code:", key="join_room_input", placeholder="ABC123")
            if st.button("🎯 Join Game", key="join_multiplayer"):
                if join_multiplayer_game(room_input):
                    st.success("Joined multiplayer game!")
                    st.rerun()
                else:
                    st.error("Invalid room code!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Drag instructions
    st.markdown("""
    <div class="drag-instructions">
        🎯 <strong>How to Play:</strong> Enter moves in UCI notation (e.g., 'e2e4', 'g1f3', 'e7e5')
    </div>
    """, unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("💎 NEW GAME", key="new_game"):
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
    
    # Additional controls
    col5, col6, col7, col8 = st.columns([1, 1, 1, 1])
    
    with col5:
        if st.button("📊 STATS", key="show_stats"):
            stats = get_game_statistics(st.session_state.board, st.session_state.move_history)
            st.session_state.show_stats = not st.session_state.get('show_stats', False)
    
    with col6:
        if st.button("📄 PGN", key="export_pgn"):
            pgn = export_pgn(st.session_state.board, st.session_state.move_history)
            st.code(pgn)
    
    with col7:
        if st.button("🔄 FLIP", key="flip_board"):
            st.session_state.flip_board = not st.session_state.get('flip_board', False)
    
    with col8:
        if st.button("💾 SAVE", key="save_game"):
            st.success("Game state saved!")
    
    # Move input with glass styling
    st.markdown('<div class="glass-input">', unsafe_allow_html=True)
    st.markdown("### 💎 Make Your Move")
    
    # Check if player can make a move
    can_move = st.session_state.game_mode == "single" or is_player_turn()
    
    if not can_move and st.session_state.game_mode == "multiplayer":
        st.markdown("⏳ **Waiting for opponent's move...**")
        if st.button("🔄 Refresh", key="refresh_turn"):
            st.rerun()
    else:
        move_input = st.text_input("Enter move (UCI):", key="move_input", placeholder="e2e4")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("♟️ MAKE MOVE", key="make_move"):
                if move_input:
                    if make_move(move_input):
                        st.rerun()
        
        with col2:
            if st.session_state.game_mode == "single":
                if st.button("🤖 AI MOVE", key="ai_move"):
                    legal_moves = list(st.session_state.board.legal_moves)
                    if legal_moves:
                        # Simple AI: pick a random move
                        ai_move = str(random.choice(legal_moves))
                        if make_move(ai_move):
                            st.rerun()
            else:
                if st.button("🔄 Refresh Game", key="refresh_multiplayer_move"):
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Game information with glass theme
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 💎 Game Info")
        st.markdown(f"**Turn:** {'⚪ White' if st.session_state.board.turn else '⚫ Black'}")
        st.markdown(f"**Moves Made:** {len(st.session_state.move_history)}")
        st.markdown(f"**Legal Moves:** {st.session_state.board.legal_moves.count()}")
        
        if st.session_state.game_mode == "multiplayer":
            st.markdown(f"**Game Mode:** 🌐 Multiplayer")
            st.markdown(f"**Your Color:** {get_player_color().title()}")
            if is_player_turn():
                st.markdown("**Status:** ✅ Your turn")
            else:
                st.markdown("**Status:** ⏳ Opponent's turn")
        else:
            st.markdown("**Game Mode:** 🎮 Single Player")
        
        # Show some suggested moves
        best_moves = get_best_moves(st.session_state.board)
        if best_moves:
            st.markdown("**💎 Suggested Moves:**")
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
            st.markdown("No moves made yet. Start the game! 💎")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Analysis")
        
        # Position analysis
        analysis, status = analyze_position(st.session_state.board)
        st.markdown(f"**Position:** {analysis}")
        
        # Game summary
        summary = generate_game_summary(st.session_state.move_history)
        st.markdown(f"**Summary:** {summary}")
        
        # Move analysis if there's input
        if 'move_input' in st.session_state and st.session_state.move_input:
            move_analysis, move_type = get_move_analysis(st.session_state.move_input, st.session_state.board)
            st.markdown(f"**Move Analysis:** {move_analysis}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics display
    if st.session_state.get('show_stats', False):
        st.markdown('<div class="glass-info">', unsafe_allow_html=True)
        st.markdown("### 📊 Game Statistics")
        
        stats = get_game_statistics(st.session_state.board, st.session_state.move_history)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Piece Count:**")
            for color, pieces in stats['piece_counts'].items():
                st.markdown(f"**{color.title()}:** {', '.join([f'{piece}: {count}' for piece, count in pieces.items()])}")
        
        with col2:
            st.markdown(f"**Game Phase:** {stats['phase']}")
            st.markdown(f"**Center Control:** White: {stats['center_control']['white']}, Black: {stats['center_control']['black']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
