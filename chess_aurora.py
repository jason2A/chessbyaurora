import streamlit as st
import chess
import streamlit.components.v1 as components

# Initialize board in session state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

fen = st.session_state.board.fen()

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
      border-radius: 22px;
      box-shadow: 0 0 40px rgba(0, 255, 255, 0.7), inset 0 0 30px rgba(0, 180, 255, 0.3);
      background: rgba(255,255,255,0.08);
      backdrop-filter: blur(15px);
      padding: 12px;
    }}
    .square-55d63 {{
      transition: background 0.3s ease;
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
    var game = new Chess('{fen}');
    var board = Chessboard('board', {{
      draggable: true,
      position: '{fen}',
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{{{piece}}}}.png',
      moveSpeed: 'slow',
      appearSpeed: 200,
      snapSpeed: 150,
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
    }});

    function onDragStart (source, piece, position, orientation) {{
      if (game.game_over()) return false;
      if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
          (game.turn() === 'b' && piece.search(/^w/) !== -1)) {{
        return false;
      }}
    }}

    function onDrop (source, target) {{
      var move = game.move({{ from: source, to: target, promotion: 'q' }});
      if (move === null) return 'snapback';
      document.querySelectorAll('.square-55d63').forEach(function(sq) {{ sq.classList.remove('highlight'); }});
      var srcEl = document.querySelector('.square-' + source);
      var tgtEl = document.querySelector('.square-' + target);
      if (srcEl) srcEl.classList.add('highlight');
      if (tgtEl) tgtEl.classList.add('highlight');
    }}

    function onSnapEnd () {{
      board.position(game.fen());
    }}
  </script>
</body>
</html>
"""

components.html(html_code, height=650)
