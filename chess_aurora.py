import streamlit as st
import chess
import chess.svg
import streamlit.components.v1 as components

# Initialize board in session state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Fancy HTML + CSS + JS Chessboard
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/css/chessboard.min.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/js/chessboard.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>
  <style>
    body {{
      margin: 0;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      font-family: 'Segoe UI', sans-serif;
    }}
    #board {{
      width: 520px;
      margin: auto;
      border-radius: 22px;
      box-shadow: 0 0 40px rgba(0, 255, 255, 0.7), inset 0 0 30px rgba(0, 180, 255, 0.3);
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(15px);
      padding: 12px;
    }}
    .square-55d63 {{
      transition: background 0.4s ease;
      border-radius: 6px;
    }}
    .highlight {{
      box-shadow: inset 0 0 18px cyan, 0 0 20px cyan !important;
      border-radius: 8px;
    }}
    .piece-417db {{
      filter: drop-shadow(0 0 8px cyan);
      transition: transform 0.3s ease, filter 0.4s ease;
    }}
    .piece-417db:hover {{
      transform: scale(1.1);
      filter: drop-shadow(0 0 20px magenta);
    }}
    .piece-417db:active {{
      transform: scale(1.2) rotate(5deg);
      filter: drop-shadow(0 0 25px lime);
    }}
  </style>
</head>
<body>
  <div id="board"></div>

  <script>
    var board = null
    var game = new Chess('{st.session_state.board.fen()}')

    function onDragStart (source, piece, position, orientation) {{
      if (game.game_over()) return false
      if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
          (game.turn() === 'b' && piece.search(/^w/) !== -1)) {{
        return false
      }}
    }}

    function onDrop (source, target) {{
      var move = game.move({{ from: source, to: target, promotion: 'q' }})
      if (move === null) return 'snapback'

      document.querySelectorAll('.square-55d63').forEach(sq => sq.classList.remove('highlight'))
      document.querySelector('.square-' + source).classList.add('highlight')
      document.querySelector('.square-' + target).classList.add('highlight')
    }}

    function onSnapEnd () {{
      board.position(game.fen())
    }}

    board = Chessboard('board', {{
      draggable: true,
      position: '{st.session_state.board.fen()}',
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd,
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{piece}}.png',
      moveSpeed: 'slow',
      appearSpeed: 200,
      snapSpeed: 150
    }})
  </script>
</body>
</html>
"""

# Render the board inside Streamlit
components.html(html_code, height=600)
