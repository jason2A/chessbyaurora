import streamlit as st
import streamlit.components.v1 as components
import chess
import json
import os

# ----------------------------
# Core game state management
# ----------------------------
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Sidebar controls
with st.sidebar:
    st.header("Game Controls")
    if st.button("New Game"):
        st.session_state.board.reset()
    if st.button("Undo Move"):
        if st.session_state.board.move_stack:
            st.session_state.board.pop()
    st.write("Current turn:", "White" if st.session_state.board.turn else "Black")

# ----------------------------
# Chessboard.js + Animations
# ----------------------------

html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/css/chessboard.min.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/js/chessboard.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>
  <style>
    body {{ background: radial-gradient(circle at center, #0f2027, #203a43, #2c5364); }}
    #board {{
      width: 500px;
      margin: auto;
      box-shadow: 0 0 25px rgba(0,255,255,0.6);
      border-radius: 20px;
    }}
    .square-55d63 {{
      transition: background 0.3s ease;
    }}
    .highlight {{
      box-shadow: inset 0 0 20px cyan, 0 0 15px cyan;
    }}
    .piece-417db {{
      filter: drop-shadow(0 0 8px cyan);
      transition: transform 0.3s ease, filter 0.3s ease;
    }}
    .piece-417db:active {{
      transform: scale(1.1);
      filter: drop-shadow(0 0 15px magenta);
    }}
  </style>
</head>
<body>
  <div id="board"></div>

  <script>
    var board = null
    var game = new Chess('{st.session_state.board.fen()}')

    function onDragStart (source, piece, position, orientation) {
      if (game.game_over()) return false
      if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
          (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false
      }
    }

    function onDrop (source, target) {
      var move = game.move({ from: source, to: target, promotion: 'q' })

      if (move === null) return 'snapback'

      // highlight the move
      document.querySelectorAll('.square-55d63').forEach(sq => sq.classList.remove('highlight'))
      document.querySelector('.square-' + source).classList.add('highlight')
      document.querySelector('.square-' + target).classList.add('highlight')

      // send updated FEN back
      const fen = game.fen()
      fetch('/update_fen', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{fen: fen}})
      }})
    }

    function onSnapEnd () {
      board.position(game.fen())
    }

    board = Chessboard('board', {{
      draggable: true,
      position: '{st.session_state.board.fen()}',
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd,
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
      moveSpeed: 'slow',
      appearSpeed: 200,
      snapSpeed: 150
    }})
  </script>
</body>
</html>
"""

components.html(html_code, height=550)

# ----------------------------
# Simple backend sync for moves
# ----------------------------
# In production, you’d hook this into Streamlit server endpoints or a file/DB.

# For now, we just refresh state if needed
st.write("FEN:", st.session_state.board.fen())
